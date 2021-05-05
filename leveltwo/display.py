import pygame
import pygame_menu

from .config import Config
from .database import Database
from .level import GenericLevel
from .maze.square import MazeEditableSquare
from .maze.square import MazePlayableSquare

from .maze.algorithm.square import Tremaux, Manual

from typing import Tuple

pygame.init()


class Display:

    """
    Parameters
    ----------

    screen_size: Tuple[int, int]
        A 2-tuple containing (1) the screen width and (2) the screen height.

    """

    def __init__(self, screen_size: Tuple[int, int]):
        self.screen_size = screen_size
        self.theme: pygame_menu.themes.Theme = pygame_menu.themes.THEME_SOLARIZED
        self.running = True
        self.db = Database()

    def set_theme(self, new_theme: pygame_menu.themes.Theme):
        self.theme = new_theme

    def get_screen(self):
        return pygame.display.set_mode(self.screen_size)


class LevelEditor(Display):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level_selected = 1  # 1-indexed
        self.new_level_size = 20
        self.display_menu()

    def display_menu(self):

        def on_level_change(_: tuple, selection: int):
            self.level_selected = selection

        screen = self.get_screen()
        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)

        # Level selector
        all_levels = self.db.get_all_levels()
        menu.add.selector('Level selected: ',
                          [(level.name, level.identifier) for level in all_levels],
                          onchange=on_level_change)

        edit_args = []  # Positional args to be passed to the callback below.
        menu.add.button('Edit', self.edit, *edit_args)

        create_args = []
        menu.add.button('Create', self.create, *create_args)

        menu.add.button('Quit', pygame_menu.events.EXIT)

        pygame.display.set_caption(Config.project_name)
        menu.mainloop(screen)

    def edit(self):
        # Get level from database
        level = self.db.construct_level(self.level_selected)
        maze = MazeEditableSquare(parent_display=self, level=level)
        maze.run()
        self.display_menu()

    def create(self):

        def on_size_change(_: tuple, selection: int):
            self.new_level_size = selection

        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)
        menu.add.text_input('Maze name : ')
        menu.add.selector('Size : ',
                          [('Small', 10), ('Medium', 20), ('Large', 30)],
                          onchange=on_size_change)
        menu.add.button('Create', self.create_new_level)
        menu.add.button('Cancel', self.display_menu)
        menu.mainloop(self.get_screen())

    def create_new_level(self):
        # Create new level
        size = (self.new_level_size, self.new_level_size)
        new_level = GenericLevel.create_new_level(size)
        maze = MazeEditableSquare(parent_display=self, level=new_level)
        maze.run()
        self.display_menu()


class Play(Display):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level_selected = 1  # 1-indexed
        self.algorithm_selected = Manual
        self.display_menu()

    def display_menu(self):

        def on_level_change(_: tuple, selection: int) -> None:
            self.level_selected = selection

        def on_algorithm_change(_: tuple, selection) -> None:
            self.algorithm_selected = selection

        screen = self.get_screen()
        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)

        # Level selector
        all_levels = self.db.get_all_levels()
        menu.add.selector('Level selected: ',
                          [(level.name, level.identifier) for level in all_levels],
                          onchange=on_level_change)

        # Algorithm selector
        menu.add.selector('Algorithm: ',
                          [
                              ('Manual', Manual),
                              ('Trémaux', Tremaux)
                          ],
                          onchange=on_algorithm_change)

        play_args = []  # Positional args to be passed to the callback below.
        menu.add.button('New game', self.play, *play_args)

        rerun_args = []
        menu.add.button('Run test', self.rerun, *rerun_args)

        menu.add.button('Quit', pygame_menu.events.EXIT)

        pygame.display.set_caption(Config.project_name)
        menu.mainloop(screen)

    def play(self):
        level = self.db.construct_level(self.level_selected)
        maze = MazePlayableSquare(parent_display=self, level=level)
        maze.run(self.algorithm_selected)
        self.display_menu()

    def rerun(self):

        def run_test(t):
            maze = MazePlayableSquare(parent_display=self, level=level)
            maze.rerun(t)
            self.display_menu()

        screen = self.get_screen()
        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)

        level = self.db.construct_level(self.level_selected)
        all_tests = self.db.get_tests_by_level_id(level.identifier)
        for test in all_tests:
            menu.add.button(f'{test.run_date} | {test.algorithm} ({len(test.steps)} steps)', run_test, test)
        else:
            menu.add.button('Back to main menu', self.display_menu)

        menu.mainloop(screen)
