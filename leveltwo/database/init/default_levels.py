import numpy as np

from datetime import datetime

from ...level import GenericLevel


example_square_level_content = np.array([[2, 4, 4, 1, 4, 1, 1, 5, 5, 1],
                                         [1, 4, 5, 6, 4, 4, 4, 1, 4, 4],
                                         [1, 4, 5, 4, 4, 5, 1, 1, 4, 1],
                                         [1, 1, 1, 4, 1, 1, 4, 1, 4, 1],
                                         [1, 4, 4, 4, 1, 4, 4, 1, 1, 1],
                                         [1, 1, 1, 1, 5, 4, 1, 1, 4, 4],
                                         [4, 4, 4, 4, 5, 4, 4, 4, 4, 6],
                                         [1, 1, 1, 1, 1, 4, 1, 5, 1, 1],
                                         [1, 4, 4, 4, 4, 4, 1, 4, 4, 1],
                                         [1, 5, 5, 1, 1, 1, 1, 4, 1, 3]])
example_square_level = GenericLevel(1, 'Example square maze', 'LevelTwoTeam', 'square',
                                    example_square_level_content,
                                    datetime.utcfromtimestamp(1619433467), datetime.utcfromtimestamp(1619433745))

example_hexagonal_level_content = np.array([[1, 4, 1, 4, 1, 2, 0, 0, 0, 0, 0],
                                            [4, 6, 4, 1, 1, 4, 1, 0, 0, 0, 0],
                                            [1, 1, 1, 1, 4, 1, 4, 4, 0, 0, 0],
                                            [4, 4, 1, 1, 4, 1, 1, 1, 4, 0, 0],
                                            [1, 1, 1, 4, 4, 1, 4, 4, 1, 6, 0],
                                            [1, 4, 4, 1, 1, 4, 1, 4, 1, 4, 1],
                                            [0, 1, 1, 4, 1, 1, 4, 1, 4, 4, 4],
                                            [0, 0, 4, 4, 1, 4, 4, 4, 1, 1, 1],
                                            [0, 0, 0, 1, 4, 1, 4, 1, 1, 4, 4],
                                            [0, 0, 0, 0, 1, 1, 1, 1, 1, 4, 1],
                                            [0, 0, 0, 0, 0, 3, 4, 1, 4, 6, 1]])
example_hexagonal_level = GenericLevel(2, 'Example hexagonal maze', 'LevelTwoTeam', 'hexagonal',
                                       example_hexagonal_level_content,
                                       datetime.utcfromtimestamp(1620214577), datetime.utcfromtimestamp(1620214577))

all_levels = [example_square_level, example_hexagonal_level]
