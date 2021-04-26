import pygame
import pygame_menu

from . import Database, MazeEditable

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
        self.level_selected = 1  # 1-indexed
        self.running = True
        self.db = Database()

    def set_theme(self, new_theme: pygame_menu.themes.Theme):
        self.theme = new_theme

    def get_screen(self):
        return pygame.display.set_mode(self.screen_size)

    def play(self, user_input):
        screen = self.get_screen()
        menu = pygame_menu.Menu('LevelTwo', *self.screen_size, theme=self.theme)
        menu.add.button(f"Welcome {user_input.get_value()} to level {self.level_selected}", self.play)
        menu.add.button('Back to main menu', self.display_menu)
        pygame.display.set_caption('LevelTwo')
        menu.mainloop(screen)

    def edit(self):
        # Get level from database
        level = self.db.construct_level(self.level_selected)
        maze = MazeEditable(parent_display=self, level=level)
        maze.run()
        self.get_screen()

    def create(self):
        # Get level from database
        level = self.db.construct_level(self.level_selected)
        maze = MazeEditable(parent_display=self, level=level)
        maze.run()
        self.get_screen()

    def display_menu(self):

        def on_selector_change(struct: tuple, selection: int):
            self.level_selected = selection
            print(selection)

        screen = self.get_screen()
        menu = pygame_menu.Menu('LevelTwo', *self.screen_size, theme=self.theme)
        user_input = menu.add.text_input('Name :', default='')

        # Level selector
        all_levels = self.db.get_all_levels()
        menu.add.selector('Level selected: ',
                          [(level.name, level.identifier) for level in all_levels],
                          onchange=on_selector_change)

        play_args = [user_input]  # Positional args to be passed to the callback below.
        menu.add.button('Play', self.play, *play_args)

        edit_args = []
        menu.add.button('Edit', self.edit, *edit_args)

        create_args = []
        menu.add.button('Create', self.create, *create_args)

        menu.add.button('Quit', pygame_menu.events.EXIT)

        pygame.display.set_caption('LevelTwo')
        menu.mainloop(screen)
