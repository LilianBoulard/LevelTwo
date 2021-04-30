import pygame
import numpy as np

from typing import Tuple, Optional, Dict

from .sprites.object_to_color import ObjectToColor
from .database import Database
from .enums import Colors

pygame.init()
style = pygame.font.SysFont('calibri', 50)
label = pygame.font.SysFont('calibri', 20)

# Toolbox settings
toolbox_size = (200, 0)


class Maze:

    def __init__(self, parent_display, level):
        db = Database()
        self.objects = db.get_all_objects()
        self.parent = parent_display
        self.level = level
        self.maze_shape = self.level.content.shape
        self.screen = pygame.display.set_mode(self.parent.screen_size, pygame.RESIZABLE)
        self.screen.fill(Colors.WHITE)  # Set the background color
        self.cells_coordinates_matrix = np.empty((self.level.content.shape[0], self.level.content.shape[1], 4))
        self._running = True
        self.viewports: Dict[str, Tuple[int, int, int, int]] = {}
        pygame.display.set_caption("Level")

    def resize(self, x: int, y: int):
        """
        Resizes PyGame's window.
        """
        self.parent.screen_size = (x, y)

    def init_grid(self) -> np.array:
        # Create an empty numpy array that will act as a matrix, in which we will store the cells.
        return np.empty(self.maze_shape, dtype='object')

    def get_z(self) -> Tuple[int, int]:
        """
        Computes `z`, which is the side length each cell has on the screen (in pixels).
        """
        x = self.parent.screen_size[0]
        y = self.parent.screen_size[1]
        x_cells, y_cells = self.maze_shape

        # Calculate the maximum z on both axis
        # Note: Using a round division might produce some unwanted margins around the edges.
        # A later version might implement the auto-resizing of the window if
        # the standard division does not produce a round integer.
        calculated_z_x = x // x_cells
        calculated_z_y = y // y_cells

        # Check if projecting each z on the other axis works.
        # If it doesn't for one, return the other.
        # If it does for both, return the largest.
        if calculated_z_x * y_cells > y:
            z = calculated_z_y
        elif calculated_z_y * x_cells > x:
            z = calculated_z_x
        else:
            z = max(calculated_z_x, calculated_z_y)

        remainder_x = x - (x_cells * z)
        remainder_y = y - (y_cells * z)

        if remainder_x > 0 or remainder_y > 0:
            new_x = x - remainder_x
            new_y = y - remainder_y
            print(f'{new_x=}, {new_y=}')
            self.resize(new_x, new_y)

        return z, z

    def draw_grid(self) -> None:
        """
        Constructs the maze's grid and draws rectangles for each cell on the screen.
        """
        z = self.get_z()
        z_x, z_y = z
        s_x, s_y = self.level.content.shape
        for i_x in range(s_x):
            for i_y in range(s_y):
                x = i_x * z_x
                y = i_y * z_y

                origin_x = x
                origin_y = y
                end_x = x + z_x
                end_y = y + z_y

                self.cells_coordinates_matrix[i_x, i_y] = np.array([origin_x, origin_y, end_x, end_y])
                cell = self.level.content[i_x, i_y] - 1  # objects are 1-indexed in the level content
                # Draw the rectangle.
                rect = pygame.Rect(x, y, z_x, z_y)
                color = ObjectToColor[self.objects[cell].name].value
                pygame.draw.rect(self.screen, color, rect)
        grid_size = (z_x * s_x, z_y * s_y)

    def get_bounds(self, x: int, y: int, z: Optional[Tuple[int, ...]] = None) -> Tuple[int, int, int, int]:
        """
        Given two coordinates, `x` and `y`, returns the bounds of the square they land in.
        Example (with `self.get_z()` returning `10`):
        >>> self.get_bounds(4, 29)
        (0, 20, 10, 30)
        """
        if z is None:
            z = self.get_z()
        z_x, z_y = z

        x_remainder = x % z_x
        y_remainder = y % z_y

        x_lower = x - x_remainder
        y_lower = y - y_remainder

        x_upper = x_lower + z_x
        y_upper = y_lower + z_y

        bounds = (x_lower, y_lower, x_upper, y_upper)

        return bounds

    def get_clicked_cell_index(self, x: int, y: int) -> Tuple[int, ...]:
        """
        Iterates through the cells matrix and returns the coordinates of the
        one the user clicked on, based on the coordinates of his input.
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

    toolbar_button_width = 200
    toolbar_button_height = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent.screen_size = np.add(self.parent.screen_size, toolbox_size)
        self.toolbar_x_offset = 610
        self.buttons_coordinates_matrix = np.empty((len(self.objects), 4))

    def draw(self):
        print(self.level.content)
        self.draw_grid()
        self.draw_toolbox()

    def draw_toolbox(self) -> None:
        """
        Creates the toolbar's buttons from `self.toolbar_items`.
        """
        # Reset buttons coordinates matrix
        self.buttons_coordinates_matrix = np.empty((len(self.objects), 4))

        # Add labels
        menu_label = label.render("ToolBox", True, Colors.BLACK)
        self.screen.blit(menu_label, (610, 5))

        x = self.toolbar_x_offset  # Watch out !!!
        for i, item in enumerate(self.objects):

            # Compute position on the vertical axis
            y = (i + 1) * self.toolbar_button_height

            # Display label for this item
            title = label.render(item.name, True, Colors.WHITE)
            # Draw the rectangle. We'll keep it in order to know when the user clicks on it.
            rectangle = pygame.Rect(x, y, self.toolbar_button_width, title.get_height())
            color = ObjectToColor[item.name].value
            pygame.draw.rect(self.screen, color, rectangle)
            self.screen.blit(title, (x, y))

            # Get coordinates
            origin_x = x
            origin_y = y
            end_x = origin_x + self.toolbar_button_width
            end_y = origin_y + self.toolbar_button_height
            # And update the matrix
            self.buttons_coordinates_matrix[i] = np.array([origin_x, origin_y, end_x, end_y])

    def get_button_bounds(self, x: int, y: int, z: Tuple[int, int]) -> Tuple[int, int, int, int]:
        """
        Given `x` and `y` (coordinates), return a 4-tuple of integers
        delimiting the bounds of a toolbox button.
        """
        z_x, z_y = z

        remainder_x = x % self.toolbar_x_offset % z_x
        remainder_y = y % z_y

        origin_x = x - remainder_x
        origin_y = y - remainder_y
        end_x = origin_x + self.toolbar_button_width
        end_y = origin_y + self.toolbar_button_height

        return origin_x, origin_y, end_x, end_y

    def get_clicked_button_index(self, x: int, y: int) -> int:
        """
        Iterates through the buttons matrix and returns the one the user clicked on,
        based on the coordinates of his input.

        :param int x:
        :param int y:
        :return int: The index of the button clicked on.
        """
        searching_for = self.get_button_bounds(x, y, z=(self.toolbar_button_width, self.toolbar_button_height))
        cell_index = np.where((self.buttons_coordinates_matrix == searching_for).all(axis=1))
        return int(cell_index[0])

    def run(self) -> None:
        """
        Main loop.
        """
        self.draw()
        # Select the first item of the list as default (should be object `Empty`)
        selected_object = self.objects[0]
        while self._running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self._running = False
                    break

                if event.type == pygame.VIDEORESIZE:  # If the screen was resized.
                    self.resize(event.w, event.h)
                    self.draw()

                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 540 < mouse_x < 740 and 0 < mouse_y < 540:  # If in the toolbox area.
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        idx = self.get_clicked_button_index(mouse_x, mouse_y)
                        selected_object = self.objects[idx]
                        print(f'New selected object {selected_object.name, selected_object.identifier}')

                if 0 < mouse_x < 540 and 0 < mouse_y < 540:  # If in the maze - grid - area.
                    if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse was clicked.
                        clicked_cell_coords = self.get_clicked_cell_index(mouse_x, mouse_y)
                        clicked_cell_bounds = self.cells_coordinates_matrix[clicked_cell_coords]
                        origin_x, origin_y, end_x, end_y = clicked_cell_bounds  # Unpack the values
                        # Get the horizontal and vertical length of the cell
                        horizontal_z = end_x - origin_x
                        vertical_z = end_y - origin_y

                        # Set the cell's object in the level content
                        self.level.content[clicked_cell_coords] = selected_object.identifier
                        self.draw()

                pygame.display.update()
