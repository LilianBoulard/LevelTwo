import os
import logging
import sqlite3
import leveltwo

from typing import List
from pathlib import Path
from datetime import datetime

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker

from .init import insert_objects, insert_levels, insert_levels_content
from .models import Base, ObjectDBO, LevelDBO, LevelContentDBO, TestDBO, TestContentDBO

from ..object import GenericObject
from ..level import GenericLevel, GenericLevelContent


class Database:

    """
    Singleton SQL local database.
    See https://python-patterns.guide/gang-of-four/singleton/
    """

    _instance = None
    engine = None
    session = None

    def __new__(cls, init: bool = True):
        """
        Uses a trick to create only one "true" database instance,
        no matter how many times this class is instantiated.
        This avoids having several engines running on the same file.
        """
        if cls._instance is None:
            logging.info('Creating database instance')

            # Initialization, only called during first instantiation
            cls._instance = super(Database, cls).__new__(cls)
            path = Path(os.path.abspath(leveltwo.__file__)).parent
            db_path = os.path.join(path, "LevelTwo.db")
            cls._instance.engine = create_engine(f'sqlite:///{db_path}')
            cls._instance.session = sessionmaker(bind=cls._instance.engine)
            Base.metadata.bind = cls._instance.engine
            if init:
                cls._instance.init_db()

        return cls._instance

    def init_db(self):
        logging.info('Initiating database')

        try:
            count = self.get_tables_counts()
        except sqlite3.OperationalError:
            # If we could not query the tables,
            # that means we must create the tables and insert the default values in.
            delete_tables = False
            create_tables = True
            insert_values = True
        else:
            # If we could query the tables, that means we don't have to delete nor create them.
            delete_tables = False
            create_tables = False
            if any([v == 0 for v in count]):
                # If any of the tables are empty, we'll insert the default values
                insert_values = True
            else:
                insert_values = False

        if delete_tables:
            self.delete_tables()
        if create_tables:
            self.create_tables()

        if insert_values:
            insert_objects(self)
            insert_levels(self)
            insert_levels_content(self)

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)
        logging.info('Created all tables')

    def delete_tables(self) -> None:
        Base.metadata.drop_all(bind=self.engine)
        logging.info('Deleted all tables')

    def init_session(self):
        return self.session.begin()

    def get_tables_counts(self) -> dict:
        with self.init_session() as session:
            object_count = session.query(ObjectDBO.id).count()
            level_count = session.query(LevelDBO.id).count()
            level_content_count = session.query(LevelContentDBO.id).count()
            tests_count = session.query(TestDBO.id).count()
            tests_content_count = session.query(TestContentDBO.id).count()

        return {
            ObjectDBO.__tablename__: object_count,
            LevelDBO.__tablename__: level_count,
            LevelContentDBO.__tablename__: level_content_count,
            TestDBO.__tablename__: tests_count,
            TestContentDBO.__tablename__: tests_content_count
        }

    def update_level_content(self, level: GenericLevel) -> None:

        level_id = level.identifier
        if level_id is None or not self.level_exists(level_id):
            # If the level does not exist already, we'll add it
            self.add_new_level(level)
        else:
            # If the level already exists in the database
            # First, update its content
            s_x, s_y = level.content.shape
            with self.init_session() as session:
                for x in range(s_x):
                    for y in range(s_y):
                        cell = session.query(LevelContentDBO).filter(LevelContentDBO.level_id == level_id,
                                                                     LevelContentDBO.pos_x == x,
                                                                     LevelContentDBO.pos_y == y).one()
                        cell.value = int(level.content[x, y])
            # Next, update the modification date in the levels table
            with self.init_session() as session:
                level_dbo = session.query(LevelDBO).filter(LevelDBO.id == level_id).one()
                level_dbo.last_modification_date = datetime.now()

    def add_new_level(self, level: GenericLevel) -> None:
        """
        Takes a new generic level, and adds it to the database.
        """
        # First, add the level
        with self.init_session() as session:
            level_dbo = level.to_dbo()
            # Using arbitrary format ? Ouch...
            session.add(level_dbo)
        # Next, add the level's content
        s_x, s_y = level.content.shape
        with self.init_session() as session:
            # Get the level id from the database
            db_level = session.query(LevelDBO).filter(LevelDBO.name == level.name,
                                                      LevelDBO.author == level.author).one()
            for x in range(s_x):
                for y in range(s_y):
                    cell = LevelContentDBO(db_level.id, x, y, int(level.content[x, y]))
                    session.add(cell)

    def level_exists(self, level_id: int) -> bool:
        """
        Checks if a level exists in the database based on its ID.
        Returns True if it does, False otherwise.
        """
        with self.init_session() as session:
            b = session.query(exists().where(LevelDBO.id == level_id)).scalar()
        return b

    def get_all_levels(self) -> List[GenericLevel]:
        with self.init_session() as session:
            q = session.query(LevelDBO.id).all()
        levels = []
        for content in q:  # Is it correct ?
            for level_id in content:
                levels.append(self.construct_level(level_id))
        return levels

    def get_all_objects(self) -> List[GenericObject]:
        """
        Returns a list of the objects in the database
        """
        with self.init_session() as session:
            result = session.query(ObjectDBO).all()
            objects = [GenericObject.from_dbo(row) for row in result]
        return objects

    def construct_level(self, level_id: int) -> GenericLevel:

        def get_content(identifier: int) -> List[GenericLevelContent]:
            with self.init_session() as s:
                q = s.query(LevelContentDBO).filter_by(level_id=identifier).all()
                content = [
                    GenericLevelContent(level_id=identifier, x=row.pos_x, y=row.pos_y, value=row.value)
                    for row in q
                ]
            return content

        with self.init_session() as session:
            level = GenericLevel.from_dbo(session.query(LevelDBO).filter_by(id=level_id).one())

        mapping = get_content(level.identifier)
        # For each cell stored in the database, paste its content in the array.
        # Note: possible optimization: remove all cells in the database that have
        # their value to `0`, as we create by default an array of zeros.
        for cell in mapping:
            level.content[cell.x, cell.y] = cell.value
        return level
