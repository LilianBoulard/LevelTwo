"""

This files contains common variables used across the project.

"""

from typing import List, Tuple


class Config:

    project_name: str = "LevelTwo"

    pathfinding_algorithms: List[Tuple[str, int]] = [
        ('None', 0),
        ('A*', 1),
    ]
