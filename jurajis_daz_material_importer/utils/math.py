from typing import TypeVar, Tuple
from typing import TypeVarTuple, Unpack

T = TypeVar('T', int, float)  # allow both ints and floats
Ts = TypeVarTuple('Ts')

def tuple_zip_sum(start: Tuple[Unpack[Ts]], *tuples: Tuple[T, ...]) -> Tuple[Unpack[Ts]]:
    """Element-wise addition of multiple numeric tuples with the same shape."""
    # noinspection PyTypeChecker
    return tuple(sum(values) for values in zip(start, *tuples))
