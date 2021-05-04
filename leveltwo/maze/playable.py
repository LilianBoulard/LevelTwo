import pygame

from datetime import datetime

from .base import Maze
from .solver import MazeSolverSquare

from ..test import Test
from ..enums import Colors
from ..database import Database
from ..character import Character

pygame.init()


class MazePlayable(Maze):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        starting_point_location = self.level.get_starting_point_position()
        self.character = Character(*starting_point_location)
        self.solver = MazeSolverSquare(self.level, self.character)

    def draw_character(self) -> None:
        # Compute coordinates
        x, y = self.character.location
        origin_x, origin_y, end_x, end_y = self.cells_coordinates_matrix[x, y]
        center_x = origin_x + ((end_x - origin_x) // 2)
        center_y = origin_y + ((end_y - origin_y) // 2)
        # Draw circle
        pygame.draw.circle(self.screen, Colors.RED, (center_x, center_y), 20)

    def draw(self) -> None:
        self.draw_grid()
        self.draw_character()

    def rerun(self, test: Test, delay: int = 0.2) -> None:
        """
        Takes a test, and runs it so as to visualize the steps the algorithm took.
        :param Test test: the test to run
        :param int delay: how long we should wait before displaying each step.
        """
        pass

    def run(self, algorithm) -> None:
        """
        Main loop.
        """
        algorithm_name: str = algorithm.__name__
        manual: bool = algorithm_name == 'manual'
        save: bool = False
        first_iter: bool = True

        self.draw()
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h, self.draw())
                if manual:
                    # If on manual mode (human-controller)
                    if event.type == pygame.KEYDOWN:
                        self.solver.manual(event.key)
                        if not self.solver.is_running():
                            save = True
                            self._running = False
                        self.draw()

            if not manual:
                # If not human-controller, advance the algorithm one step.
                # To keep values between iterations, use the dictionary attribute `state`

                # TODO: replace strings by __name__ attributes

                if first_iter:
                    # Initialization part
                    if algorithm_name == 'recursive_walk':
                        x, y = self.character.location
                        self.solver.state.update({
                            'x': x,
                            'y': y
                        })

                algorithm(self.solver)

            pygame.display.update()

        if save:
            # If we finished the level one way or another, we'll save the run in the database.
            test = Test(identifier=None,
                        level_id=self.level.identifier,
                        algorithm=algorithm_name,
                        steps=self.character.path,
                        run_date=datetime.now())
            db = Database()
            db.store_test(test)
