"""Лямбда-выражения и функция, принимающая лямбду."""
from __future__ import annotations
import time
from typing import Any, Callable


# Лямбда без параметров
now_unix = lambda: int(time.time())  # noqa: E731  (сознательно лямбда, для задания)


# Лямбда с параметрами
pair_to_str = lambda a, b: f"({a}, {b})"  # noqa: E731


def timeit(func: Callable[..., Any], *args: Any, **kwargs: Any) -> tuple[Any, float]:
    """Принимает функцию (в т.ч. лямбду), вызывает её и возвращает (результат, секунды)."""
    start = time.perf_counter()
    res = func(*args, **kwargs)
    dur = time.perf_counter() - start
    return res, dur
