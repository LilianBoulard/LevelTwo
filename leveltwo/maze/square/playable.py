import pygame

from time import sleep

from datetime import datetime

from .base import MazeSquare
from ..algorithm.base import MazeSolvingAlgorithm
from ..base import MazePlayable

from ...test import Test

pygame.init()


class MazePlayableSquare(MazePlayable, MazeSquare):

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
                    self.resize(event.w, event.h, self.draw)
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

            if not manual:
                sleep(0.2)

            pygame.display.update()

        if save:
            # If we finished the level one way or another, we'll save the run in the database.
            test = Test(identifier=None,
                        level_id=self.level.identifier,
                        algorithm=algorithm_name,
                        steps=self.character.path,
                        run_date=datetime.now())
            self.db.store_test(test)
