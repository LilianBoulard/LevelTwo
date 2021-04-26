import numpy as np

from datetime import datetime

from ...level import GenericLevel


example_level_content = np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                  [4, 1, 1, 6, 4, 1, 4, 4, 4, 4],
                                  [4, 1, 4, 4, 1, 1, 1, 4, 3, 4],
                                  [4, 1, 1, 4, 1, 4, 1, 4, 1, 4],
                                  [4, 4, 1, 4, 1, 4, 1, 6, 1, 4],
                                  [4, 4, 1, 4, 1, 5, 5, 4, 1, 4],
                                  [4, 1, 1, 4, 1, 4, 1, 1, 5, 4],
                                  [4, 1, 4, 1, 1, 4, 4, 1, 1, 4],
                                  [4, 2, 1, 1, 6, 1, 1, 4, 4, 4],
                                  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]])
example_level = GenericLevel(0, 'Example maze', 'LevelTwoTeam', example_level_content,
                             datetime.utcfromtimestamp(1619433467), datetime.utcfromtimestamp(1619433745))