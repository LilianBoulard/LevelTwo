from abc import ABC

import pygame
import numpy as np

from tkinter import Tk
from tkinter import messagebox

from time import sleep
from datetime import datetime
from typing import Tuple, Optional, Dict, List

from ..test import Test
from ..enums import Colors
from ..database import Database
from ..level import GenericLevel
from ..character import Character
from ..sprites.object_to_color import ObjectToColor
from .algorithm.base import MazeSolvingAlgorithm, Manual

BoundType = Tuple[int, int, int, int]


class Viewport:

    def __init__(self, name, bounds: BoundType):
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

        db = Database()
        self.objects = db.get_all_objects()

        self.cells_coordinates_matrix = self.init_cell_coordinates_matrix()
        self.viewports: Dict[str, Viewport] = {}

        self.screen_size = self.parent.screen_size
        self.screen = self.get_screen()
        self.adjust_style()

        self._running: bool = True

    def get_screen(self):
        return pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

    def get_selected_viewport(self, x: int, y: int) -> Viewport:
        """
        Given `x` and `y`, returns the viewport the user clicked in.
        """
        for viewport in self.viewports.values():
            if viewport.inside(x, y):
                return viewport

        # Create dummy viewport that spans the entire window.
        max_x, max_y, = self.screen_size
        return Viewport('outside', (0, 0, max_x, max_y))

    def resize(self, x: int, y: int, callback) -> None:
        """
        Resize window.

        :param int x: New size on the `x` axis
        :param int y: New size on the `y` axis
        :param callback: Function to call once the resizing has been performed.
        """
        self.screen_size = (x, y)
        self.screen = self.get_screen()
        pygame.display.set_caption(self.level.name)  # Set the window title
        self.adjust_style()
        callback()

    def adjust_style(self) -> None:
        self.screen.fill(Colors.WHITE)  # Set the background color

    def init_cell_coordinates_matrix(self) -> np.array:
        raise NotImplementedError()

    def get_z(self) -> Tuple[int, int]:
        raise NotImplementedError()

    def draw_grid(self) -> None:
        """
        Constructs the maze's grid and draws rectangles for each cell on the screen.
        """
        raise NotImplementedError()

    def adjust_screen(self, callback, *, down_margin: int = 0, right_margin: int = 0) -> None:
        """
        Calculates the size each viewport should have on the screen,
        and resize the window accordingly.
        """
        x, y = self.screen_size
        z_x, z_y = self.get_z()

        x_cells, y_cells = self.level.content.shape

        remainder_x = x - (x_cells * z_x) - right_margin
        remainder_y = y - (y_cells * z_y) - down_margin

        if remainder_x > 0 or remainder_y > 0:
            new_x = x - remainder_x
            new_y = y - remainder_y
            self.resize(new_x, new_y, callback)

    def get_bounds(self, x: int, y: int, z: Optional[Tuple[int, ...]] = None) -> BoundType:
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

    def get_cell_center(self, x: int, y: int) -> Tuple[int, int]:
        raise NotImplementedError()


