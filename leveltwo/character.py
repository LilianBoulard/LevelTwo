from time import time
from math import floor
from functools import wraps


class Dead(Exception):
    """
    Exception raised when a character is dead, but asked to do something.
    """
    pass


class Alive(Exception):
    """
    Exception raised when a character is alive, but shouldn't.
    """
    pass


class Stunned(Exception):
    """
    Exception raised when a character is stunned and cannot execute the action.
    """
    pass


def assert_state(*expected_states: str):
    """
    Decorator used to assert that the character is in certain states before performing the requested action.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            instance = args[0]  # Get `self`, the instance.
            for expected_state in expected_states:
                if expected_state == 'alive':
                    if not instance.is_alive():
                        raise Dead
                elif expected_state == 'dead':
                    if instance.is_alive():
                        raise Alive
                elif expected_state == 'able':
                    if instance.is_stunned():
                        raise Stunned
            return func(*args, **kwargs)
        return wrapper
    return decorator


class Character:

    """
    Implements a character class.

    Parameters
    ----------

    start_location_x: int
        Starting location of the character on the `x` (horizontal) axis.

    start_location_y: int
        Starting location of the character on the `y` (vertical) axis.

    """

    def __init__(self, start_location_x: int, start_location_y: int):
        self.location_x: int = start_location_x
        self.location_y: int = start_location_y

        self._alive: bool = True
        self._stunned_until: int = 0

    # State verification methods.
    # These methods mustn't be decorated with `assert_state`.

    def is_alive(self) -> bool:
        return self._alive

    def is_stunned(self) -> bool:
        """
        Returns whether the character is stunned.
        """
        return time() > self._stunned_until

    def is_able(self) -> bool:
        return self.is_stunned()  # Use `and`

    # Action methods
    # These methods should be decorated with `assert_state`.

    @assert_state('alive')
    def die(self) -> None:
        """
        Kills the character, making it unable to execute further actions.
        """
        self._alive = False

    @assert_state('dead')
    def get_resurrected(self):
        """
        Resurrects the character.
        """
        self._alive = True

    @assert_state('alive')
    def get_stunned(self, duration: int) -> None:
        """
        Stuns the character for `duration` _seconds_.
        """
        self._stunned_until = floor(time() + duration)

    @assert_state('alive', 'able')
    def move(self, direction: int, amount: int = 1) -> None:
        """
        Changes the position of the character by `amount` cell(s).
        Does not verify if we are running into a wall, out of the map bounds, and so on.

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

        for _ in range(amount):
            if direction == 0:
                self.location_y -= 1
            elif direction == 1:
                self.location_x -= 1
            elif direction == 2:
                self.location_y += 1
            elif direction == 3:
                self.location_x += 1
