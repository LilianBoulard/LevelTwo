"""
Arrival : ending point of a level.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import LevelEffects


class ArrivalPoint(GenericObject):
    def __init__(self):
        name = "arrival"
        effect = LevelEffects.FINISH
        traversable = True
        appearance = []
        min_instances = 1
        max_instances = 1
        super().__init__(name, effect, traversable, appearance, min_instances, max_instances)
