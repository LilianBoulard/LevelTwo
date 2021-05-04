from ....database import Database
from ....level import GenericLevel
from ....character import Character


class MazeSolvingAlgorithm:

    def __init__(self, level: GenericLevel, character: Character):
        self.level = level
        self.level.construct_object_content()
        self.character = character

        db = Database()
        self.objects = db.get_all_objects()

        self._running = True

    def is_running(self) -> bool:
        return self._running

    def run_one_step(self, *args, **kwargs):
        raise NotImplementedError()
