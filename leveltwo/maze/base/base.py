from typing import Tuple

BoundType = Tuple[int, int, int, int]


class Viewport:

    def __init__(self, name, bounds: BoundType):
        self.name = name
        self.bounds = bounds
        self.origin_x, self.origin_y, self.end_x, self.end_y = bounds

    def inside(self, x: int, y: int) -> bool:
        if self.origin_x < x < self.end_x and self.origin_y < y < self.end_y:
            return True
        else:
            return False
