import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, ObjectDBO, LevelDBO, LevelContentDBO
from ..objects import GenericObject


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
            cls._instance.engine = create_engine(f'sqlite:///LevelTwo.db', echo=True)
            cls._instance.session = None
            Base.metadata.bind = cls._instance.engine

        return cls._instance

    def __del__(self):
        if self.session is not None:
            raise Exception('Session is ongoing, please clear it using method `end_session` before quitting.')

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def init_session(self):
        return sessionmaker(bind=self.engine)

    def get_all_levels(self):
        with self.init_session() as session:
            q = session.query(LevelDBO).all()
        return q

    def get_all_objects(self) -> dict:
        """
        Returns a mapping of the objects and their respective ID in the database.
        Example:
        >>> self.get_all_objects()
        {0: Empty, 1: Wall, 2: Trap, 3: Mud}
        """
        with self.init_session() as session:
            mapping = {}
            result = session.query(ObjectDBO).all()
            for obj in result:
                mapping.update({obj.id, GenericObject.from_dbo(obj)})
        return mapping

    def get_level(self, id: int):
        pass
