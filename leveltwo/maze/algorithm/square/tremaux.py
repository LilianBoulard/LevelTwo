from tkinter import Tk
from tkinter import messagebox
from typing import List, Tuple

from ..base import Tremaux, Deadend, Visited
from ....object import GenericObject
from ....database.init.default_objects import Wall


class TremauxSquare(Tremaux):

    def run_one_step(self) -> None:
        x, y = current_cell = self.character.location

        # Coordinates
        up_cell_pos = x, y - 1
        left_cell_pos = x - 1, y
        down_cell_pos = x, y + 1
        right_cell_pos = x + 1, y

        # GenericObjects
        # As it will try at some point to gather cells outside the bounds of the maze,
        # We'll have to mark the missing cells as walls.
        try:
            up_cell = (self.level.object_map[up_cell_pos], up_cell_pos)
        except IndexError:
            up_cell = (Wall(), up_cell_pos)
        try:
            left_cell = (self.level.object_map[left_cell_pos], left_cell_pos)
        except IndexError:
            left_cell = (Wall(), left_cell_pos)
        try:
            down_cell = (self.level.object_map[down_cell_pos], down_cell_pos)
        except IndexError:
            down_cell = (Wall(), down_cell_pos)
        try:
            right_cell = (self.level.object_map[right_cell_pos], right_cell_pos)
        except IndexError:
            right_cell = (Wall(), right_cell_pos)

        adjacent_cells = [up_cell, left_cell, down_cell, right_cell]

        available_cells: List[Tuple[GenericObject, Tuple[int, int]]] = [(obj, pos) for obj, pos in adjacent_cells if obj.traversable]

        max_x, max_y = self.level.content.shape
        traversable_cells = [(obj, (x, y)) for obj, (x, y) in available_cells if 0 <= x < max_x and 0 <= y < max_y]

        # Set priorities
        # We will try to move to the cell with the lowest value assigned
        valid_cells = {
            0: 'arrivalpoint',
            1: 'empty',
            2: 'mud',
            3: 'visited'
        }

        # Next, replace the objects by their priority
        cells = []
        for priority, associated_name in valid_cells.items():
            for obj, pos in traversable_cells:
                if obj.name == associated_name:
                    cells.append((priority, pos))

        if len(cells) == 0:
            # We've explored the whole maze, and didn't find an arrival point.
            self._running = False

        # If we have 3 non-traversable cells around us, we signal this cell as a deadend,
        # and we go the only way available.
        if len(cells) == 1:
            # Mark as deadend
            deadend_object = Deadend.from_existing(self.level.object_map[current_cell])
            self.level.object_map[current_cell] = deadend_object

        if len(cells) == 2:
            # We're in a corridor
            pass

        if len(cells) == 3 or len(cells) == 4:
            # We're at an intersection.
            pass

        # Soft by priority, lowest first
        cells.sort(key=lambda x: x[0])

        # cells[0] selects the first cell
        # [1] selects only the cell's coordinates
        try:
            next_cell: Tuple[int, int] = cells[0][1]
        except IndexError:
            # We could not find any resolution to the maze.
            Tk().wm_withdraw()
            messagebox.showwarning('No solution !', f'Could not find any solution to the maze !')
            self._running = False
            return

        next_cell_object: GenericObject = self.level.object_map[next_cell]

        # As we are about to leave this cell, we mark it as visited.
        # Only applicable if not already a dead end.
        current_cell_object: GenericObject = self.level.object_map[current_cell]
        if current_cell_object.name != 'deadend':
            visited_object = Visited.from_existing(self.level.object_map[current_cell])
            self.level.object_map[current_cell] = visited_object

        # Move to the next cell
        next_cell_x, next_cell_y = next_cell
        self.character.move_and_handle_object_effect(next_cell_x, next_cell_y, next_cell_object)

        # If it's the finish object, we'll mark ourself as done.
        if next_cell_object.name == 'arrivalpoint':
            self._running = False
