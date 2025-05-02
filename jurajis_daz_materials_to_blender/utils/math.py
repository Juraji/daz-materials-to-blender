import math
from itertools import zip_longest
from typing import TypeVar, Tuple, TypeVarTuple

T = TypeVar('T', int, float)  # allow both ints and floats
Ts = TypeVarTuple('Ts')


def tuple_zip_sum(base: Tuple[T, ...], *tuples: Tuple[T, ...]) -> Tuple[T, ...]:
    """Element-wise addition of multiple numeric tuples with the same shape as `start`.
    Missing values are treated as 0.0 (neutral for addition)."""
    # noinspection PyArgumentList
    return tuple(
        sum(values)
        for values in zip_longest(base, *tuples, fillvalue=0.0)
    )


def tuple_zip_mult(base: Tuple[T, ...], *tuples: Tuple[T, ...]) -> Tuple[T, ...]:
    """Element-wise addition of multiple numeric tuples with the same shape as `start`.
    Missing values are treated as 1.0 (neutral for multiplication)."""
    # noinspection PyArgumentList
    return tuple(
        math.prod(values)
        for values in zip_longest(base, *tuples, fillvalue=1.0)
    )
