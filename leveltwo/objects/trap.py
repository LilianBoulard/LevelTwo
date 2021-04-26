"""
Trap : Kills the player when walked on.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import Effects


class Trap(GenericObject):
    def __init__(self, **kwargs):
        name = "trap"
        effect = Effects.PLAYER_KILL
        traversable = True
        min_instances = 4
        max_instances = 10
        super().__init__(4, name, effect, traversable, min_instances, max_instances, **kwargs)
