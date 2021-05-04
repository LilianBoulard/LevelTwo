import pygame

from .base import MazeSolvingAlgorithm


class Tremaux(MazeSolvingAlgorithm):

    name = "tremaux"
    inputs = {
        'up': pygame.key.key_code('Z'),
        'left': pygame.key.key_code('Q'),
        'down': pygame.key.key_code('S'),
        'right': pygame.key.key_code('D'),
    }

    def run_one_step(self):
        pass
