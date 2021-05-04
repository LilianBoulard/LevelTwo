import pygame
import numpy as np

from typing import Tuple, Optional, Dict

from ..enums import Colors
from ..database import Database
from ..level import GenericLevel
from ..sprites.object_to_color import ObjectToColor


BoundType = Tuple[int, int, int, int]


class Viewport:

    def __init__(self, name, bounds: BoundType):
        self.name = name
        self.bounds = bounds
        self.origin_x, self.origin_y, self.end_x, self.end_y = bounds

    def inside(self, x: int, y: int) -> bool:
        if self.origin_x < x < self.end_x and self.origin_y < y < self.end_y:
            return True
        else:
            return False


class Maze:

    def __init__(self, parent_display, level):
        self.parent = parent_display
        self.level: GenericLevel = level
        self.maze_shape = self.level.content.shape

        db = Database()
        self.objects = db.get_all_objects()

        self.cells_coordinates_matrix = np.empty((self.level.content.shape[0], self.level.content.shape[1], 4))
        self.viewports: Dict[str, Viewport] = {}

        self.screen_size = self.parent.screen_size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.adjust_style()

        self._running: bool = True

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
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.level.name)  # Set the window title
        callback()
        self.adjust_style()

    def adjust_style(self) -> None:
        self.screen.fill(Colors.WHITE)  # Set the background color

    def get_z(self) -> Tuple[int, int]:
        """
        Computes `z`, which is the size each cell has on the screen (in pixels).
        """
        x = self.screen_size[0]
        y = self.screen_size[1]
        x_cells, y_cells = self.maze_shape

        # Calculate the maximum z on both axis.
        # Note: Using a round division might produce some unwanted margins around the edges,
        # So we calculate the new y and x, and resize the window to these later on.
        calculated_z_x = x // x_cells
        calculated_z_y = y // y_cells

        # Check if projecting each z on the other axis works.
        # If it doesn't for one, return the other.
        # If it does for both, return the largest.
        if calculated_z_x * y_cells > y:
            z = calculated_z_y
        elif calculated_z_y * x_cells > x:
            z = calculated_z_x
        else:
            z = max(calculated_z_x, calculated_z_y)

        # remainder_x = x - (x_cells * z)
        # remainder_y = y - (y_cells * z)

        # if remainder_x > 0 or remainder_y > 0:
        #     new_x = x - remainder_x
        #     new_y = y - remainder_y
        #     self.resize(new_x, new_y, self.draw_grid())

        return z, z

    def draw_grid(self) -> None:
        """
        Constructs the maze's grid and draws rectangles for each cell on the screen.
        """
        z = self.get_z()
        z_x, z_y = z
        # On the x and y axis, how many cells we want
        s_x, s_y = self.level.content.shape
        for i_x in range(s_x):
            for i_y in range(s_y):
                x = i_x * z_x
                y = i_y * z_y

                origin_x = x
                origin_y = y
                end_x = x + z_x
                end_y = y + z_y

                self.cells_coordinates_matrix[i_x, i_y] = np.array([origin_x, origin_y, end_x, end_y])
                cell = self.level.content[i_x, i_y] - 1  # objects are 1-indexed in the level content
                # Draw the rectangle.
                rect = pygame.Rect(x, y, z_x, z_y)
                try:
                    color = ObjectToColor[self.objects[cell].name].value
                except IndexError:
                    color = (0, 0, 0)
                pygame.draw.rect(self.screen, color, rect)

        # Update viewport
        viewport_name = 'grid'
        viewport_end_x = z_x * s_x
        viewport_end_y = z_y * s_y
        grid_viewport = Viewport(viewport_name, (0, 0, viewport_end_x, viewport_end_y))
        self.viewports[viewport_name] = grid_viewport

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

    def get_clicked_cell_index(self, x: int, y: int) -> Tuple[int, int]:
        """
        Iterates through the cells matrix and returns the coordinates of the
        one the user clicked on, based on the coordinates of his input.
        """
        searching_for = self.get_bounds(x, y)
        cell_index = np.where((self.cells_coordinates_matrix == searching_for).all(axis=2))
        print(int(cell_index[0]), int(cell_index[1]))
        return int(cell_index[0]), int(cell_index[1])