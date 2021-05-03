import pygame
import numpy as np
from tkinter import *
from tkinter import messagebox

from typing import Tuple, Optional, Dict

from .base import Maze, Viewport, BoundType

from ..enums import Colors
from ..database import Database
from ..sprites.object_to_color import ObjectToColor

pygame.init()


class MazeEditable(Maze):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons_coordinates_matrix = np.empty((len(self.objects), 4))
        self.manipulation_buttons: Dict[str, pygame.Rect] = {}

    def draw(self):
        self.draw_grid()
        self.draw_toolbox()

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
        cancel_label_x = x + save_label.get_width() + left_margin
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
        all_objects_in_bounds: bool = all(
            [
                self.level.is_object_occurrences_in_limits(obj)
                for obj in self.objects
            ]
        )
        if all_objects_in_bounds:
            db = Database()
            db.update_level_content(self.level)
            self._running = False

        else:
            # Add popup to signal the issue
            Tk().wm_withdraw()  # to hide the main window
            messagebox.showwarning('WARNING', 'Please add a starting point')
            pass

    def cancel(self) -> None:
        self._running = False

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
                    self.resize(event.w, event.h, self.draw())
                    self.draw()

                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_viewport = self.get_selected_viewport(mouse_x, mouse_y)

                if selected_viewport.name == 'toolbox':  # If in the toolbox area.
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        for label, button in self.manipulation_buttons.items():
                            if button.collidepoint(mouse_x, mouse_y):
                                if label == 'save':
                                    self.save()
                                elif label == 'cancel':
                                    self.cancel()

                        idx = self.get_clicked_button_index(mouse_x, mouse_y)
                        if isinstance(idx, int):
                            selected_object = self.objects[idx]

                if selected_viewport.name == 'grid':  # If in the maze - grid - area.
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = self.get_clicked_cell_index(mouse_x, mouse_y)

                        # Set the cell's object in the level content if within limits.
                        self.level.set_cell_object(x, y, selected_object)
                        self.draw()

            pygame.display.update()
