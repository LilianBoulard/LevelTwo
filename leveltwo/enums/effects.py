"""
Lists effects that can be applied to the character.
"""

from enum import Enum


class LevelEffects(Enum):
    NONE = 0
    FINISH = 1
    STOP = 2


class PlayerEffects(Enum):
    NONE = 0
    SLOW = 1
    KILL = 2
