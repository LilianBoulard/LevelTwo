"""
Inserts an example level into the database.
"""

from .default_levels import all_levels


def insert_levels(db) -> None:
    with db.init_session() as session:
        for level in all_levels:
            session.add(level.to_dbo())