class MazeEditable(Maze, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons_coordinates_matrix = np.empty((len(self.objects), 4))
        self.manipulation_buttons: Dict[str, pygame.Rect] = {}

    def draw(self):
        self.draw_grid()
        self.draw_toolbox()

        toolbox_vp = self.viewports['toolbox']
        toolbox_width = toolbox_vp.end_x - toolbox_vp.origin_x
        self.adjust_screen(self.draw, right_margin=toolbox_width)

        pygame.display.update()

    def get_toolbox_buttons_size(self) -> Tuple[int, int]:
        button_width = 100
        button_height = button_width // 2
        return button_width, button_height

    def get_toolbox_margins(self) -> Tuple[int, int, int, int]:
        left_margin = 50
        top_margin = 0
        right_margin = 50
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

        # Starting from the window lower edge, we'll display the labels up `n` pixels
        n = 100
        manipulation_labels_y = viewport_end_y - n

        save_label = label.render("Save", True, Colors.BLACK)
        save_label_x = x
        # Display label
        save_button = self.screen.blit(save_label, (save_label_x, manipulation_labels_y))
        # And add the button to the manipulation buttons list.
        # We'll use the method `collidepoint` on it.
        self.manipulation_buttons.update({'save': save_button})

        cancel_label = label.render("Cancel", True, Colors.BLACK)
        cancel_label_x = viewport_end_x - cancel_label.get_width() - right_margin
        cancel_button = self.screen.blit(cancel_label, (cancel_label_x, manipulation_labels_y))
        self.manipulation_buttons.update({'cancel': cancel_button})

    def get_button_bounds(self, x: int, y: int, z: Tuple[int, int]) -> BoundType:
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
        try:
            index = int(cell_index[0])
            return index
        except (TypeError, IndexError):
            return

    def save(self) -> None:
        anomalies = self.level.get_objects_occurrences_anomalies(self.objects)
        if len(anomalies) == 0:
            db = Database()
            db.update_level_content(self.level)
            self._running = False

        else:
            # Add popup to signal the issue
            Tk().wm_withdraw()
            formatted_anomalies = '\n'.join(
                [
                    f"{v['min']} < {object_name} ({v['current']}) < {v['max']}"
                    for object_name, v in anomalies.items()
                ]
            )
            messagebox.showwarning('Anomalies', f'Got errors: \n{formatted_anomalies}')
            pass

    def cancel(self) -> None:
        self._running = False


class MazePlayable(Maze, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        starting_point_location = self.level.get_starting_point_position()
        self.character = Character(*starting_point_location)
        self.db = Database()
        objects = self.db.get_all_objects()
        self.level.set_objects(objects)

    def draw(self) -> None:
        self.adjust_screen(self.draw)
        self.draw_grid()
        self.draw_character()
        pygame.display.update()

    def rerun(self, test: Test, delay: int = 0.5) -> None:
        """
        Takes a test, and runs it so as to visualize the steps the algorithm took.
        :param Test test: the test to run
        :param int delay: how long we should wait before displaying each step.
        """

        def draw_path():
            for line in path:
                pygame.draw.line(self.screen, Colors.BLACK, *line)

        self.draw()
        path: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

        delay = int(delay * 1000)  # Convert delay to milliseconds
        last_step = test.steps[0]
        for step in test.steps:
            pygame.time.delay(delay)  # Wait

            # Get the centers of this step and the last
            cell_x, cell_y = step
            cell_center_x, cell_center_y = self.get_cell_center(cell_x, cell_y)
            last_cell_x, last_cell_y = last_step
            last_step_center_x, last_step_center_y = self.get_cell_center(last_cell_x, last_cell_y)

            # Move the character
            self.character.move(cell_x, cell_y)

            # And add a line between the two.
            path.append(((cell_center_x, cell_center_y), (last_step_center_x, last_step_center_y)))

            last_step = step

            self.draw()
            draw_path()
            pygame.display.update()

        pygame.time.delay(800)

    def run(self, algorithm_class) -> None:
        """
        Main loop.
        """
        save: bool = False
        algo: MazeSolvingAlgorithm = algorithm_class(self.level, self.character)
        manual: bool = isinstance(algo, Manual)

        self.draw()
        while self._running:
            key = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h, self.draw)
                if manual:
                    # If on manual mode (human-controller)
                    if event.type == pygame.KEYDOWN:
                        key = event.key

            # Keyword arguments to pass to the algorithm iteration.
            kwargs = {}

            if isinstance(algo, Manual):
                kwargs.update({
                    'key': key
                })

            # If not human-controller, advance the algorithm one step.
            algo.run_one_step(**kwargs)
            self.draw()
            if not algo.is_running():
                save = True
                self._running = False

            if not manual:
                sleep(0.2)

            pygame.display.update()

        if save:
            # If we finished the level one way or another, we'll save the run in the database.
            test = Test(identifier=None,
                        level_id=self.level.identifier,
                        algorithm=algo.name,
                        steps=self.character.path,
                        run_date=datetime.now())
            self.db.store_test(test)
