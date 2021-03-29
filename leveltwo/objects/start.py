"""
Start : beginning point of a level.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import LevelEffects


class Wall(GenericObject):
    def __init__(self):
        name = "start"
        effect = LevelEffects.NONE
        traversable = True
        appearance = []
        min_instances = 1
        max_instances = 1
        super().__init__(name, effect, traversable, appearance, min_instances, max_instances)
