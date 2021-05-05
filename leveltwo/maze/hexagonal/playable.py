import pygame

from .base import MazeHexagonal
from ..base import MazePlayable

from ...enums import Colors


class MazePlayableHexagonal(MazePlayable, MazeHexagonal):

    def draw_character(self) -> None:
        # Compute coordinates
        x, y = self.character.location
        center_x, center_y = self.cells_coordinates_matrix[x, y]
        # Draw circle
        z, z = self.get_z()
        pygame.draw.circle(self.screen, Colors.RED, (center_x, center_y), z * 0.7 // 2)
