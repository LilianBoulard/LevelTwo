from ...object import GenericObject
from ...enums import Effects


class Empty(GenericObject):
    """
    Empty: Default object, doesn't do anything special.
    """
    def __init__(self):
        name = "empty"
        effect = Effects.NONE
        traversable = True
        min_instances = 25
        max_instances = 1000
        super().__init__(1, name, effect, traversable, min_instances, max_instances)


class StartingPoint(GenericObject):
    """
    Start : beginning point of a level.
    """
    def __init__(self):
        name = "start"
        effect = Effects.NONE
        traversable = True
        min_instances = 1
        max_instances = 1
        super().__init__(2, name, effect, traversable, min_instances, max_instances)


class ArrivalPoint(GenericObject):
    def __init__(self):
        name = "arrival"
        effect = Effects.LEVEL_FINISH
        traversable = True
        min_instances = 1
        max_instances = 1
        super().__init__(3, name, effect, traversable, min_instances, max_instances)


class Wall(GenericObject):
    """
    Wall : the character can't go past this obstacle.
    """
    def __init__(self):
        name = "wall"
        effect = Effects.PLAYER_STOP
        traversable = False
        min_instances = 25
        max_instances = 100
        super().__init__(4, name, effect, traversable, min_instances, max_instances)


class Mud(GenericObject):
    """
    Mud : slows the character when walked on.
    """
    def __init__(self):
        name = "mud"
        effect = Effects.PLAYER_SLOW
        traversable = True
        min_instances = 5
        max_instances = 20
        super().__init__(5, name, effect, traversable, min_instances, max_instances)


class Trap(GenericObject):
    """
    Trap : Kills the player when stepped on.
    """
    def __init__(self):
        name = "trap"
        effect = Effects.PLAYER_KILL
        traversable = True
        min_instances = 2
        max_instances = 10
        super().__init__(6, name, effect, traversable, min_instances, max_instances)


all_objects = [Empty, StartingPoint, ArrivalPoint, Wall, Mud, Trap]
