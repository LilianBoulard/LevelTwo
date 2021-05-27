import numpy as np

from typing import Tuple

from .base import MazeSquare
from ..base import MazeEditable


class MazeEditableSquare(MazeEditable, MazeSquare):

    def get_clicked_cell_index(self, x: int, y: int) -> Tuple[int, int]:
        searching_for = self.get_bounds(x, y)
        cell_index = np.where((self.cells_coordinates_matrix == searching_for).all(axis=2))
        return int(cell_index[0]), int(cell_index[1])
