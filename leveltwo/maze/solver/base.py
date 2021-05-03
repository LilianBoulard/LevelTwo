from ...database import Database
from ...level import GenericLevel
from ...character import Character


class MazeSolver:

    def __init__(self, level: GenericLevel, character: Character):
        self.level = level
        self.character = character

        db = Database()
        self.objects = db.get_all_objects()
