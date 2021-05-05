import heapq

from ..base import MazeSolvingAlgorithm


class Astar(MazeSolvingAlgorithm):

    name = "astar"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = self.level.content
        self.s_x = self.level.content.shape[0]
        self.s_y = self.level.content.shape[1]
        self.start = self.level.get_starting_point_position()
        self.end = (9, 9)

    def get_heuristic(self, cell):
        return 10 * (abs(cell[0] - self.end[0]) + abs(cell[1] - self.end[1]))

    def get_cell(self, x, y):
        return self.cells[x * self.s_x + y]

    def get_adjacent(self, cell):
        cells = []
        if cell[0] < self.s_y - 1:
            cells.append(self.get_cell(cell[0] + 1, cell[1]))
        if cell[1] > 0:
            cells.append(self.get_cell(cell[0], cell[1] - 1))
        if cell.x > 0:
            cells.append(self.get_cell(cell[0] - 1, cell[1]))
        if cell.y < self.s_x:
            cells.append(self.get_cell(cell[0], cell[1]+ 1))
        return cells

    def update_cell(self, adj, cell):
        adj.g = 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def run_one_step(self):
        heapq.heappush(self.opened, (self.start[0], self.start))
        while len(self.opened):
            f, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            adj_cells = self.get_adjacent(cell)
            for adj_cell in adj_cells:
                if adj_cell == 4 and adj_cell not in self.closed:
                    if adj_cell > 10:
                        self.update_cell(adj_cell, cell)
                else:
                    self.update_cell(adj_cell, cell)
                    heapq.heappush(self.opened, (adj_cell.f, adj_cell))
