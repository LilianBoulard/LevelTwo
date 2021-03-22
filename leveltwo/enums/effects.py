"""
Lists effects that can be applied to the character.
"""

from enum import Enum


class Effects(Enum):
    NONE = 0
    SLOW = 1
    FINISH = 2
    STOP = 3
    KILL = 4
