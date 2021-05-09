import pygame
import pygame_menu

from tkinter import Tk
from tkinter import messagebox

from .config import Config
from .database import Database
from .level import GenericLevel

from .maze.square import MazeEditableSquare
from .maze.square import MazePlayableSquare
from .algorithm.square import TremauxSquare, ManualSquare, AstarSquare

from .maze.hexagonal import MazePlayableHexagonal
from .algorithm.hexagonal import ManualHexagonal

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
        self.level_selected: int = 1  # 1-indexed
        self.new_level_size: int = 10
        self.new_maze_name: str = ''
        self.new_maze_author: str = ''
        self.display_menu()

    def display_menu(self):

        def on_level_change(_: tuple, selection: int):
            self.level_selected = selection

        def on_text_change(value: str, *args, **kwargs):
            self.new_maze_author = value

        screen = self.get_screen()
        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)

        # User name text input
        menu.add.text_input('User name : ',
                            default=self.new_maze_author,
                            onchange=on_text_change,
                            maxchar=16)

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

        def on_text_change(value: str, *args, **kwargs):
            self.new_maze_name = value

        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)
        menu.add.text_input('Maze name : ',
                            default=self.new_maze_name,
                            onchange=on_text_change,
                            maxchar=16)
        menu.add.selector('Size : ',
                          [
                              ('Small', 10),
                              ('Medium', 20),
                              ('Large', 30),
                              ('Very large', 40)
                          ],
                          onchange=on_size_change)
        menu.add.button('Create', self.create_new_level)
        menu.add.button('Cancel', self.display_menu)
        menu.mainloop(self.get_screen())

    def create_new_level(self):
        if not self.new_maze_name or not self.new_maze_author:
            Tk().wm_withdraw()
            messagebox.showwarning('Cannot create maze', f'Missing user name and/or maze name.')
            self.create()

        size = (self.new_level_size, self.new_level_size)
        new_level = GenericLevel.create_new_level(size=size,
                                                  name=self.new_maze_name,
                                                  author=self.new_maze_author,
                                                  disposition='square')
        maze = MazeEditableSquare(parent_display=self, level=new_level)
        maze.run()
        self.display_menu()


class Play(Display):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level_selected = 1  # 1-indexed
        self.algorithm_selected = None
        self.display_menu()

    def display_menu(self):

        def on_level_change(_: tuple, selection: int) -> None:
            self.level_selected = selection

        screen = self.get_screen()
        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)

        # Level selector
        all_levels = self.db.get_all_levels()
        menu.add.selector('Level selected: ',
                          [(level.name, level.identifier) for level in all_levels],
                          onchange=on_level_change)

        menu.add.button('New game', self.select_algo_and_play)

        menu.add.button('Run test', self.rerun)

        menu.add.button('Quit', pygame_menu.events.EXIT)

        pygame.display.set_caption(Config.project_name)
        menu.mainloop(screen)

    def select_algo_and_play(self):

        def on_algorithm_change(_: tuple, selection) -> None:
            self.algorithm_selected = selection

        screen = self.get_screen()
        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)

        # Algorithm selector

        # Construct available algorithm depending on the level type
        level = self.db.construct_level(self.level_selected)
        if level.disposition == 'square':
            default_algo = ManualSquare
            algorithms = [
                ('Manual', ManualSquare),
                ('Trémaux', TremauxSquare),
                ('Astar', AstarSquare)
            ]
        elif level.disposition == 'hexagonal':
            default_algo = ManualHexagonal
            algorithms = [
                ('Manual', ManualHexagonal)
            ]
        else:
            raise ValueError(f'Invalid level type {level.disposition!r}')
        self.algorithm_selected = default_algo

        menu.add.selector('Algorithm: ', algorithms, onchange=on_algorithm_change)
        menu.add.button('Play', self.play)
        menu.add.button('Back to main menu', self.display_menu)

        pygame.display.set_caption(Config.project_name)
        menu.mainloop(screen)

    def play(self):
        level = self.db.construct_level(self.level_selected)
        if level.disposition == 'square':
            maze = MazePlayableSquare(parent_display=self, level=level)
        elif level.disposition == 'hexagonal':
            maze = MazePlayableHexagonal(parent_display=self, level=level)
        else:
            raise ValueError(f'Invalid level type {level.disposition!r}')
        maze.run(self.algorithm_selected)
        self.display_menu()

    def rerun(self):

        def run_test(t):
            if level.disposition == 'square':
                maze = MazePlayableSquare(parent_display=self, level=level)
            elif level.disposition == 'hexagonal':
                maze = MazePlayableHexagonal(parent_display=self, level=level)
            else:
                raise ValueError(f'Invalid level type {level.disposition!r}')
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
