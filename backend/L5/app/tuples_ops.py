""" Функции с кортежами. """
from __future__ import annotations
from typing import Any

def tuple_concat(a: tuple[Any, ...], b: tuple[Any, ...]) -> tuple[Any, ...]:
    """
    Операция над кортежами: конкатенация.
    """
    return a + b

def tuple_stats(nums: tuple[int, ...]) -> tuple[int, int, float]:
    """
    Возвращает (min, max, average) по целочисленному кортежу.
    """
    if not nums:
        raise ValueError("Кортеж пуст")
    return (min(nums), max(nums), sum(nums) / len(nums))

def types_of_tuple(items: tuple[Any, ...]) -> tuple[type, ...]:
    """
    Формирует новый кортеж из типов элементов входного кортежа.
    """
    return tuple(type(x) for x in items)


def tuple_contains(items: tuple[Any, ...], value: Any, case_insensitive: bool = False) -> bool:
    """
    Проверяет наличие элемента в кортеже.
    Если case_insensitive=True, сравниваем строки без учёта регистра.
    """
    if case_insensitive:
        return any(
            (isinstance(x, str) and isinstance(value, str) and x.lower() == value.lower())
            or x == value for x in items
        )
    return value in items
