import logging

from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import Base, ObjectDBO, LevelDBO, LevelContentDBO
from .. import GenericLevel, GenericObject, GenericLevelContent


class Database:

    """
    Singleton SQL local database.
    See https://python-patterns.guide/gang-of-four/singleton/
    """

    _instance = None
    engine = None
    session = None

    def __new__(cls):
        """
        Uses a trick to create only one "true" database instance,
        no matter how many times this class is instantiated.
        This avoids having several engines running on the same file.
        """
        if cls._instance is None:
            logging.info('Creating database instance')

            # Initialization, only called during first instantiation
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine = create_engine('sqlite:///LevelTwo.db', echo=True)
            cls._instance.session = sessionmaker(bind=cls._instance.engine)
            Base.metadata.bind = cls._instance.engine

        return cls._instance

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def delete_tables(self) -> None:
        Base.metadata.drop_all(bind=self.engine)

    def init_session(self):
        return self.session.begin()

    def get_all_levels(self) -> list:
        with self.init_session() as session:
            q = session.query(LevelDBO).all()
        levels = []
        for level in q:
            levels.append(GenericLevel.from_dbo(level))
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
            with self.init_session() as session:
                q = session.query(LevelContentDBO).filter_by(level_id=identifier).all()
                content = [
                    GenericLevelContent(level_id=identifier, x=row.x, y=row.y, value=row.value)
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
