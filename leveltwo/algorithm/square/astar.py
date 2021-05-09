import heapq

from ..base import MazeSolvingAlgorithm
from ...object import GenericObject


class Cell:
    def __init__(self, x, y, traversable):
        self.x = x
        self.y = y
        self.traversable = traversable
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0


class Astar(MazeSolvingAlgorithm):

    name = "astar"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.s_x = self.level.content.shape[0]
        self.s_y = self.level.content.shape[1]
        self.start = Cell(self.level.get_starting_point_position()[0],
                          self.level.get_starting_point_position()[1],
                          traversable=True)
        self.end = Cell(self.level.get_arrival_point_position()[0],
                        self.level.get_arrival_point_position()[1],
                        traversable=True)
        for x, y in self.level.iterate_over_shape():
            cell: GenericObject = self.level.content[x, y]
            self.cells.append(Cell(x, y, traversable=cell.traversable))

    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end[0]) + abs(cell.x - self.end[1]))

    def get_cell(self, x, y):
        return self.cells[x * self.s_x + y]

    def get_adjacent(self, cell):
        cells = []
        if cell.x < self.s_y - 1:
            cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y - 1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.y < self.s_x:
            cells.append(self.get_cell(cell.x, cell.y + 1))
        return cells

    def update_cell(self, adj, cell):
        adj.g = 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def run_one_step(self):
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            f, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            if cell is self.end:
                print("END")
            adj_cells = self.get_adjacent(cell)
            for adj_cell in adj_cells:
                if adj_cell.traversable and adj_cell not in self.closed:
                    if(adj_cell.f, adj_cell) in self.opened:
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                else:
                    self.update_cell(adj_cell, cell)
                    heapq.heappush(self.opened, (adj_cell.f, adj_cell))
