import heapq
import logging
import time
from ..base import Astar


from ...object import GenericObject


class Cell:
    def __init__(self, x, y, traversable):
        self.traversable = traversable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


class AstarSquare(Astar):

    name = "astar"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.s_x, self.s_y = self.level.content.shape
        start_x, start_y = self.level.get_starting_point_position()
        self.start = Cell(start_x, start_y, traversable=True)
        end_x, end_y = self.level.get_arrival_point_position()
        self.end = Cell(end_x, end_y, traversable=True)
        for x, y in self.level.iterate_over_shape():
            cell: GenericObject = self.level.object_map[x, y]
            self.cells.append(Cell(x, y, traversable=cell.traversable))

    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        return self.cells[x * self.s_y + y]

    def get_adjacent(self, cell):
        cells = []
        if cell.x < self.s_x - 1:
            cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y - 1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.y < self.s_y - 1:
            cells.append(self.get_cell(cell.x, cell.y + 1))
        return cells

    def display_path(self, cell=Cell):
        cell = self.end
        print(cell.x)
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def run_one_step(self):
        heapq.heappush(self.opened, (self.start.f, self.start))
        f, cell = heapq.heappop(self.opened)
        self.closed.add(cell)
        if cell.x == self.end.x:
            if cell.y == self.end.y:
                print("end")
                self._running = False
        adj_cells = self.get_adjacent(cell)
        for adj_cell in adj_cells:
            if adj_cell.traversable and adj_cell not in self.closed:
                if (adj_cell.f, adj_cell) in self.opened:
                    if adj_cell.g > cell.g + 10:
                        self.update_cell(adj_cell, cell)
                else:
                    self.update_cell(adj_cell, cell)
                    print(cell.x, cell.y)
                    time.sleep(1)
                    heapq.heappush(self.opened, (adj_cell.f, adj_cell))
        next_cell_object: GenericObject = self.level.object_map[cell.x, cell.y]
        self.character.move_and_handle_object_effect(cell.x, cell.y, next_cell_object)


