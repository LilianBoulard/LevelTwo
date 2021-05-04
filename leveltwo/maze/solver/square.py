import heapq

import pygame

from .base import MazeSolver

pygame.init()


class MazeSolverSquare(MazeSolver):
    step = 0
    def move_character(self, direction: int, amount: int = 1) -> None:
        """
        Changes the position of the character by `amount` cell(s) on a squared grid.

        :param int direction: Direction the character should move to.
                              Mapping:
                              0: up
                              1: left
                              2: down
                              3: right
        :param int amount: How many cells it will try to move. Default is 1.
        """
        if direction not in range(4):
            raise ValueError(f'Invalid direction {direction!r}, should be an integer between 0 and 3 included.')

        new_x, new_y = self.character.location

        for _ in range(amount):
            if direction == 0:
                new_y -= 1
            elif direction == 1:
                new_x -= 1
            elif direction == 2:
                new_y += 1
            elif direction == 3:
                new_x += 1

            # Check if new coords are in the available space
            max_x, max_y = self.level.content.shape
            if 0 <= new_x < max_x and 0 <= new_y < max_y:
                # Get the object which is on our path
                next_step_cell_object_id = self.level.content[new_x, new_y]
                next_step_cell_object = self.objects[next_step_cell_object_id - 1]
                # We remove one because objects are 1-indexed

                if next_step_cell_object.traversable:
                    self.character.move_and_handle_object_effect(new_x, new_y, next_step_cell_object)

    # Maze solving algorithms section

    def manual(self, event_key) -> None:
        inputs = {
            'up': pygame.key.key_code('Z'),
            'left': pygame.key.key_code('Q'),
            'down': pygame.key.key_code('S'),
            'right': pygame.key.key_code('D'),
        }

        if event_key == inputs['up']:
            # Go up
            self.move_character(0)
        elif event_key == inputs['left']:
            # Go left
            self.move_character(1)
        elif event_key == inputs['down']:
            # Go down
            self.move_character(2)
        elif event_key == inputs['right']:
            # Go right
            self.move_character(3)

    def breadth_first_search(self) -> None:
        pass

    def recursive_walk(self, x, y):
        if self.level.content[x][y] == 3:
            print('end %d,%d' % (x, y))
            return True
        elif self.level.content[x][y] == 4:
            print('wall %d,%d' % (x, y))
            return False
        elif self.level.content[x][y] == 7:
            print('visited %d,%d' % (x, y))
            return False
        print("empty")
        self.step+=1
        print(self.step)

        self.level.content[x][y] = 7
        if ((x < len(self.level.content) - 1 and self.recursive_walk(x + 1, y))
                or (y > 0 and self.recursive_walk(x, y - 1))
                or (x > 0 and self.recursive_walk(x - 1, y))
                or (y < len(self.level.content) - 1 and self.recursive_walk(x, y + 1))):
                return True
        return False

    # Astar Section
    def astar(self) -> None:
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.s_x, s_y = self.level.content.shape
        self.start = self.level.get_starting_point_position()
        self.end = self.level.get_ending_point_position()

    def heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

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
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            f, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            adj_cells = self.getadjacent(cell)
            for adj_cell in adj_cells:
                if adj_cell.trave and adj_cell not in self.closed:
                    if adj_cell.g > cell.g + 10:
                        self.update_cell(adj_cell, cell)
                else:
                    self.update_cell(adj_cell, cell)
                    heapq.heappush(self.opened, (adj_cell.f, adj_cell))
