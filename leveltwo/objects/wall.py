"""
Wall : the character can't go past this obstacle.
"""

from leveltwo.objects.generic import GenericObject
from leveltwo.enums.effects import Effects


class Wall(GenericObject):
    def __init__(self):
        name = "wall"
        effect = Effects.NONE
        traversable = False
        appearance = []
        min_instances = 4
        max_instances = 10
        super().__init__(name, effect, traversable, appearance, min_instances, max_instances)
