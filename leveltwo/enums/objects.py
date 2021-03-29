from enum import Enum

from ..objects import StartingPoint, ArrivalPoint, Wall, Trap, Mud


class Objects(Enum):
    EMPTY = None
    START = StartingPoint
    ARRIVAL = ArrivalPoint
    WALL = Wall
    TRAP = Trap
    MUD = Mud
