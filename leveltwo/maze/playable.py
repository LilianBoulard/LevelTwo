import pygame

from .base import Maze

from ..enums import Colors
from ..character import Character
from .solver import MazeSolverSquare

pygame.init()


class MazePlayable(Maze):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        starting_point_location = self.level.get_starting_point_position()
        x = starting_point_location[0]
        y = starting_point_location[1]
        print(x , y)
        self.character = Character(*starting_point_location)
        #solver = MazeSolverSquare(self.level, self.character).recursive_walk(x, y)
        solver = MazeSolverSquare(self.level, self.character).astar()

    def draw_character(self):
        # Compute coordinates
        x, y = self.character.location
        origin_x, origin_y, end_x, end_y = self.cells_coordinates_matrix[x, y]
        center_x = origin_x + ((end_x - origin_x) // 2)
        center_y = origin_y + ((end_y - origin_y) // 2)
        # Draw circle
        pygame.draw.circle(self.screen, Colors.RED, (center_x, center_y), 20)

    def draw(self):
        self.draw_grid()
        self.draw_character()

    def run(self) -> None:
        """
        Main loop.
        """
        self.draw()
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h, self.draw())
                if event.type == pygame.KEYDOWN:
                    self.solver.manual(event.key)
                    self.draw()
            pygame.display.update()
