"""
Trap : Kills the player when walked on.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import Effects


class Trap(GenericObject):
    def __init__(self):
        name = "trap"
        effect = Effects.KILL
        traversable = True
        appearance = []
        min_instances = 4
        max_instances = 10
        super().__init__(name, effect, traversable, appearance, min_instances, max_instances)
