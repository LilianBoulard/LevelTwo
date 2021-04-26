"""
Wall : the character can't go past this obstacle.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import Effects


class Wall(GenericObject):
    def __init__(self, **kwargs):
        name = "wall"
        effect = Effects.PLAYER_STOP
        traversable = False
        min_instances = 4
        max_instances = 10
        super().__init__(3, name, effect, traversable, min_instances, max_instances, **kwargs)
