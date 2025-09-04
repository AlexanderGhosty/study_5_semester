"""Функции, принимающие функцию как параметр (3 примера)."""
from __future__ import annotations
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def apply_twice(func: Callable[[T], T], x: T) -> T:
    """Применяет функцию дважды к значению x."""
    return func(func(x))


def transform(data: Iterable[T], f: Callable[[T], U]) -> list[U]:
    """Преобразует элементы data функцией f (аналог map)."""
    return [f(item) for item in data]


def keep_if(data: Iterable[T], pred: Callable[[T], bool]) -> list[T]:
    """Оставляет элементы, для которых предикат pred возвращает True (аналог filter)."""
    return [item for item in data if pred(item)]
