"""
Inserts the content of the example level into the database.
"""

from typing import List

from .default_levels import example_level

from ..models import LevelContentDBO
from ...level import GenericLevel


def insert_levels_content(db) -> None:
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

    # Add level content to the database
    with db.init_session() as session:
        for cell in level_to_dbo_level(example_level):
            session.add(cell)
