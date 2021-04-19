"""
Empty: Default object, doesn't do anything special.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import PlayerEffects


class Empty(GenericObject):
    def __init__(self, **kwargs):
        name = "empty"
        effect = PlayerEffects.NONE
        traversable = True
        appearance = []
        min_instances = 10
        max_instances = 1000
        super().__init__(name, effect, traversable, appearance, min_instances, max_instances, **kwargs)
