import logging

from typing import List

from collections import namedtuple

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, ObjectDBO, LevelDBO, LevelContentDBO
from ..objects import GenericObject
from ..level import GenericLevel


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

    def __del__(self):
        if self.session is not None:
            raise Exception('Session is ongoing, please clear it using method `end_session` before quitting.')

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def init_session(self):
        return self.session.begin()

    def get_all_levels(self) -> List[GenericLevel]:
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

    def get_level_content_by_id(self, identifier: int) -> List[namedtuple]:
        with self.init_session() as session:
            q = session.query(LevelContentDBO).filter_by(level_id=identifier)
            LevelContent = namedtuple('LevelContent', ('x', 'y', 'value'))
            content = [
                LevelContent(x=row.x, y=row.y, value=row.value)
                for row in q
            ]
        return content
