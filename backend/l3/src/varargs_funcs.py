"""Примеры *args и **kwargs."""
from __future__ import annotations
from urllib.parse import urlencode


def sum_positive(*nums: float) -> float:
    """Суммирует только положительные числа из *nums."""
    return sum(n for n in nums if n > 0)


def build_url(base: str, **params: str) -> str:
    """Собирает URL с параметрами запроса из kwargs."""
    if not params:
        return base
    return f"{base}?{urlencode(params)}"
