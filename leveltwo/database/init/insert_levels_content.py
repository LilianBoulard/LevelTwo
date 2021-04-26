"""
Inserts the content of the example level into the database.
"""

import numpy as np

from typing import List
from datetime import datetime

from .. import Database
from .. import LevelContentDBO
from ... import GenericLevel


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


def insert_levels_content() -> None:
    def level_to_dbo_level(generic_level: GenericLevel) -> List[LevelContentDBO]:
        all_cells_dbo = []
        level_id = generic_level.identifier
        for pos_x in generic_level.content:
            for pos_y, value in enumerate(pos_x):
                pos_x = pos_x
                pos_y = pos_y
                value = value
                cell_dbo = LevelContentDBO(level_id=level_id,
                                           pos_x=pos_x,
                                           pos_y=pos_y,
                                           value=value)
                all_cells_dbo.append(cell_dbo)
        return all_cells_dbo

    db = Database()

    # Add level content to the database
    with db.init_session() as session:
        for cell in level_to_dbo_level(example_level):
            session.add(cell)
