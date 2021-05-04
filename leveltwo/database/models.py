"""
Defines the database models.
"""

from datetime import datetime

from sqlalchemy import Column, Date, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ObjectDBO(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    effect = Column(Integer)
    traversable = Column(Boolean)
    min_instances = Column(Integer)
    max_instances = Column(Integer)

    def __init__(self, name: str, effect: int, traversable: bool, min_instances: int, max_instances: int):
        self.name = name
        self.effect = effect
        self.traversable = traversable
        self.min_instances = min_instances
        self.max_instances = max_instances


class LevelDBO(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    author = Column(String(64))
    shape = Column(String(8))
    creation_date = Column(Date, default=datetime.utcnow())
    last_modification_date = Column(Date)

    def __init__(self, name: str, author: str, shape: str,
                 creation_date: datetime, last_modification_date: datetime):
        self.name = name
        self.author = author
        self.shape = shape
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date


class LevelContentDBO(Base):
    __tablename__ = "levels_content"

    id = Column(Integer, primary_key=True)
    level_id = Column(ForeignKey('levels.id', ondelete='CASCADE'))
    pos_x = Column(Integer)
    pos_y = Column(Integer)
    value = Column(Integer, default=0)

    def __init__(self, level_id: int, pos_x: int, pos_y: int, value: int):
        self.level_id = level_id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.value = value


class TestDBO(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True)
    level_id = Column(ForeignKey('levels.id', ondelete='CASCADE'))
    algorithm = Column(String(32))
    steps_number = Column(Integer)
    run_date = Column(Date, default=datetime.utcnow())

    def __init__(self, level_id: int, algorithm: str, steps_number: int, run_date: datetime):
        self.level_id = level_id
        self.algorithm = algorithm
        self.steps_number = steps_number
        self.run_date = run_date


class TestContentDBO(Base):
    __tablename__ = "tests_content"

    id = Column(Integer, primary_key=True)
    test_id = Column(ForeignKey('tests.id', ondelete='CASCADE'))
    step = Column(Integer)
    pos_x = Column(Integer)
    pos_y = Column(Integer)

    def __init__(self, test_id: int, step: int, pos_x: int, pos_y: int):
        self.test_id = test_id
        self.step = step
        self.pos_x = pos_x
        self.pos_y = pos_y
