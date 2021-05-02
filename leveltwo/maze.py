import pygame
import numpy as np

from typing import Tuple, Optional, Dict

from .enums import Colors
from .database import Database
from .level import GenericLevel
from .sprites.object_to_color import ObjectToColor

pygame.init()

bound_struct = Tuple[int, int, int, int]


class Viewport:

    def __init__(self, name, bounds: bound_struct):
        self.name = name
        self.bounds = bounds
        self.origin_x, self.origin_y, self.end_x, self.end_y = bounds

    def inside(self, x: int, y: int) -> bool:
        if self.origin_x < x < self.end_x and self.origin_y < y < self.end_y:
            return True
        else:
            return False


class Maze:

    def __init__(self, parent_display, level):
        self.parent = parent_display
        self.level: GenericLevel = level
        self.maze_shape = self.level.content.shape

        db = Database()
        self.objects = db.get_all_objects()

        self.cells_coordinates_matrix = np.empty((self.level.content.shape[0], self.level.content.shape[1], 4))
        self.viewports: Dict[str, Viewport] = {}

        self.screen_size = self.parent.screen_size
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.adjust_style()

        self._running: bool = True

    def get_selected_viewport(self, x: int, y: int) -> Viewport:
        """
        Given `x` and `y`, returns the name of the viewport the user clicked in.
        """
        for viewport in self.viewports.values():
            if viewport.inside(x, y):
                return viewport

        x, y, = self.screen_size
        return Viewport('outside', (0, 0, x, y))

    def resize(self, x: int, y: int):
        """
        Resize window.
        """
        self.screen_size = (x, y)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        pygame.display.set_caption(self.level.name)  # Set the window title
        self.draw_grid()
        self.adjust_style()

    def adjust_style(self) -> None:
        self.screen.fill(Colors.WHITE)  # Set the background color

    def init_grid(self) -> np.array:
        # Create an empty numpy array that will act as a matrix, in which we will store the cells.
        return np.empty(self.maze_shape, dtype='object')

    def get_z(self) -> Tuple[int, int]:
        """
        Computes `z`, which is the size each cell has on the screen (in pixels).
        """
        x = self.screen_size[0]
        y = self.screen_size[1]
        x_cells, y_cells = self.maze_shape

        # Calculate the maximum z on both axis.
        # Note: Using a round division might produce some unwanted margins around the edges,
        # So we calculate the new y and x, and resize the window to these later on.
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
            self.resize(new_x, new_y)

        return z, z

    def draw_grid(self) -> None:
        """
        Constructs the maze's grid and draws rectangles for each cell on the screen.
        """
        z = self.get_z()
        z_x, z_y = z
        # On the x and y axis, how many cells we want
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

        # Update viewport
        viewport_name = 'grid'
        viewport_end_x = z_x * s_x
        viewport_end_y = z_y * s_y
        grid_viewport = Viewport(viewport_name, (0, 0, viewport_end_x, viewport_end_y))
        self.viewports[viewport_name] = grid_viewport

    def get_bounds(self, x: int, y: int, z: Optional[Tuple[int, ...]] = None) -> bound_struct:
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

    def get_clicked_cell_index(self, x: int, y: int) -> Tuple[int, int]:
        """
        Iterates through the cells matrix and returns the coordinates of the
        one the user clicked on, based on the coordinates of his input.
        """
        searching_for = self.get_bounds(x, y)
        cell_index = np.where((self.cells_coordinates_matrix == searching_for).all(axis=2))
        return int(cell_index[0]), int(cell_index[1])


class MazeDisplay(Maze):

    def run(self) -> None:
        """
        Main loop.
        """
        self.draw_grid()
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.VIDEORESIZE:  # If the screen was resized.
                    self.resize(event.w, event.h)
            pygame.display.update()


