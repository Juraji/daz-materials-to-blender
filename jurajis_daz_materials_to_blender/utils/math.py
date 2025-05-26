import math
from itertools import zip_longest
from typing import TypeVar, Tuple, overload

T = TypeVar('T', int, float)  # allow both ints and floats


@overload
def tuple_zip_sum(base: tuple[T, T, T], *tuples: Tuple[T, T, T]) -> tuple[T, T, T]: ...


@overload
def tuple_zip_sum(base: tuple[T, T, T, T], *tuples: Tuple[T, T, T, T]) -> tuple[T, T, T, T]: ...


def tuple_zip_sum(base: Tuple[T, ...], *tuples: Tuple[T, ...]) -> Tuple[T, ...]:
    """
    Element-wise addition of multiple numeric tuples with the same shape as `start`.
    Missing values are treated as 0.0 (neutral for addition).
    """
    # noinspection PyArgumentList
    return tuple(
        sum(values)
        for values in zip_longest(base, *tuples, fillvalue=0.0)
    )


@overload
def tuple_zip_prod(base: tuple[T, T, T], *tuples: Tuple[T, T, T]) -> tuple[T, T, T]: ...


@overload
def tuple_zip_prod(base: tuple[T, T, T, T], *tuples: Tuple[T, T, T, T]) -> tuple[T, T, T, T]: ...


def tuple_zip_prod(base: Tuple[T, ...], *tuples: Tuple[T, ...]) -> Tuple[T, ...]:
    """
    Element-wise addition of multiple numeric tuples with the same shape as `start`.
    Missing values are treated as 1.0 (neutral for multiplication).
    """
    # noinspection PyArgumentList
    return tuple(
        math.prod(values)
        for values in zip_longest(base, *tuples, fillvalue=1.0)
    )


@overload
def tuple_zip_div(base: tuple[T, T, T], *tuples: Tuple[T, T, T]) -> tuple[T, T, T]: ...


@overload
def tuple_zip_div(base: tuple[T, T, T, T], *tuples: Tuple[T, T, T, T]) -> tuple[T, T, T, T]: ...


def tuple_zip_div(base: Tuple[T, ...], *tuples: Tuple[T, ...]) -> Tuple[T, ...]:
    """
    Element-wise division of multiple numeric tuples with the same shape as `start`.
    Missing values are treated as 1.0 (neutral for multiplication).
    """

    def div_chain(start, divisors):
        for d in divisors:
            start /= d
        return start

    # noinspection PyArgumentList
    return tuple(
        div_chain(v0, others)
        for v0, *others in zip_longest(base, *tuples, fillvalue=1.0)
    )


@overload
def tuple_zip_sub(base: tuple[T, T, T], *tuples: Tuple[T, T, T]) -> tuple[T, T, T]: ...


@overload
def tuple_zip_sub(base: tuple[T, T, T, T], *tuples: Tuple[T, T, T, T]) -> tuple[T, T, T, T]: ...


def tuple_zip_sub(base: tuple[T, ...], *tuples: tuple[T, ...]) -> tuple[T, ...]:
    """
    Element-wise subtraction of multiple numeric tuples with the same shape as `start`.
    Missing values are treated as 0.0 (neutral for subtraction).
    """

    def sub_chain(start, subtractors):
        for d in subtractors:
            start -= d
        return start

    # noinspection PyArgumentList
    return tuple(
        sub_chain(v0, others)
        for v0, *others in zip_longest(base, *tuples, fillvalue=0.0)
    )


@overload
def tuple_prod(base: tuple[T, T, T], product: T) -> tuple[T, T, T]: ...


@overload
def tuple_prod(base: tuple[T, T, T, T], product: T) -> tuple[T, T, T, T]: ...


def tuple_prod(base: tuple[T, ...], product: T):
    """Element-wise multiplication of numeric tuple."""
    return tuple(value * product for value in base)


@overload
def tuple_mod(base: tuple[T, T, T], product: T) -> tuple[T, T, T]: ...


@overload
def tuple_mod(base: tuple[T, T, T, T], product: T) -> tuple[T, T, T, T]: ...


def tuple_mod(base: Tuple[T, ...], mod: T) -> Tuple[T, ...]:
    """Element-wise modulus of numeric tuple."""
    return tuple(value % mod for value in base)
