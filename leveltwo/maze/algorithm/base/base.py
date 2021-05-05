from ....object import GenericObject
from ....database import Database
from ....level import GenericLevel
from ....character import Character


class Visited(GenericObject):
    """
    Visited: signals the way we came from.
    """
    def __init__(self, identifier, effect, traversable, min_instances, max_instances):
        name = Visited.__name__.lower()
        super().__init__(identifier, name, effect, traversable, min_instances, max_instances)

    @classmethod
    def from_existing(cls, obj: GenericObject):
        """
        Takes an object, and impersonates it (inherits its attributes).
        """
        identifier = obj.identifier
        effect = obj.effect
        traversable = obj.traversable
        min_instances = obj.min_instances
        max_instances = obj.max_instances
        return cls(identifier, effect, traversable, min_instances, max_instances)


class Deadend(GenericObject):
    """
    Deadend: signals a way that has already been visited, and leads to nowhere.
    It is somewhat considered a wall.
    """
    def __init__(self, identifier, effect, traversable, min_instances, max_instances):
        name = Deadend.__name__.lower()
        super().__init__(identifier, name, effect, traversable, min_instances, max_instances)

    @classmethod
    def from_existing(cls, obj: GenericObject):
        """
        Takes an object, and impersonates it (inherits its attributes).
        """
        identifier = obj.identifier
        effect = obj.effect
        traversable = False
        min_instances = obj.min_instances
        max_instances = obj.max_instances
        return cls(identifier, effect, traversable, min_instances, max_instances)


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
