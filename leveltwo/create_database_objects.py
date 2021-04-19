"""
Implements a generic database interface for interacting with SQLAlchemy.
"""
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///LevelTwo_Objects.db', echo=True)  # Create the Database file

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


# create tables
def create_objects():
    Base.metadata.create_all(engine)
