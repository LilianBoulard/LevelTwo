import pygame
import pygame_menu

from .config import Config
from .database import Database
from .level import GenericLevel
from .maze import MazeEditable, MazeDisplay

from typing import Tuple


pygame.init()
# Set font
style = pygame.font.SysFont('calibri', 50)

# timer = pygame.time.Clock()


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

        def on_selector_change(_: tuple, selection: int):
            self.level_selected = selection

        screen = self.get_screen()
        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)

        # Level selector
        all_levels = self.db.get_all_levels()
        menu.add.selector('Level selected: ',
                          [(level.name, level.identifier) for level in all_levels],
                          onchange=on_selector_change)

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
        maze = MazeEditable(parent_display=self, level=level)
        maze.run()
        self.get_screen()

    def create(self):

        def on_selector_change(_: tuple, selection: int):
            self.new_level_size = selection

        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)
        menu.add.text_input('Maze name : ')
        menu.add.selector('Size : ',
                          [('Small', 10), ('Medium', 20), ('Large', 30)],
                          onchange=on_selector_change)
        menu.add.button('Create', self.create_new_level)
        menu.add.button('Cancel', self.display_menu)
        menu.mainloop(self.get_screen())

    def create_new_level(self):
        # Create new level
        size = (self.new_level_size, self.new_level_size)
        new_level = GenericLevel.create_new_level(size)
        maze = MazeEditable(parent_display=self, level=new_level)
        maze.run()
        self.get_screen()


class Play(Display):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level_selected = 1  # 1-indexed
        self.algorithm_selected = 0  # 0-indexed
        self.display_menu()

    def display_menu(self):

        def on_selector_change(_: tuple, selection: int):
            self.level_selected = selection

        screen = self.get_screen()
        menu = pygame_menu.Menu(Config.project_name, *self.screen_size, theme=self.theme)

        # Level selector
        all_levels = self.db.get_all_levels()
        menu.add.selector('Level selected: ',
                          [(level.name, level.identifier) for level in all_levels],
                          onchange=on_selector_change)

        # Algorithm selector
        menu.add.selector('Algorithm: ',
                          Config.pathfinding_algorithms,
                          onchange=on_selector_change)

        play_args = []  # Positional args to be passed to the callback below.
        menu.add.button('Play', self.play, *play_args)

        menu.add.button('Quit', pygame_menu.events.EXIT)

        pygame.display.set_caption(Config.project_name)
        menu.mainloop(screen)

    def play(self):
        level = self.db.construct_level(self.level_selected)
        maze = MazeDisplay(parent_display=self, level=level)
        maze.run()
        self.get_screen()


