from typing import Tuple
from functools import wraps

from .object import GenericObject
from .enums.effects import Effects


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
        self._update_location()

        # Self-explanatory
        # Contains the steps the character took to arrive at its current destination
        # It is appended each time `move_and_handle_object_effect()` is called
        # (depending on some conditions)
        self.path = [self.location]

        self._alive: bool = True
        self._stunned_for: int = 0

    # State verification methods.
    # These methods mustn't be decorated with `assert_state`.

    def is_alive(self) -> bool:
        return self._alive

    def is_stunned(self) -> bool:
        """
        Returns whether the character is stunned.
        """
        return self._stunned_for > 0

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
        Stuns the character for `duration` _steps_.
        """
        self._stunned_for += duration

    @assert_state('alive', 'able')
    def move(self, x: int, y: int) -> None:
        self.location_x = x
        self.location_y = y
        self._update_location()

    # Other

    def _update_location(self) -> None:
        self.location: Tuple[int, int] = (self.location_x, self.location_y)

    def append_location_to_path(self) -> None:
        self.path.append(self.location)

    def handle_object_effect(self, obj: GenericObject) -> None:
        """
        Applies effect(s) to the character depending on the effects defined in the object passed.
        """
        effect = Effects(obj.effect)
        if effect == Effects.NONE:
            pass
        elif effect == Effects.PLAYER_SLOW:
            self.get_stunned(1)
        elif effect == Effects.PLAYER_KILL:
            self.die()
        elif effect == Effects.LEVEL_FINISH:
            self.append_location_to_path()

    def move_and_handle_object_effect(self, x: int, y: int, obj: GenericObject) -> None:
        """
        Wrapper for both methods `move()` and `handle_object_effect()`.
        """
        if not obj.traversable:
            return

        self.append_location_to_path()

        try:
            self.move(x, y)
        except (Dead, Stunned):
            # If the character can't move, there is no use handling the object effect
            if self._stunned_for > 0:
                self._stunned_for -= 1
            return

        self.handle_object_effect(obj)
