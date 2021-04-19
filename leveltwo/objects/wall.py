"""
Wall : the character can't go past this obstacle.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import LevelEffects


class Wall(GenericObject):
    def __init__(self, **kwargs):
        name = "wall"
        effect = LevelEffects.STOP
        traversable = False
        appearance = []
        min_instances = 4
        max_instances = 10
        super().__init__(name, effect, traversable, appearance, min_instances, max_instances, **kwargs)
