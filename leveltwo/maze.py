import pygame
import numpy as np

from typing import Tuple

from leveltwo.enums import Objects
from leveltwo.utils import calc_tuple

pygame.init()
style = pygame.font.SysFont('calibri', 50)

# Define colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BROWN = (165, 42, 42)

# Toolbox settings
toolbox_size = (200, 0)


class Cell:

    """
    Implements a `Cell`, which is a square in our maze.
    It acts as a block in which the character can move (one at a time),
    and in which an object can be placed.
    """

    def __init__(self, object_type: Objects, origin_x: int, origin_y: int, end_x: int, end_y: int):
        self.object_type: Objects = object_type
        self.origin_x: int = origin_x
        self.origin_y: int = origin_y
        self.end_x: int = end_x
        self.end_y: int = end_y

    def inside(self, x: int, y: int) -> bool:
        """
        Takes coordinates and returns whether they are located inside this cell perimeter.

        :param int x:
        :param int y:
        :return bool: True if they are, False otherwise.
        """
        return self.origin_x < x < self.end_x and self.origin_y < y < self.end_y

    def get_sprite(self):
        pass


class Maze:

    def __init__(self, parent_display, screen_size: Tuple[int, int], side_cells_count: int):
        self.parent = parent_display
        self.screen_size = calc_tuple(int.__add__, self.squarify(screen_size), toolbox_size)
        self.side_cells_count = side_cells_count
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.screen.fill(WHITE)  # Set the background color
        self._running = True
        pygame.display.set_caption("Level")

    def squarify(self, size: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        "squarifies" a tuple of integers.
        Example:
        >>> self.squarify((1920, 1080))
        (1080, 1080)
        """
        m = min(size)
        return tuple(m for _ in range(len(size)))

    def resize(self, x: int, y: int):
        """
        Resizes PyGame's window.
        """
        self.screen_size = (x, y)
        self.draw_grid()

    def draw_grid(self) -> np.array:
        """
        Constructs the maze's grid.
        """
        # Compute `z`, the size each cell has on the screen (number of pixels).
        # Using a round division might produce some unwanted pixel lines along the window's edges.
        # A further version might implement the auto-resizing of the window if
        # the standard division does not produce a round integer.
        grid_size = calc_tuple(int.__sub__, self.screen_size, toolbox_size)
        z = max(grid_size) // self.side_cells_count
        # Create a numpy array that will act as a matrix, in which we will store the cells.
        cells = np.empty((self.side_cells_count, self.side_cells_count), dtype='object')
        for i_x in range(self.side_cells_count):  # Along the x axis
            for i_y in range(self.side_cells_count):  # Along the y axis
                # Create the cell stored in this location.
                # This information is usually read from the database.
                x = i_x * z
                y = i_y * z
                cell = Cell(Objects.EMPTY,
                            origin_x=x,
                            origin_y=y,
                            end_x=x + z,
                            end_y=y + z,)
                # Add the cell to the matrix
                cells[i_x, i_y] = cell
                # Draw the rectangle.
                rect = pygame.Rect(x, y, z, z)
                pygame.draw.rect(self.screen, BLACK, rect, width=1)
        return cells

    def get_clicked_cell(self, x: int, y: int, cells: np.array) -> Cell or None:
        """
        Iterates through the cells matrix and returns the one the user clicked on,
        based on the coordinates of his input.

        :param int x:
        :param int y:
        :param np.array cells:
        :return Cell|None: A Cell if found, None otherwise.
        """
        for cell_row in cells:
            for cell in cell_row:
                if cell.inside(x, y):
                    return cell

    def run(self) -> None:
        """
        Main loop.
        """
        cells = self.draw_grid()
        while self._running:
            for event in pygame.event.get():
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse was clicked.
                    clicked_cell = self.get_clicked_cell(mouse_x, mouse_y, cells)
                    if not clicked_cell:
                        continue
                    print(vars(clicked_cell))
                if event.type == pygame.VIDEORESIZE:  # If the screen was resized.
                    self.resize(event.w, event.h)
            pygame.display.update()


class MazeDisplay(Maze):
    pass


class MazeEditable(Maze):

    def run(self) -> None:
        """
        Main loop.
        """
        cells = self.draw_grid()
        while self._running:
            for event in pygame.event.get():
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # If the mouse was clicked.
                    clicked_cell = self.get_clicked_cell(mouse_x, mouse_y, cells)
                    if not clicked_cell:
                        continue
                    print(vars(clicked_cell))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    clicked_cell = self.get_clicked_cell(mouse_x, mouse_y, cells)
                    if not clicked_cell:
                        continue
                    clicked_cell.object_type = Objects.TRAP
                    z = clicked_cell.end_x - clicked_cell.origin_x
                    rect = pygame.Rect(clicked_cell.origin_x, clicked_cell.origin_y, z, z)
                    pygame.draw.rect(self.screen, BROWN, rect, width=1)
                    print(vars(clicked_cell))
                if event.type == pygame.VIDEORESIZE:  # If the screen was resized.
                    self.resize(event.w, event.h)
            pygame.display.update()
