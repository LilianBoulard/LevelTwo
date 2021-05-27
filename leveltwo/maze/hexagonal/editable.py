from typing import Tuple

from .base import MazeHexagonal
from ..base import MazeEditable


class MazeEditableHexagonal(MazeHexagonal, MazeEditable):

    def get_clicked_cell_index(self, x: int, y: int) -> Tuple[int, int]:
        pass
