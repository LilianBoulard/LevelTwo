"""
Implements a generic object.
Must be inherited by all other objects.
"""

import numpy as np

from math import sqrt, floor
from typing import List, Tuple

from leveltwo.enums.effects import LevelEffects, PlayerEffects
from enum import Enum


class GenericObject:

    """
    Parameters
    ----------

    name: str
        The name of the object.

    effect: Enum
        One of the values contained from any of the enumerators from
        `leveltwo.enums.effects`.

    appearance: list
        A flattened `x * x` matrix.
        The system will automatically guess `x`,
        and will raise a `ValueError` if invalid.

    min_instances: int
        The minimum number of this object in any scene.
        Must be inferior or equal to `max_instances`.

    max_instances: int
        The maximum number of this object in any scene.
        Must be superior or equal to `min_instances`.

    Raises
    ------

    TypeError
        If the type of the variables are not passed as mentioned above.

    ValueError
        If appearance is not a `x * x` matrix (`x` being an integer).

    """

    def __init__(self,
                 name: str,
                 effect: Enum,
                 traversable: bool,
                 appearance: list,
                 min_instances: int,
                 max_instances: int,
                 **kwargs):

        # Check types are valid.
        if not isinstance(name, str) \
                or not (isinstance(effect, LevelEffects) or isinstance(effect, PlayerEffects)) \
                or not isinstance(traversable, bool) \
                or not isinstance(appearance, list) \
                or not isinstance(min_instances, int) \
                or not isinstance(max_instances, int):
            raise TypeError

        self.name = name
        self.effect = effect
        self.traversable = traversable
        self.appearance = appearance
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.sprite = self.read_sprite()

        # Setting additional arguments as attributes.
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    @classmethod
    def from_dbo(cls, dbo):
        """
        Takes a database object coming straight from SQLAlchemy,
        and creates a new generic object with its attributes.
        """
        obj = cls(
            name=dbo.name,
            effect=dbo,
            traversable=dbo.traversable,
            appearance=None, # TODO
            min_instances=dbo.min_instances,
            max_instances=dbo.max_instances
        )

    def read_sprite(self):
        pass
