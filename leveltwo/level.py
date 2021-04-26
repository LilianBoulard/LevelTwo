import numpy as np

from typing import Tuple
from datetime import datetime

from . import Database


class GenericLevel:
    def __init__(self, identifier: int, name: str, author: str, shape: Tuple[int, int],
                 creation_date: int, last_modification_date: int):
        self.identifier = identifier
        self.name = name
        self.author = author
        self.shape = shape
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date
        self.content = self.get_content()

    @classmethod
    def from_dbo(cls, dbo):
        """
        Takes a Levels Database Object (LevelsDBO, see `database/models.py`),
        and creates a new GenericLevel instance from the information it contains.
        """
        identifier = dbo.id
        name = dbo.name
        author = dbo.author
        shape = dbo.shape
        creation_date = dbo.creation_date
        last_modification_date = dbo.last_modification_date
        return cls(identifier, name, author, shape, creation_date, last_modification_date)

    def write(self) -> None:
        """
        Writes own content to the database.
        """
        pass

    def get_content(self) -> np.array:
        """
        Constructs the level's content from the values stored in the database.
        :return numpy.array:
        """
        db = Database()
        # Init content, a numpy array
        content = np.zeros(self.shape)
        mapping = db.get_level_content_by_id(self.identifier)
        # For each cell stored in the database, paste its content in the array.
        # Note: possible optimization: remove all cells in the database that have
        # their value to `0`, as we create by default an array of zeros.
        for cell in mapping:
            content[cell.x, cell.y] = cell.value
        return content

    def get_readable_creation_date(self) -> datetime:
        return datetime.fromtimestamp(self.creation_date)

    def get_readable_last_modification_date(self) -> datetime:
        return datetime.fromtimestamp(self.last_modification_date)