class MazeEditable(Maze):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons_coordinates_matrix = np.empty((len(self.objects), 4))

    def draw(self):
        self.draw_grid()
        self.draw_toolbox()

    def resize(self, x: int, y: int):
        self.screen_size = (x, y)
        self.draw()
        self.adjust_style()

    def get_toolbox_buttons_size(self) -> Tuple[int, int]:
        button_width = 100
        button_height = button_width // 2
        return button_width, button_height

    def get_toolbox_margins(self) -> Tuple[int, int, int, int]:
        left_margin = 25
        top_margin = 0
        right_margin = 25
        bottom_margin = 0
        return left_margin, top_margin, right_margin, bottom_margin

    def draw_toolbox(self) -> None:
        """
        Creates the toolbar.
        """
        button_width, button_height = self.get_toolbox_buttons_size()
        left_margin, top_margin, right_margin, bottom_margin = self.get_toolbox_margins()

        total_side_length = left_margin + button_width + right_margin

        # Reset buttons coordinates matrix
        self.buttons_coordinates_matrix = np.empty((len(self.objects), 4))

        # Get toolbox viewport coordinates.
        # We want to stick this viewport to the right side of the grid.
        grid_viewport = self.viewports['grid']
        # Define this viewport
        viewport_name = 'toolbox'
        viewport_origin_x = grid_viewport.end_x
        viewport_origin_y = grid_viewport.origin_y
        viewport_end_x = grid_viewport.end_x + total_side_length
        viewport_end_y = grid_viewport.end_y
        # Update viewport
        toolbox_viewport = Viewport(
            viewport_name,
            (viewport_origin_x, viewport_origin_y, viewport_end_x, viewport_end_y)
        )
        self.viewports[viewport_name] = toolbox_viewport

        x = viewport_origin_x + left_margin

        # Add labels
        label = pygame.font.SysFont('calibri', 20)
        menu_label = label.render("ToolBox", True, Colors.BLACK)
        self.screen.blit(menu_label, (x, 5))

        for i, item in enumerate(self.objects):

            # Compute position on the vertical axis
            y = viewport_origin_y + (i + 1) * button_height

            # Display label for this item
            title = label.render(item.name, True, Colors.WHITE)
            # Draw the rectangle. We'll keep it in order to know when the user clicks on it.
            rectangle = pygame.Rect(x, y, button_width, title.get_height())
            color = ObjectToColor[item.name].value
            pygame.draw.rect(self.screen, color, rectangle)
            self.screen.blit(title, (x, y))

            # Get coordinates
            origin_x = x
            origin_y = y
            end_x = origin_x + button_width
            end_y = origin_y + button_height
            # And update the matrix
            self.buttons_coordinates_matrix[i] = np.array([origin_x, origin_y, end_x, end_y])

    def get_button_bounds(self, x: int, y: int, z: Tuple[int, int]) -> bound_struct:
        """
        Given `x` and `y` (coordinates), return a 4-tuple of integers
        delimiting the bounds of a toolbox button.
        """
        button_width, button_height = self.get_toolbox_buttons_size()
        left_margin, top_margin, _, _ = self.get_toolbox_margins()
        toolbox_viewport = self.viewports['toolbox']
        x_offset = toolbox_viewport.origin_x

        z_x, z_y = z

        remainder_x = x % x_offset % z_x
        remainder_y = y % z_y

        origin_x = x - remainder_x + left_margin
        origin_y = y - remainder_y + top_margin
        end_x = origin_x + button_width
        end_y = origin_y + button_height

        return origin_x, origin_y, end_x, end_y

    def get_clicked_button_index(self, x: int, y: int) -> Optional[int]:
        """
        Iterates through the buttons matrix and returns the one the user clicked on,
        based on the coordinates of his input.

        :param int x:
        :param int y:
        :return int: The index of the button clicked on.
        """
        b = self.get_toolbox_buttons_size()
        searching_for = self.get_button_bounds(x, y, z=b)
        cell_index = np.where((self.buttons_coordinates_matrix == searching_for).all(axis=1))
        print(x, y)
        print(b)
        print(searching_for)
        print(self.buttons_coordinates_matrix)
        print(cell_index)
        try:
            index = int(cell_index[0])
            return index
        except (TypeError, IndexError):
            return

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
                selected_viewport = self.get_selected_viewport(mouse_x, mouse_y)

                if selected_viewport.name == 'toolbox':  # If in the toolbox area.
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        idx = self.get_clicked_button_index(mouse_x, mouse_y)
                        if isinstance(idx, int):
                            selected_object = self.objects[idx]

                if selected_viewport.name == 'grid':  # If in the maze - grid - area.
                    if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse was clicked.
                        x, y = self.get_clicked_cell_index(mouse_x, mouse_y)

                        # Set the cell's object in the level content if within limits.
                        self.level.set_cell_object(x, y, selected_object)
                        self.draw()

            pygame.display.update()
