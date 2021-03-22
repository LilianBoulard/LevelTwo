"""
Implements a generic object.
Must be inherited by all other objects.
"""

from enum import Enum


class GenericObject:

    """
    Parameters
    ----------

    name: str
        The name of the object.

    effect: Enum
        One of the values contained in the enumerator
        `leveltwo.enums.effects.Effects`.

    appearance: list
        A flattened `x * x` matrix.
        The system will automatically try to guess `x`,
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

    """

    def __init__(self,
                 name: str,
                 effect: Enum,
                 traversable: bool,
                 appearance: list,
                 min_instances: int,
                 max_instances: int):

        # Check types are valid.
        if not isinstance(name, str) \
                or not isinstance(effect, Enum) \
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
