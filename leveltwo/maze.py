import pygame
import numpy as np

from typing import Tuple

from leveltwo.enums import Objects, Colors
from leveltwo.objects import StartingPoint, ArrivalPoint, Wall, Mud, Trap, Empty

pygame.init()
style = pygame.font.SysFont('calibri', 50)
label = pygame.font.SysFont('calibri', 20)

# Toolbox settings
toolbox_size = (200, 0)


class Cell:

    """
    Implements a `Cell`, which is a square in our maze.
    It acts as a block in which the character can move (one at a time),
    and in which an object can be placed.
    """

    def __init__(self, object_type: Objects):
        self.object_type: Objects = object_type
        self.origin_x = None
        self.origin_y = None
        self.end_x = None
        self.end_y = None

    def set_coordinates(self, origin_x: int, origin_y: int, end_x: int, end_y: int):
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
        return self.origin_x < x <= self.end_x and self.origin_y < y <= self.end_y

    def get_sprite(self):
        pass


class Maze:

    def __init__(self, parent_display, level):
        self.parent = parent_display
        self.level = level
        self.parent.screen_size = np.add(self.squarify(self.parent.screen_size), toolbox_size)
        self.maze_shape = self.level.content.shape
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.screen.fill(Colors.WHITE)  # Set the background color
        self.cells_coordinates_matrix = np.empty(self.level.content.shape)
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

    def init_grid(self) -> np.array:
        # Create an empty numpy array that will act as a matrix, in which we will store the cells.
        return np.empty(self.maze_shape, dtype='object')

    def get_z(self) -> int:
        """
        Computes `z`, which is the side length each cell has on the screen (in pixels).
        """
        # Using a round division might produce some unwanted pixel lines along the window's edges.
        # A later version might implement the auto-resizing of the window if
        # the standard division does not produce a round integer.
        grid_size = np.subtract(self.screen_size, toolbox_size)
        z = grid_size // self.maze_shape
        if z[0] != z[1]:
            raise RuntimeError(f'Could not create squared cells (got {z=}).')
        return z

    def draw_grid(self) -> None:
        """
        Constructs the maze's grid and draws rectangles for each cell on the screen.
        """
        z = self.get_z()
        rows, cols = self.cells_coordinates_matrix
        for i_x in range(rows):
            for i_y in range(cols):
                x = i_x * z
                y = i_y * z

                origin_x = x
                origin_y = y
                end_x = x + z
                end_y = y + z

                # Construct the matrix
                self.cells_coordinates_matrix[i_x, i_y] = [origin_x, origin_y, end_x, end_y]
                cell = self.level.content[i_x, i_y]
                # Draw the rectangle.
                rect = pygame.Rect(x, y, z, z)
                pygame.draw.rect(self.screen, cell.object_type.item_color, rect, width=1)

    def get_bounds(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Given two coordinates, `x` and `y`, constructs the coordinates of the square they land in.
        Example (with `self.get_z()` returning `10`):
        >>> self.get_bounds(4, 29)
        (0, 20, 10, 30)
        """
        z = self.get_z()
        x_remainder = x % z
        y_remainder = y % z
        x_lower = x - x_remainder
        y_lower = y - y_remainder
        x_upper = x_lower + z
        y_upper = y_lower + z
        bounds = (x_lower, y_lower, x_upper, y_upper)
        return bounds

    def get_clicked_cell_index(self, x: int, y: int) -> Tuple[int, ...]:
        """
        Iterates through the cells matrix and returns the one the user clicked on,
        based on the coordinates of his input.

        :param int x:
        :param int y:
        :return Tuple[int, ...]: The coordinates of the cell clicked on.
        """
        searching_for = self.get_bounds(x, y)
        cell_index = np.where((self.cells_coordinates_matrix == searching_for).all(axis=2))
        return tuple([int(c) for c in cell_index])


class MazeDisplay(Maze):

    def run(self) -> None:
        """
        Main loop.
        """
        self.draw_grid()
        while self._running:
            for event in pygame.event.get():
                # mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                # if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse was clicked.
                #     clicked_cell_coords = self.get_clicked_cell_index(mouse_x, mouse_y)
                if event.type == pygame.VIDEORESIZE:  # If the screen was resized.
                    self.resize(event.w, event.h)
            pygame.display.update()


class MazeEditable(Maze):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toolbar_items = [
            Empty(font_color=Colors.BLACK, item_color=Colors.WHITE),
            Trap(font_color=Colors.BLACK, item_color=Colors.BROWN),
            Wall(font_color=Colors.WHITE, item_color=Colors.BLACK),
            StartingPoint(font_color=Colors.BLACK, item_color=Colors.GREEN),
            ArrivalPoint(font_color=Colors.BLACK, item_color=Colors.RED),
            Mud(font_color=Colors.BLACK, item_color=Colors.BROWN),
        ]
        self.toolbar_buttons = {}

    def draw_toolbox(self) -> None:
        """
        Creates the toolbar's buttons from `self.toolbar_items`.
        """
        # Reset buttons
        self.toolbar_buttons = {}

        menu_label = label.render("ToolBox", True, Colors.BLACK)
        self.screen.blit(menu_label, (610, 5))
        indic_label = label.render("Click and set !", True, Colors.BLACK)
        self.screen.blit(indic_label, (570, 25))

        x = 610
        for i, item in enumerate(self.toolbar_items):
            y = (i + 1) * 50
            title = label.render(item.name, True, item.font_color)
            rectangle = pygame.Rect(x, y, title.get_width(), title.get_height())
            pygame.draw.rect(self.screen, item.item_color, rectangle)
            self.screen.blit(title, (x, y))

            self.toolbar_buttons.update({item.name: rectangle})

    def run(self) -> None:
        """
        Main loop.
        """

        self.draw_grid()
        selected_tool_index = 0  # Select the first item of the list as default (should be object `Empty`)
        while self._running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self._running = False
                    break

                if event.type == pygame.VIDEORESIZE:  # If the screen was resized.
                    self.resize(event.w, event.h)

                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 540 < mouse_x < 740 and 0 < mouse_y < 540:  # If in the toolbox area.
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for index, button in enumerate(self.toolbar_buttons.values()):
                            if button.collidepoint:
                                selected_tool_index = index
                                print(f'{selected_tool_index=}')

                if 0 < mouse_x < 540 and 0 < mouse_y < 540:  # If in the maze - grid - area.
                    if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse was clicked.
                        clicked_cell_coords = self.get_clicked_cell_index(mouse_x, mouse_y)
                        clicked_cell_bounds = self.cells_coordinates_matrix[clicked_cell_coords]
                        origin_x, origin_y, end_x, end_y = clicked_cell_bounds  # Unpack the values
                        # Get the horizontal and vertical length of the cell
                        horizontal_z = end_x - origin_x
                        vertical_z = end_y - origin_y

                        selected_object = self.toolbar_items[selected_tool_index]
                        # Set the cell's object in the level content
                        self.level.content[clicked_cell_coords].object_type = selected_object
                        rect = pygame.Rect(origin_x, origin_y, horizontal_z, vertical_z)
                        self.draw_grid()
                        # pygame.draw.rect(self.screen, Colors.BROWN, rect)
            pygame.display.update()
