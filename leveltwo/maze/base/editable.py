from abc import ABC

import pygame
import numpy as np

from tkinter import Tk
from tkinter import messagebox

from typing import Tuple, Optional, Dict

from .maze import Maze
from .base import Viewport, BoundType

from ...enums import Colors
from ...database import Database
from ...sprites.object_to_color import ObjectToColor


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

        # We'll also display two dates:
        # 1. The level creation date
        # 2. The last time it was modified

        creation_intro_label = label.render(f"Created on", True, Colors.BLACK)
        creation_label = label.render(f'{self.level.creation_date}', True, Colors.BLACK)
        creation_intro_label_y = viewport_end_y - n - 100
        creation_label_y = creation_intro_label_y + creation_intro_label.get_height()

        last_modified_intro_label = label.render("Last modified on", True, Colors.BLACK)
        last_modified_label = label.render(f"{self.level.last_modification_date}", True, Colors.BLACK)
        last_modified_intro_label_y = creation_label_y + creation_label.get_height()
        last_modified_label_y = last_modified_intro_label_y + last_modified_intro_label.get_height()

        self.screen.blit(creation_intro_label, (x, creation_intro_label_y))
        self.screen.blit(creation_label, (x, creation_label_y))
        self.screen.blit(last_modified_intro_label, (x, last_modified_intro_label_y))
        self.screen.blit(last_modified_label, (x, last_modified_label_y))

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
