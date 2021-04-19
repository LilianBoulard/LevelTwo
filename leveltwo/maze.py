import pygame
import numpy as np

from typing import Tuple

from leveltwo.enums import Objects
from leveltwo.utils import calc_tuple

pygame.init()
style = pygame.font.SysFont('calibri', 50)
label = pygame.font.SysFont('calibri', 20)

# Define colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BROWN = (222,184,135)
GREEN = (0,128,0)
RED = (128,0,0)

# Toolbox settings
toolbox_size = (200, 0)


class Cell:

    """
    Implements a `Cell`, which is a square in our maze.
    It acts as a block in which the character can move (one at a time),
    and in which an object can be placed.
    """

    def __init__(self, object_type: Objects, origin_x: int, origin_y: int, end_x: int, end_y: int):
        self.object_type: Objects = object_type
        self.origin_x: int = origin_x
        self.origin_y: int = origin_y
        self.end_x: int = end_x
        self.end_y: int = end_y

    def inside(self, x: int, y: int) -> bool:
        """
        Takes coordinates and returns whether they are located inside this cell perimeter.

        :param int x:
        :param int y:
        :return bool: True if they are, False otherwise.
        """
        return self.origin_x < x <= self.end_x and self.origin_y < y <= self.end_y

    def get_sprite(self):
        pass


