import pygame
import numpy as np

from typing import Tuple, Optional, Dict

from .base import Viewport, BoundType

from ...enums import Colors
from ...database import Database
from ...level import GenericLevel


class Maze:

    def __init__(self, parent_display, level):
        self.parent = parent_display
        self.level: GenericLevel = level

        db = Database()
        self.objects = db.get_all_objects()

        self.cells_coordinates_matrix = self.init_cell_coordinates_matrix()
        self.viewports: Dict[str, Viewport] = {}

        self.screen_size = self.parent.screen_size
        self.screen = self.get_screen()
        self.adjust_style()

        self._running: bool = True

    def get_screen(self):
        return pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

    def get_selected_viewport(self, x: int, y: int) -> Viewport:
        """
        Given `x` and `y`, returns the viewport the user clicked in.
        """
        for viewport in self.viewports.values():
            if viewport.inside(x, y):
                return viewport

        # Create dummy viewport that spans the entire window.
        max_x, max_y, = self.screen_size
        return Viewport('outside', (0, 0, max_x, max_y))

    def resize(self, x: int, y: int, callback) -> None:
        """
        Resize window.

        :param int x: New size on the `x` axis
        :param int y: New size on the `y` axis
        :param callback: Function to call once the resizing has been performed.
        """
        self.screen_size = (x, y)
        self.screen = self.get_screen()
        pygame.display.set_caption(self.level.name)  # Set the window title
        self.adjust_style()
        callback()

    def adjust_style(self) -> None:
        self.screen.fill(Colors.WHITE)  # Set the background color

    def init_cell_coordinates_matrix(self) -> np.array:
        raise NotImplementedError()

    def get_z(self) -> Tuple[int, int]:
        raise NotImplementedError()

    def draw_grid(self) -> None:
        """
        Constructs the maze's grid and draws rectangles for each cell on the screen.
        """
        raise NotImplementedError()

    def adjust_screen(self, callback, *, down_margin: int = 0, right_margin: int = 0) -> None:
        """
        Calculates the size each viewport should have on the screen,
        and resize the window accordingly.
        """
        x, y = self.screen_size
        z_x, z_y = self.get_z()

        x_cells, y_cells = self.level.content.shape

        remainder_x = x - (x_cells * z_x) - right_margin
        remainder_y = y - (y_cells * z_y) - down_margin

        if remainder_x > 0 or remainder_y > 0:
            new_x = x - remainder_x
            new_y = y - remainder_y
            self.resize(new_x, new_y, callback)

    def get_bounds(self, x: int, y: int, z: Optional[Tuple[int, ...]] = None) -> BoundType:
        """
        Given two coordinates, `x` and `y`, returns the bounds of the square they land in.
        Example (with `self.get_z()` returning `10`):
        >>> self.get_bounds(4, 29)
        (0, 20, 10, 30)
        """
        if z is None:
            z = self.get_z()
        z_x, z_y = z

        x_remainder = x % z_x
        y_remainder = y % z_y

        x_lower = x - x_remainder
        y_lower = y - y_remainder

        x_upper = x_lower + z_x
        y_upper = y_lower + z_y

        bounds = (x_lower, y_lower, x_upper, y_upper)

        return bounds

    def get_cell_center(self, x: int, y: int) -> Tuple[int, int]:
        raise NotImplementedError()
