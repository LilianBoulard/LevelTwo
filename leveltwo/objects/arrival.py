"""
Arrival : ending point of a level.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import Effects


class ArrivalPoint(GenericObject):
    def __init__(self, **kwargs):
        name = "arrival"
        effect = Effects.LEVEL_FINISH
        traversable = True
        min_instances = 1
        max_instances = 1
        super().__init__(2, name, effect, traversable, min_instances, max_instances, **kwargs)
