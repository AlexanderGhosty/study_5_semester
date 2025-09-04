"""Функция, вызывающая другую функцию внутри себя."""
from __future__ import annotations
from math import hypot


def distance_between_points(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Расстояние между точками a и b по теореме Пифагора."""
    ax, ay = a
    bx, by = b
    return hypot(bx - ax, by - ay)


def perimeter_of_triangle(a: tuple[float, float],
                          b: tuple[float, float],
                          c: tuple[float, float]) -> float:
    """Периметр треугольника: вызывает distance_between_points трижды."""
    ab = distance_between_points(a, b)
    bc = distance_between_points(b, c)
    ca = distance_between_points(c, a)
    return ab + bc + ca
