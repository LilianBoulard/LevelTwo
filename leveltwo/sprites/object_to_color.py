from enum import Enum


class ObjectToColor(Enum):
    empty = (255, 255, 255)
    start = (0, 127, 0)
    arrival = (0, 0, 127)
    wall = (127, 127, 127)
    mud = (222, 184, 135)
    trap = (127, 0, 0)
