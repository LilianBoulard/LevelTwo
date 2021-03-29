from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class LevelDBO(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    creation_date = Column(DateTime)
    last_modification_date = Column(DateTime)
    content = Column(String)


class ObjectsDatabase:

    def __init__(self):
        engine = create_engine('sqlite:///levels.db')
        Base.metadata.bind = engine
        session_o = sessionmaker(bind=engine)
        self.session = session_o()

    def add_object(self):
        pass

    def remove_object(self):
        pass

    def update_object(self):
        pass

    def get_object_info(self):
        pass
