from abc import ABC

from .base import MazeSolvingAlgorithm


class Astar(MazeSolvingAlgorithm, ABC):

    name = "astar"
