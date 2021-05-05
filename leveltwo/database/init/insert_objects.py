"""
Inserts default objects into the database.
"""

from .default_objects import all_objects


def insert_objects(db):
    with db.init_session() as session:
        for obj in all_objects:
            session.add(obj().to_dbo())
