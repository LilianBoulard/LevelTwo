"""
Implements utility functions.
"""


def list_to_string(l: list) -> str:
    """
    :param list l: A list to serialize.
    :return str: The same list, as a string.
    """
    return ', '.join([str(v) for v in l])


def string_to_list(s: str) -> list:
    """
    :param str s: A serialized list.
    :return list: The actual list.
    """
    return s.split(', ')
