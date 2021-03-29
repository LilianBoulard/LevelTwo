"""
Implements a generic object.
Must be inherited by all other objects.
"""

import numpy as np

from math import sqrt

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
        If appearance is not a `x * x` matrix (x being an integer).

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
        self.sprite = self._compute_sprite()

    def _compute_sprite(self) -> np.array:
        guessed_x = int(sqrt(len(self.appearance)))
        computed_size = guessed_x ** 2
        if computed_size != len(self.appearance):
            raise ValueError(f"Invalid size found: computed {computed_size}, expected {len(self.appearance)}")
        array = np.array(self.appearance)  # Convert to numpy array.
        array.resize((guessed_x, guessed_x))  # Resize to a 2D matrix.
        return array
