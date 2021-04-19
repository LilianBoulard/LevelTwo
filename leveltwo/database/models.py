"""
Defines the database models.
"""

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
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
    creation_date = Column(Date, default=datetime.utcnow())
    last_modification_date = Column(Date)
    shape = Column(String(8))

    def __init__(self, name: str, author: str, creation_date: int, last_modification_date: int):
        self.name = name
        self.author = author
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date


class LevelContentDBO(Base):
    __tablename__ = "levels_content"

    id = Column(Integer, primary_key=True)
    level_id = Column(ForeignKey('levels.id', ondelete='CASCADE'))
    pos_x = Column(Integer)
    pos_y = Column(Integer)
    value = Column(String)

    def __init__(self, name: str, pos_x: int, pos_y: int, value: str):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.value = value
