"""
Implements a generic database interface for interacting with SQLAlchemy.
"""
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///LevelTwo_LevelsContent.db', echo=True)  # Create the Database file

Base = declarative_base()


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
def create_levels_content():
    Base.metadata.create_all(engine)