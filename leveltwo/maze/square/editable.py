import pygame

from .base import MazeSquare
from ..base import MazeEditable

pygame.init()


class MazeEditableSquare(MazeEditable, MazeSquare):

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

                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h, self.draw)

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
