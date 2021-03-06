import pygame

from ..base import Manual

from ...enums import Effects


class ManualSquare(Manual):

    inputs = {
        'up': pygame.key.key_code('Z'),
        'left': pygame.key.key_code('Q'),
        'down': pygame.key.key_code('S'),
        'right': pygame.key.key_code('D'),
    }

    def run_one_step(self, key) -> None:
        if not key:
            return

        if key == self.inputs['up']:
            # Go up
            self.move_character(0)
        elif key == self.inputs['left']:
            # Go left
            self.move_character(1)
        elif key == self.inputs['down']:
            # Go down
            self.move_character(2)
        elif key == self.inputs['right']:
            # Go right
            self.move_character(3)

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

                if next_step_cell_object.traversable:
                    self.character.move_and_handle_object_effect(new_x, new_y, next_step_cell_object)
                    if next_step_cell_object.effect == Effects.LEVEL_FINISH:
                        self._running = False

                # If the character is dead, end.
                if not self.character.is_alive():
                    self._running = False
