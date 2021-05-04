from datetime import datetime

from .database.models import TestDBO


class Test:

    def __init__(self, identifier, level_id, algorithm, steps, run_date):
        self.identifier = identifier
        self.level_id = level_id
        self.algorithm = algorithm
        self.steps = steps
        self.run_date = run_date

    @classmethod
    def from_dbo(cls, dbo: TestDBO):
        """
        Takes a Levels Database Object (LevelsDBO, see `database/models.py`),
        and creates a new GenericLevel instance from the information it contains.
        """
        identifier = dbo.id
        level_id = dbo.level_id
        algorithm = dbo.algorithm
        steps = [(0, 0) for _ in range(dbo.steps_number)]
        run_date = dbo.run_date
        return cls(identifier, level_id, algorithm, steps, run_date)

    def to_dbo(self) -> TestDBO:
        level_id = self.level_id
        algorithm = self.algorithm
        steps_number = len(self.steps)
        run_date = datetime.now()
        return TestDBO(level_id, algorithm, steps_number, run_date)


class TestContent:

    def __init__(self, test_id: int, step: int, x: int, y: int):
        self.test_id = test_id
        self.step = step
        self.x = x
        self.y = y
