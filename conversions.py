from constants import LETTERS, NUMBERS
from typing import Tuple


def algebraic_to_index(an: str) -> int:
    """
    Converts from algebraic notation to an index
    :param an: algebraic notation to be converted
    :return: index from 0-63
    """
    c = LETTERS.index(an[0])
    r = NUMBERS[::-1].index(an[1])
    return 8 * r + c


def index_to_algebraic(i: int) -> str:
    """
    Converts from an index to algebraic notation
    :param i: index from 0-63 to be converted
    :return: algebraic notation from the index
    """
    c, r = index_to_coordinate(i)
    return LETTERS[c] + NUMBERS[::-1][r]


def index_to_coordinate(i: int) -> Tuple[int, int]:
    """
    Converts from an index to a (col, row) coordinate
    :param i: index from 0-63 to be converted
    :return: (col, row) tuple from the index
    """
    return i % 8, i // 8


def coordinate_to_index(square: Tuple[int, int]) -> int:
    """
    Converts from a (col, row) coordinate to an index
    :param square: (col, row) tuple to be converted
    :return: index from 0-63
    """
    c, r = square
    return c + r * 8