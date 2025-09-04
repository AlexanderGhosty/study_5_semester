"""Функции с несколькими параметрами и явными аннотациями типов."""
from __future__ import annotations
from typing import Tuple


def scale_point(x: float, y: float, factor: float) -> Tuple[float, float]:
    """Масштабирует точку (x, y) на коэффициент factor.

    :return: новая точка (x', y')
    """
    return x * factor, y * factor


def weighted_mean(a: float, b: float, wa: float, wb: float) -> float:
    """Взвешенное среднее двух чисел."""
    if wa + wb == 0:
        raise ValueError("Сумма весов не должна быть нулевой")
    return (a * wa + b * wb) / (wa + wb)
