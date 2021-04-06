"""
Implements a generic database interface for interacting with SQLAlchemy.
"""
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///LevelTwo.db', echo=True)  # Create the Database file

Base = declarative_base()


class Object(Base):
    """"""
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    effect = Column(Integer)
    traversable = Column(Boolean)
    min_instances = Column(Integer)
    max_instances = Column(Integer)

    # ----------------------------------------------------------------------
    def __init__(self, name, effect, traversable, min_instances, max_instances):
        """"""
        self.name = name
        self.effect = effect
        self.traversable = traversable
        self.min_instances = min_instances
        self.max_instances = max_instances


class ObjectSprites(Base):
    """"""
    __tablename__ = "objects_sprites"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    pos_x = Column(String)
    pos_y = Column(String)
    value = Column(String)

    # ----------------------------------------------------------------------
    def __init__(self, name, pos_x, pos_y, value):
        """"""
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.value = value


class Levels(Base):
    """"""
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    creation_date = Column(Date)
    last_modification_date = Column(String)

    # ----------------------------------------------------------------------
    def __init__(self, name, author, creation_date, last_modification_date):
        """"""
        self.name = name
        self.author = author
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date


class LevelsContent(Base):
    """"""
    __tablename__ = "levels_content"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    pos_x = Column(String)
    pos_y = Column(String)
    value = Column(String)

    # ----------------------------------------------------------------------
    def __init__(self, name, pos_x, pos_y, value):
        """"""
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.value = value


# create tables
Base.metadata.create_all(engine)
