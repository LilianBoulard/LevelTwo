import numpy as np

from datetime import datetime


class GenericLevel:
    def __init__(self, identifier: int, name: str, author: str, creation_date: int, last_modification_date: int):
        self.identifier = identifier
        self.name = name
        self.author = author
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date
        self.content = self.get_content()
        self.shape = self.content.shape

    def write(self) -> None:
        """
        Writes the content to the database.
        """
        pass

    def get_content(self) -> np.array:
        """
        Constructs the level's content from the values stored in the database.
        :return:
        """
        pass

    def get_readable_creation_date(self) -> datetime:
        return datetime.fromtimestamp(self.creation_date)

    def get_readable_last_modification_date(self) -> datetime:
        return datetime.fromtimestamp(self.last_modification_date)
