import pygame
import pygame_menu

from leveltwo.maze import Maze, MazeDisplay, MazeEditable

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
        self.level_selected = 0
        self.running = True

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
        # GET MAZE FROM DB
        maze = MazeEditable(parent_display=self,
                            screen_size=self.screen_size,
                            side_cells_count=15)
        maze.run()
        self.get_screen()

    def create(self):
        maze = MazeEditable(parent_display=self,
                            screen_size=self.screen_size,
                            side_cells_count=15)
        maze.run()
        self.get_screen()

    def display_menu(self):

        def on_selector_change(struct: tuple, selection: int):
            self.level_selected = selection

        screen = self.get_screen()
        menu = pygame_menu.Menu('LevelTwo', *self.screen_size, theme=self.theme)
        user_input = menu.add.text_input('Name :', default='')

        # Level selector
        menu.add.selector('Level selected: ', [
            ('Random level', 0),
            ('First level', 1),
            ('Second level', 2),
        ], onchange=on_selector_change)

        play_args = [user_input]  # Positional args to be passed to the callback below.
        menu.add.button('Play', self.play, *play_args)

        edit_args = []
        menu.add.button('Edit', self.edit, *edit_args)

        create_args = []
        menu.add.button('Create', self.create, *create_args)

        menu.add.button('Quit', pygame_menu.events.EXIT)

        pygame.display.set_caption('LevelTwo')
        menu.mainloop(screen)
