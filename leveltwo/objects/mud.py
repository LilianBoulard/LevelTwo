"""
Mud : slows the character when walked on.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import Effects


class Mud(GenericObject):
    def __init__(self, **kwargs):
        name = "mud"
        effect = Effects.PLAYER_SLOW
        traversable = True
        min_instances = 4
        max_instances = 10
        super().__init__(5, name, effect, traversable, min_instances, max_instances, **kwargs)
