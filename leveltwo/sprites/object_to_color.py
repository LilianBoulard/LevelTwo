from enum import Enum


class ObjectToColor(Enum):
    default = (0, 0, 0)
    empty = (255, 255, 255)
    startingpoint = (0, 127, 0)
    arrivalpoint = (0, 0, 127)
    wall = (127, 127, 127)
    mud = (222, 184, 135)
    trap = (127, 0, 0)
