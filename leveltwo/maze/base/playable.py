from abc import ABC

import pygame

from time import sleep
from datetime import datetime
from typing import Tuple, List

from .maze import Maze

from ...test import Test
from ...enums import Colors
from ...database import Database
from ...character import Character
from ...algorithm.base import MazeSolvingAlgorithm, Manual


class MazePlayable(Maze, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        starting_point_location = self.level.get_starting_point_position()
        self.character = Character(*starting_point_location)
        self.db = Database()
        objects = self.db.get_all_objects()
        self.level.set_objects(objects)

    def draw(self) -> None:
        self.adjust_screen(self.draw)
        self.draw_grid()
        self.draw_character()
        pygame.display.update()

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

    def run(self, algorithm_class) -> None:
        """
        Main loop.
        """
        save: bool = False
        algo: MazeSolvingAlgorithm = algorithm_class(self.level, self.character)
        manual: bool = isinstance(algo, Manual)

        self.draw()
        while self._running:
            key = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h, self.draw)
                if manual:
                    # If on manual mode (human-controller)
                    if event.type == pygame.KEYDOWN:
                        key = event.key

            # Keyword arguments to pass to the algorithm iteration.
            kwargs = {}

            if isinstance(algo, Manual):
                kwargs.update({
                    'key': key
                })

            # If not human-controller, advance the algorithm one step.
            algo.run_one_step(**kwargs)
            self.draw()
            if not algo.is_running():
                save = True
                self._running = False

            if not manual:
                sleep(0.2)

            pygame.display.update()

        if save:
            # If we finished the level one way or another, we'll save the run in the database.
            test = Test(identifier=None,
                        level_id=self.level.identifier,
                        algorithm=algo.name,
                        steps=self.character.path,
                        run_date=datetime.now())
            self.db.store_test(test)
