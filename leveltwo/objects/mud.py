"""
Mud : slows the character when walked on.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import PlayerEffects


class Mud(GenericObject):
    def __init__(self):
        name = "mud"
        effect = PlayerEffects.SLOW
        traversable = True
        appearance = []
        min_instances = 4
        max_instances = 10
        super().__init__(name, effect, traversable, appearance, min_instances, max_instances)
