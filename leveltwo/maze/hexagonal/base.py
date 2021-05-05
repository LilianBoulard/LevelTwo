import pygame
import numpy as np

from typing import Tuple
from math import cos, sin, pi, sqrt, floor

from ..base import Maze, Viewport

from ...sprites.object_to_color import ObjectToColor


def draw_ngon(surface, color, n, radius, position, display_border: bool = False):
    pi2 = 2 * pi
    points = [(cos(i / n * pi2) * radius + position[0], sin(i / n * pi2) * radius + position[1]) for i in range(0, n)]

    polygon = pygame.draw.polygon(surface, color, points)

    if display_border:
        pygame.draw.lines(surface, (0, 0, 0), True, points)

    return polygon


def find_nearest_point(array: np.array, point: Tuple[int, int]):
    idx = (np.abs(array - point)).argmin()
    return array[idx]


class MazeHexagonal(Maze):

    def init_cell_coordinates_matrix(self) -> np.array:
        return np.empty((self.level.content.shape[0], self.level.content.shape[1], 2))

    def draw_grid(self) -> None:
        """
        Constructs the maze's grid and draws rectangles for each cell on the screen.
        """
        z_x, z_y = self.get_z()
        z = min(z_x, z_y)
        s_x, s_y = self.level.content.shape

        # Size is the length between the center and any of the edges of the hexagon
        size = (z // 2)
        hexagon_width = 2 * size
        hexagon_height = sqrt(3) * size
        horizontal_offset = -(hexagon_width * 0.25)
        vertical_offset = (s_x / 2) * size

        for x_i, y_i in self.level.iterate_over_shape():
            x = floor((x_i + 1) * (hexagon_width * 0.75) + horizontal_offset)
            y = floor(-(x_i * (hexagon_height // 2)) + (y_i * hexagon_height) + vertical_offset)

            self.cells_coordinates_matrix[x_i, y_i] = np.array([x, y])
            cell = self.level.content[x_i, y_i] - 1
            color = ObjectToColor[self.objects[cell].name].value
            draw_ngon(self.screen, color, 6, size, (x, y), True)

        # Update viewport
        viewport_name = 'grid'
        viewport_end_x = hexagon_width * s_x
        viewport_end_y = hexagon_height * s_y
        grid_viewport = Viewport(viewport_name, (0, 0, viewport_end_x, viewport_end_y))
        self.viewports[viewport_name] = grid_viewport

    def get_z(self) -> Tuple[int, int]:
        """
        Computes `z`, which is the size each cell has on the screen (in pixels).
        """
        x, y = self.screen_size

        x_cells, y_cells = self.level.content.shape

        # Calculate the maximum z on both axis.
        z_x = x // x_cells
        z_y = y // y_cells

        z = min(z_x, z_y)

        return z, z

    def get_cell_center(self, x: int, y: int) -> Tuple[int, int]:
        return self.cells_coordinates_matrix[x, y]
