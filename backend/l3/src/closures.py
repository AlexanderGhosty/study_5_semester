"""Примеры замыканий (3 шт.)."""
from __future__ import annotations
from typing import Callable, Any


def make_counter(start: int = 0) -> Callable[[], int]:
    """Возвращает счётчик, помнящий внутреннее состояние."""
    value = start

    def inc() -> int:
        nonlocal value
        value += 1
        return value

    return inc


def make_multiplier(k: float) -> Callable[[float], float]:
    """Возвращает функцию, умножающую аргумент на зафиксированный коэффициент k."""
    def mul(x: float) -> float:
        return x * k
    return mul


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """Простая мемоизация: кэширует результаты func по аргументам."""
    cache: dict[tuple[Any, ...], Any] = {}

    def wrapper(*args: Any) -> Any:
        if args in cache:
            return cache[args]
        res = func(*args)
        cache[args] = res
        return res

    return wrapper
