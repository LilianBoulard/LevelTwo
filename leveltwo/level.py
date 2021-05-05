import numpy as np

from typing import Tuple, List, Optional
from datetime import datetime

from .object import GenericObject
from .database.models import LevelDBO
from .utils import string_to_list, list_to_string


class GenericLevel:

    def __init__(self, identifier: Optional[int], name: str, author: str, disposition: str,
                 content: np.array, creation_date: datetime, last_modification_date: datetime):
        self.identifier = identifier
        self.name = name
        self.author = author
        self.disposition = disposition
        self.content = content
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date

        self.objects_map = None
        self.objects = None

    @classmethod
    def from_dbo(cls, dbo: LevelDBO):
        """
        Takes a Levels Database Object (LevelsDBO, see `database/models.py`),
        and creates a new GenericLevel instance from the information it contains.
        """
        identifier = dbo.id
        name = dbo.name
        author = dbo.author
        disposition = dbo.disposition
        content = np.zeros(tuple([int(v) for v in string_to_list(dbo.shape)]), dtype='int16')
        creation_date = dbo.creation_date
        last_modification_date = dbo.last_modification_date
        return cls(identifier, name, author, disposition, content, creation_date, last_modification_date)

    def to_dbo(self) -> LevelDBO:
        name = self.name
        author = self.author
        disposition = self.disposition
        shape = list_to_string(self.content.shape)
        creation_date = datetime.now()
        last_modification_date = datetime.now()
        return LevelDBO(name, author, disposition, shape, creation_date, last_modification_date)

    @classmethod
    def create_new_level(cls, size: Tuple[int, int], disposition: str):
        identifier = None
        name = 'New level'
        author = 'New user'
        content = np.ones(size, dtype='int16')
        creation_date = datetime.utcnow()
        last_modification_date = datetime.utcnow()
        return cls(identifier, name, author, disposition, content, creation_date, last_modification_date)

    def set_objects(self, objects: List[GenericObject]) -> None:
        self.objects = objects

    def construct_object_content(self):
        """
        Takes the content of the level, and converts the integers to GenericObjects.
        Use sparsely, as it can be rather computationally expensive.
        """
        assert self.objects

        self.object_map = np.empty(self.content.shape, dtype='object')
        s_x, s_y = self.content.shape
        for x in range(s_x):
            for y in range(s_y):
                object_id = self.content[x, y]
                self.object_map[x, y] = self.objects[object_id - 1]

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

    def set_cell_object(self, x: int, y: int, obj: GenericObject) -> None:
        if self.get_number_of_objects_in(obj.identifier) < obj.max_instances:
            self.content[x, y] = obj.identifier

    def _get_object_coordinates(self, object_id: int) -> np.array:
        return np.argwhere(self.content == object_id)

    def get_starting_point_position(self) -> Tuple[int, int]:
        """
        Returns the `x` and `y` coordinates of the starting point in the level.
        """
        starting_point_index = 2
        cell_indexes = self._get_object_coordinates(starting_point_index)

        # If we don't find exactly one starting point, we raise an error
        if len(cell_indexes) != 1:
            raise ValueError('Invalid starting point')

        cell_index = cell_indexes[0]
        return cell_index[0], cell_index[1]

    def get_arrival_point_position(self) -> Tuple[int, int]:
        """
        Returns the `x` and `y` coordinates of the arrival point in the level.
        """
        arrival_point_index = 3
        cell_indexes = self._get_object_coordinates(arrival_point_index)

        # If we don't find exactly one arrival point, we raise an error
        if len(cell_indexes) != 1:
            raise ValueError('Invalid arrival point')

        cell_index = cell_indexes[0]
        return cell_index[0], cell_index[1]


class GenericLevelContent:

    def __init__(self, level_id: int, x: int, y: int, value: int):
        self.level_id = level_id
        self.x = x
        self.y = y
        self.value = value
