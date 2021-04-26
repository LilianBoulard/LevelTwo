"""
Start : beginning point of a level.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import Effects


class StartingPoint(GenericObject):
    def __init__(self, **kwargs):
        name = "start"
        effect = Effects.NONE
        traversable = True
        min_instances = 1
        max_instances = 1
        super().__init__(1, name, effect, traversable, min_instances, max_instances, **kwargs)
