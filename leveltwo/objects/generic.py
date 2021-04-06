"""
Implements a generic object.
Must be inherited by all other objects.
"""

import numpy as np

from math import sqrt, floor
from typing import List, Tuple

from leveltwo.enums.effects import LevelEffects, PlayerEffects
from enum import Enum


sprite_struct = List[Tuple[int, int, int, int]]
sprite_sep = ', '  # Separator


def read_sprite(sprite: str) -> sprite_struct:
    """
    Takes a sprite serialized as a string, and returns a list of tuples (pixels).
    :param str sprite:
    :return sprite_struct:
    """
    sprite_list = sprite.split(sprite_sep)
    # We check if the remainder of the modulo by 4 is 0.
    # 4 because we have 4 values per pixel: Red, Green, Blue, Alpha.
    # See `docs/sprite_data_representation.md`.
    if not len(sprite_list) % 4 == 0:
        raise ValueError("Sprite's length should be divisible by 4.")

    # Then, we group the values to get the list of pixels.
    pixels: sprite_struct = []
    offset = 0
    for _ in range(len(sprite_list) // 4):
        r, g, b, a = [int(i) for i in sprite_list[offset:offset + 4]]
        pixels.append((r, g, b, a))
        offset += 4

    return pixels


def serialize_sprite(sprite: sprite_struct) -> str:
    flat_pixels: List[str] = []
    for pixel in sprite:
        flat_pixel = sprite_sep.join([str(v) for v in pixel])
        flat_pixels.append(flat_pixel)

    # Or as a comprehension:
    # return sprite_sep.join([sprite_sep.join([str(v) for v in pixel]) for pixel in I])

    return sprite_sep.join(flat_pixels)


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
        guessed_x = floor(sqrt(len(self.appearance)))
        computed_size = guessed_x ** 2
        if computed_size != len(self.appearance):
            raise ValueError(f"Invalid size found: computed {computed_size}, expected {len(self.appearance)}")
        array = np.array(self.appearance)  # Convert to numpy array.
        array.resize((guessed_x, guessed_x))  # Resize to a 2D matrix.
        return array
