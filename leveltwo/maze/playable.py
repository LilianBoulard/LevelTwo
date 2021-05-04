import pygame

from time import sleep

from datetime import datetime
from typing import Tuple, List

from .base import Maze
from .algorithm.square.base import MazeSolvingAlgorithm

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
        self.db = Database()
        objects = self.db.get_all_objects()
        self.level.set_objects(objects)

    def draw_character(self) -> None:
        # Compute coordinates
        x, y = self.character.location
        center_x, center_y = self.get_cell_center(x, y)
        # Draw circle
        pygame.draw.circle(self.screen, Colors.RED, (center_x, center_y), 20)

    def draw(self) -> None:
        self.draw_grid()
        self.draw_character()
        pygame.display.update()

    def get_cell_center(self, x: int, y: int) -> Tuple[int, int]:
        origin_x, origin_y, end_x, end_y = self.cells_coordinates_matrix[x, y]
        center_x = origin_x + ((end_x - origin_x) // 2)
        center_y = origin_y + ((end_y - origin_y) // 2)
        return center_x, center_y

    def rerun(self, test: Test, delay: int = 0.5) -> None:
        """
        Takes a test, and runs it so as to visualize the steps the algorithm took.
        :param Test test: the test to run
        :param int delay: how long we should wait before displaying each step.
        """

        def draw_path():
            for line in path:
                pygame.draw.line(self.screen, Colors.BLACK, *line)

        self.draw()
        path: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

        delay = int(delay * 1000)  # Convert delay to milliseconds
        last_step = test.steps[0]
        for step in test.steps:
            pygame.time.delay(delay)  # Wait

            # Get the centers of this step and the last
            cell_x, cell_y = step
            cell_center_x, cell_center_y = self.get_cell_center(cell_x, cell_y)
            last_cell_x, last_cell_y = last_step
            last_step_center_x, last_step_center_y = self.get_cell_center(last_cell_x, last_cell_y)

            # Move the character
            self.character.move(cell_x, cell_y)

            # And add a line between the two.
            path.append(((cell_center_x, cell_center_y), (last_step_center_x, last_step_center_y)))

            last_step = step

            self.draw()
            draw_path()
            pygame.display.update()

        pygame.time.delay(800)

    def run(self, algorithm) -> None:
        """
        Main loop.
        """
        algorithm_name: str = algorithm.__name__
        manual: bool = algorithm_name == 'Manual'
        save: bool = False
        algo: MazeSolvingAlgorithm = algorithm(self.level, self.character)

        self.draw()
        while self._running:
            key = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h, self.draw())
                if manual:
                    # If on manual mode (human-controller)
                    if event.type == pygame.KEYDOWN:
                        key = event.key

            # Keyword arguments to pass to the algorithm iteration.
            kwargs = {}

            if algorithm_name == 'Manual':
                kwargs.update({
                    'key': key
                })

            # If not human-controller, advance the algorithm one step.
            algo.run_one_step(**kwargs)
            self.draw()
            if not algo.is_running():
                save = True
                self._running = False
            sleep(0.5)

            pygame.display.update()

        if save:
            # If we finished the level one way or another, we'll save the run in the database.
            test = Test(identifier=None,
                        level_id=self.level.identifier,
                        algorithm=algorithm_name,
                        steps=self.character.path,
                        run_date=datetime.now())
            self.db.store_test(test)
