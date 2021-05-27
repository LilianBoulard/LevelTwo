class InvalidLevelType(Exception):

    def __init__(self, level_type: str):
        message = f"Invalid level type {level_type}"
        super().__init__(message)
