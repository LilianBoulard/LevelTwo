"""
Implements utility functions.
"""

from time import time
from math import floor
from typing import Tuple


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


def get_timestamp() -> int:
    """
    Returns the current time, as a UNIX timestamp.
    """
    return floor(time())


def calc_tuple(operator, first_tuple: Tuple[int, ...], second_tuple: Tuple[int, ...]):
    """
    Uses an operator on two tuples of integers.
    They must be of same size.
    The arithmetic operator must be the magic function of the class `int`.
    Example:
    >>> calc_tuple(int.__sub__, (5, 5), (5, 0))
    (0, 5)
    """
    if len(first_tuple) != len(second_tuple):
        raise ValueError('Tuples are not the same size.')
    return tuple(operator(a, b) for a, b in zip(first_tuple, second_tuple))
