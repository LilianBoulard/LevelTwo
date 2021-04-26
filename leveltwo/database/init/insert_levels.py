"""
Inserts an example level into the database.
"""

import numpy as np

from datetime import datetime

from .. import Database
from .. import LevelDBO
from ... import GenericLevel, list_to_string

example_level_content = np.array([[6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                                  [6, 2, 2, 5, 6, 2, 6, 6, 6, 6],
                                  [6, 2, 6, 6, 2, 2, 2, 6, 1, 6],
                                  [6, 2, 2, 6, 2, 6, 2, 6, 2, 6],
                                  [6, 6, 2, 6, 2, 6, 2, 5, 2, 6],
                                  [6, 6, 2, 6, 2, 3, 3, 6, 2, 6],
                                  [6, 2, 2, 6, 2, 6, 2, 2, 3, 6],
                                  [6, 2, 6, 2, 2, 6, 6, 2, 2, 6],
                                  [6, 2, 2, 2, 5, 2, 2, 6, 6, 6],
                                  [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]])
example_level = GenericLevel(0, 'Example maze', 'LevelTwoTeam', example_level_content,
                             datetime.utcfromtimestamp(1619433467), datetime.utcfromtimestamp(1619433745))


def insert_levels() -> None:
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

    db = Database()

    # Add level to the database
    with db.init_session() as session:
        session.add(level_to_dbo_level(example_level))
