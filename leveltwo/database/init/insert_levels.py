"""
Inserts an example level into the database.
"""

from .default_levels import example_level

from ..models import LevelDBO
from ...level import GenericLevel
from ...utils import list_to_string


def insert_levels(db) -> None:
    def level_to_dbo_level(generic_level: GenericLevel) -> LevelDBO:
        name = generic_level.name
        author = generic_level.author
        shape = list_to_string(generic_level.content.shape)
        creation_date = generic_level.creation_date
        last_modification_date = generic_level.last_modification_date
        level_dbo = LevelDBO(name=name,
                             author=author,
                             shape=shape,
                             creation_date=creation_date,
                             last_modification_date=last_modification_date)
        return level_dbo

    # Add level to the database
    with db.init_session() as session:
        session.add(level_to_dbo_level(example_level))