class Maze:

    def __init__(self, parent_display, screen_size: Tuple[int, int], side_cells_count: int):
        self.parent = parent_display
        self.screen_size = calc_tuple(int.__add__, self.squarify(screen_size), toolbox_size)
        self.side_cells_count = side_cells_count
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.screen.fill(WHITE)  # Set the background color
        self._running = True
        pygame.display.set_caption("Level")

    def squarify(self, size: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        "squarifies" a tuple of integers.
        Example:
        >>> self.squarify((1920, 1080))
        (1080, 1080)
        """
        m = min(size)
        return tuple(m for _ in range(len(size)))

    def resize(self, x: int, y: int):
        """
        Resizes PyGame's window.
        """
        self.screen_size = (x, y)
        self.draw_grid()

    def draw_grid(self) -> np.array:
        """
        Constructs the maze's grid.
        """
        # Compute `z`, the size each cell has on the screen (number of pixels).
        # Using a round division might produce some unwanted pixel lines along the window's edges.
        # A further version might implement the auto-resizing of the window if
        # the standard division does not produce a round integer.
        grid_size = calc_tuple(int.__sub__, self.screen_size, toolbox_size)
        z = max(grid_size) // self.side_cells_count
        # Create a numpy array that will act as a matrix, in which we will store the cells.
        cells = np.empty((self.side_cells_count, self.side_cells_count), dtype='object')
        for i_x in range(self.side_cells_count):  # Along the x axis
            for i_y in range(self.side_cells_count):  # Along the y axis
                # Create the cell stored in this location.
                # This information is usually read from the database.
                x = i_x * z
                y = i_y * z
                cell = Cell(Objects.EMPTY,
                            origin_x=x,
                            origin_y=y,
                            end_x=x + z,
                            end_y=y + z,)
                # Add the cell to the matrix
                cells[i_x, i_y] = cell
                # Draw the rectangle.
                rect = pygame.Rect(x, y, z, z)
                pygame.draw.rect(self.screen, BLACK, rect, width=1)
        return cells

    def get_clicked_cell(self, x: int, y: int, cells: np.array) -> Cell or None:
        """
        Iterates through the cells matrix and returns the one the user clicked on,
        based on the coordinates of his input.

        :param int x:
        :param int y:
        :param np.array cells:
        :return Cell|None: A Cell if found, None otherwise.
        """
        for cell_row in cells:
            for cell in cell_row:
                if cell.inside(x, y):
                    return cell

    def run(self) -> None:
        """
        Main loop.
        """
        cells = self.draw_grid()
        while self._running:
            for event in pygame.event.get():
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse was clicked.
                    clicked_cell = self.get_clicked_cell(mouse_x, mouse_y, cells)
                    if not clicked_cell:
                        continue
                    print(vars(clicked_cell))
                if event.type == pygame.VIDEORESIZE:  # If the screen was resized.
                    self.resize(event.w, event.h)
            pygame.display.update()


class MazeDisplay(Maze):
    pass


class MazeEditable(Maze):

    def run(self) -> None:
        """
        Main loop.
        """
        #Drawing ToolBox
        #Title
        menu_label = label.render("ToolBox",1,BLACK)
        self.screen.blit(menu_label,(610,5))
        indic_label = label.render("Cliquez et Placez",1,BLACK)
        self.screen.blit(indic_label,(570,25))

        #Trap
        trap_label = label.render("Piège", 1, BLACK) 
        trap = pygame.Rect(610,50,trap_label.get_width(),trap_label.get_height())
        pygame.draw.rect(self.screen, BROWN, trap)
        self.screen.blit(trap_label, (610, 50))
        #Wall
        wall_label = label.render("Mur", 1, WHITE) 
        wall = pygame.Rect(610,100,wall_label.get_width(),wall_label.get_height())
        pygame.draw.rect(self.screen, BLACK, wall)
        self.screen.blit(wall_label, (610, 100))
        
        #Start
        start_label = label.render("Start", 1, BLACK) 
        start = pygame.Rect(610,150,start_label.get_width(),start_label.get_height())
        pygame.draw.rect(self.screen, GREEN, start)
        self.screen.blit(start_label, (610, 150))

        #Arrival
        arrival_label = label.render("Arrival", 1, BLACK) 
        arrival = pygame.Rect(610,200,arrival_label.get_width(),arrival_label.get_height())
        pygame.draw.rect(self.screen, RED, arrival)
        self.screen.blit(arrival_label, (610, 200))

        #Empty
        empty_label = label.render("Couloir", 1, BLACK) 
        empty = pygame.Rect(610,250,empty_label.get_width(),empty_label.get_height())
        pygame.draw.rect(self.screen, WHITE, empty)
        self.screen.blit(empty_label, (610, 250))

        #Mud
        mud_label = label.render("Mud", 1, BLACK) 
        mud = pygame.Rect(610,300,mud_label.get_width(),mud_label.get_height())
        pygame.draw.rect(self.screen, BROWN, mud)
        self.screen.blit(mud_label, (610, 300))

        cells = self.draw_grid()
        while self._running:
            for event in pygame.event.get():
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if 540 < mouse_x < 740 and 0 < mouse_y < 540:   
                    if trap.collidepoint((mouse_x,mouse_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                        choix = 1
                        print(choix)
                    elif wall.collidepoint((mouse_x,mouse_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                        choix = 2
                        print(choix)
                    elif start.collidepoint((mouse_x,mouse_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                        choix = 3
                        print(choix)
                    elif arrival.collidepoint((mouse_x,mouse_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                        choix = 4
                        print(choix)
                    elif empty.collidepoint((mouse_x,mouse_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                        choix = 5
                        print(choix)
                    elif mud.collidepoint((mouse_x,mouse_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                        choix = 6
                        print(choix)
                if 0 < mouse_x < 540 and 0 < mouse_y < 540: 
                    if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse was clicked.
                        clicked_cell = self.get_clicked_cell(mouse_x, mouse_y, cells)
                        z = clicked_cell.end_x - clicked_cell.origin_x
                        if not clicked_cell:
                            continue
                        print(vars(clicked_cell))
                        if choix == 1:
                            rect = pygame.Rect(clicked_cell.origin_x, clicked_cell.origin_y, z, z)
                            pygame.draw.rect(self.screen, BROWN, rect)
                            clicked_cell.object_type = Objects.TRAP
                        elif choix == 2:
                            rect = pygame.Rect(clicked_cell.origin_x, clicked_cell.origin_y, z, z)
                            pygame.draw.rect(self.screen, BLACK, rect)
                            clicked_cell.object_type = Objects.WALL
                        elif choix == 3:
                            rect = pygame.Rect(clicked_cell.origin_x, clicked_cell.origin_y, z, z)
                            pygame.draw.rect(self.screen, GREEN, rect)
                            clicked_cell.object_type = Objects.START
                        elif choix == 4:
                            rect = pygame.Rect(clicked_cell.origin_x, clicked_cell.origin_y, z, z)
                            pygame.draw.rect(self.screen, RED, rect)
                            clicked_cell.object_type = Objects.ARRIVAL
                        elif choix == 5:
                            rect = pygame.Rect(clicked_cell.origin_x, clicked_cell.origin_y, z, z)
                            pygame.draw.rect(self.screen, WHITE, rect)
                            clicked_cell.object_type = Objects.EMPTY
                        elif choix == 6:
                            rect = pygame.Rect(clicked_cell.origin_x, clicked_cell.origin_y, z, z)
                            pygame.draw.rect(self.screen, BROWN, rect)    
                            clicked_cell.object_type = Objects.MUD
                if event.type == pygame.VIDEORESIZE:  # If the screen was resized.
                    self.resize(event.w, event.h)
            pygame.display.update()
