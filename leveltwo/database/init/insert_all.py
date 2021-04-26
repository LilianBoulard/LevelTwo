from .insert_levels import insert_levels
from .insert_objects import insert_objects
from .insert_levels_content import insert_levels_content

from .. import Database


def insert_all() -> None:

    db = Database()

    # Reset all tables
    db.delete_tables()
    db.create_tables()

    # Insert all
    insert_objects()
    insert_levels()
    insert_levels_content()


if __name__ == "__main__":
    insert_all()
