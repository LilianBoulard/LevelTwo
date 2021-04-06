import pygame
import numpy as np

from leveltwo.enums import Objects

pygame.init()
style = pygame.font.SysFont('calibri', 50)

# Define colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)


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

    def __init__(self, parent_display, screen_size: int, side_cells_count: int):
        self.parent = parent_display
        self.screen_size = screen_size
        self.side_cells_count = side_cells_count
        self.screen = pygame.display.set_mode((screen_size, screen_size), pygame.RESIZABLE)
        self.screen.fill(WHITE)  # Set the background color
        self._running = True
        pygame.display.set_caption("Level")

    def resize(self, x: int, y: int):
        self.screen_size = max(x, y)
        self.draw_grid()

    def draw_grid(self) -> np.array:
        """
        Constructs the maze's grid.
        """
        # Compute the size each cell has on the screen (number of pixels).
        # Using a round division might produce some unwanted pixel lines along the window's edges.
        # A further version might implement the auto-resizing of the window if
        # the standard division does not produce a round integer.
        z = self.screen_size // self.side_cells_count
        # Create a numpy array that will act as a matrix, in which we will store the cells.
        cells = np.empty((self.side_cells_count, self.side_cells_count), dtype='object')
        for i_x, x in enumerate(range(0, self.screen_size, z)):  # Along the x axis
            for i_y, y in enumerate(range(0, self.screen_size, z)):  # Along the y axis
                # Create the cell stored in this location.
                # This information is usually read from the database.
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
