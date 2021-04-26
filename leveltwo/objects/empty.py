"""
Empty: Default object, doesn't do anything special.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import Effects


class Empty(GenericObject):
    def __init__(self, **kwargs):
        name = "empty"
        effect = Effects.NONE
        traversable = True
        min_instances = 10
        max_instances = 1000
        super().__init__(0, name, effect, traversable, min_instances, max_instances, **kwargs)
