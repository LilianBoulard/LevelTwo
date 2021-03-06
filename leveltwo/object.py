"""
Implements a generic object.
Must be inherited by all other objects.
"""

import os

from enum import Enum
from PIL import Image

from .enums import Effects
from .database.models import ObjectDBO


objects_sprites_directory: str = "../sprites/"


class GenericObject:

    """
    Parameters
    ----------

    identifier: int
        The id of the object in the database.

    name: str
        The name of the object.

    effect: Enum
        One of the values contained from any of the enumerators from
        `leveltwo.enums.effects`.

    appearance: Image
        The picture corresponding to this object.

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
                 identifier: int,
                 name: str,
                 effect: Enum,
                 traversable: bool,
                 min_instances: int,
                 max_instances: int,
                 **kwargs):

        # Check types are valid.
        if not isinstance(name, str) \
                or not isinstance(identifier, int) \
                or not isinstance(effect, Effects) \
                or not isinstance(traversable, bool) \
                or not isinstance(min_instances, int) \
                or not isinstance(max_instances, int):
            raise TypeError

        self.identifier = identifier
        self.name = name
        self.effect = effect
        self.traversable = traversable
        self.min_instances = min_instances
        self.max_instances = max_instances

        # Setting additional arguments as attributes.
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    @classmethod
    def from_dbo(cls, dbo: ObjectDBO):
        """
        Takes a Object Database Object (ObjectsDBO, see `database/models.py`),
        and creates a new GenericObject instance from the information it contains.
        """
        identifier = dbo.id
        name = dbo.name
        effect = Effects(dbo.effect)
        traversable = dbo.traversable
        min_instances = dbo.min_instances
        max_instances = dbo.max_instances
        return cls(identifier, name, effect, traversable, min_instances, max_instances)

    def to_dbo(self) -> ObjectDBO:
        name = self.name
        effect = self.effect.value
        traversable = self.traversable
        min_instances = self.min_instances
        max_instances = self.max_instances
        return ObjectDBO(name, effect, traversable, min_instances, max_instances)
