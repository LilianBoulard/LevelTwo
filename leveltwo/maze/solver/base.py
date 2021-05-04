from ...database import Database
from ...level import GenericLevel
from ...character import Character


class MazeSolver:

    def __init__(self, level: GenericLevel, character: Character):
        self.level = level
        self.character = character

        db = Database()
        self.objects = db.get_all_objects()

        # State is meant to store the state of each iteration of an algorithm.
        self.state = {}

        self._running: bool = True

    def is_running(self) -> bool:
        return self._running
