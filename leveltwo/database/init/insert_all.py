from .insert_levels import insert_levels
from .insert_objects import insert_objects
from .insert_levels_content import insert_levels_content

from ..database import Database


def insert_all() -> None:

    db = Database(init=False)

    # Reset all tables
    db.delete_tables()
    db.create_tables()

    # Insert all
    insert_objects(db)
    insert_levels(db)
    insert_levels_content(db)

    count = db.get_tables_counts()
    print(count)


if __name__ == "__main__":
    insert_all()
