from .base import MazeSolvingAlgorithm


class Tremaux(MazeSolvingAlgorithm):
    name = "tremaux"

    def __init__(self):
        level = self.level

    def run_one_step(self):
        x, y = self.character.location

        up_cell_value = self.level.content[x, y - 1]
        left_cell_value = self.level.content[x - 1, y]
        down_cell_value = self.level.content[x, y + 1]
        right_cell_value = self.level.content[x + 1, y]

        priority = {
            0: 'endpoint',
            1: 'empty',
            2: 'mud',
            3: 'visited'
        }
        if self.level.content[x][y] == 3:
            print('end %d,%d' % (x, y))
            return True
        elif self.level.content[x][y] == 4:
            print('wall %d,%d' % (x, y))
            return False
        elif self.level.content[x][y] == 6:
            print('trap %d,%d' % (x, y))
            return False

        print("empty")

        self.character.location[x][y]
        if ((x < len(self.level.content) - 1 and self.run_one_step(x + 1, y))
                or (y > 0 and self.run_one_step(x, y - 1))
                or (x > 0 and self.run_one_step(x - 1, y))
                or (y < len(self.level.content) - 1 and self.run_one_step(x, y + 1))):
            return True
        return False
