import numpy as np

from datetime import datetime

from ...level import GenericLevel


example_level_content = np.array([[2, 4, 4, 1, 4, 1, 1, 5, 5, 1],
                                  [1, 4, 5, 6, 4, 4, 4, 1, 4, 4],
                                  [1, 4, 5, 4, 4, 5, 1, 1, 4, 1],
                                  [1, 1, 1, 4, 1, 1, 4, 1, 4, 1],
                                  [1, 4, 4, 4, 1, 4, 4, 1, 1, 1],
                                  [1, 1, 1, 1, 5, 4, 1, 1, 4, 4],
                                  [4, 4, 4, 4, 5, 4, 4, 4, 4, 6],
                                  [1, 1, 1, 1, 1, 4, 1, 5, 1, 1],
                                  [1, 4, 4, 4, 4, 4, 1, 4, 4, 1],
                                  [1, 5, 5, 1, 1, 1, 1, 4, 1, 3]])
example_level = GenericLevel(1, 'Example maze', 'LevelTwoTeam', example_level_content,
                             datetime.utcfromtimestamp(1619433467), datetime.utcfromtimestamp(1619433745))
