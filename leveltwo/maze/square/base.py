import pygame
import numpy as np

from ..base import Maze, Viewport

from ...sprites.object_to_color import ObjectToColor


class MazeSquare(Maze):

    def draw_grid(self) -> None:
        """
        Constructs the maze's grid and draws rectangles for each cell on the screen.
        """
        z_x, z_y = self.get_z()
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
