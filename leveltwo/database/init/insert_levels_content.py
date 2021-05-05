"""
Inserts the content of the example level into the database.
"""

from typing import List

from .default_levels import all_levels

from ..models import LevelContentDBO
from ...level import GenericLevel


def insert_levels_content(db) -> None:
    def level_to_dbo_level(generic_level: GenericLevel) -> List[LevelContentDBO]:
        all_cells_dbo = []
        level_id = generic_level.identifier
        s_x, s_y = generic_level.content.shape
        for x in range(s_x):
            for y in range(s_y):
                pos_x = x
                pos_y = y
                value = int(generic_level.content[x, y])
                cell_dbo = LevelContentDBO(level_id=level_id,
                                           pos_x=pos_x,
                                           pos_y=pos_y,
                                           value=value)
                all_cells_dbo.append(cell_dbo)
        return all_cells_dbo

    # Add level content to the database
    with db.init_session() as session:
        for level in all_levels:
            for cell in level_to_dbo_level(level):
                session.add(cell)
