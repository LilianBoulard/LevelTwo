"""
Lists effects that can be applied.
"""

from enum import Enum


class Effects(Enum):
    NONE = 0
    LEVEL_FINISH = 1
    PLAYER_STOP = 2
    PLAYER_SLOW = 3
    PLAYER_KILL = 4
