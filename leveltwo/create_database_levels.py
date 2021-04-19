"""
Implements a generic database interface for interacting with SQLAlchemy.
"""
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///LevelTwo_Levels.db', echo=True)  # Create the Database file

Base = declarative_base()


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


# create tables
def create_levels():
    Base.metadata.create_all(engine)
