from abc import ABC

from .base import MazeSolvingAlgorithm


class Manual(MazeSolvingAlgorithm, ABC):

    name = "manual"
