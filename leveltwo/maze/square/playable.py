import pygame

from .base import MazeSquare
from ..base import MazePlayable

from ...enums import Colors


class MazePlayableSquare(MazePlayable, MazeSquare):

    def draw_character(self) -> None:
        # Compute coordinates
        x, y = self.character.location
        center_x, center_y = self.get_cell_center(x, y)
        # Draw circle
        z, z = self.get_z()
        pygame.draw.circle(self.screen, Colors.RED, (center_x, center_y), z * 0.8 // 2)
