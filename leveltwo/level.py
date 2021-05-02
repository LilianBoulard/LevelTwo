import numpy as np

from datetime import datetime

from .object import GenericObject
from .utils import string_to_list


class GenericLevel:
    def __init__(self, identifier: int, name: str, author: str, content: np.array,
                 creation_date: datetime, last_modification_date: datetime):
        self.identifier = identifier
        self.name = name
        self.author = author
        self.content = content
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date

    @classmethod
    def from_dbo(cls, dbo):
        """
        Takes a Levels Database Object (LevelsDBO, see `database/models.py`),
        and creates a new GenericLevel instance from the information it contains.
        """
        identifier = dbo.id
        name = dbo.name
        author = dbo.author
        content = np.zeros(tuple([int(v) for v in string_to_list(dbo.shape)]), dtype='int16')
        creation_date = dbo.creation_date
        last_modification_date = dbo.last_modification_date
        return cls(identifier, name, author, content, creation_date, last_modification_date)

    @classmethod
    def create_new_level(cls):
        identifier = None
        name = 'New level'
        author = 'New user'
        content = np.ones((25, 25), dtype='int16')
        creation_date = datetime.utcnow()
        last_modification_date = datetime.utcnow()
        return cls(identifier, name, author, content, creation_date, last_modification_date)

    def write(self) -> None:
        """
        Writes own content to the database.
        """
        pass

    def get_number_of_objects_in(self, object_id: int) -> int:
        """
        Gets number of occurrences of the object in the content.
        """
        return self.content[self.content == object_id].size

    def is_object_occurrences_in_limits(self, obj: GenericObject) -> bool:
        """
        Takes an object id, and returns whether its number of occurrences
        in the content is within the object limits.
        """
        occurrences = self.get_number_of_objects_in(obj.identifier)
        return obj.min_instances <= occurrences <= obj.max_instances

    def set_cell_object(self, x: int, y: int, obj: GenericObject):
        if self.get_number_of_objects_in(obj.identifier) < obj.max_instances:
            self.content[x, y] = obj.identifier


class GenericLevelContent:
    def __init__(self, level_id: int, x: int, y: int, value: int):
        self.level_id = level_id
        self.x = x
        self.y = y
        self.value = value

    @classmethod
    def from_dbo(cls, dbo):
        level_id = dbo.level_id
        x = dbo.x
        y = dbo.y
        value = dbo.value
        cls(level_id, x, y, value)
