"""Базовые примеры функций: без параметров, с параметрами, с умолчаниями."""
from __future__ import annotations


def app_version() -> str:
    """Функция без параметров: возвращает версию приложения."""
    return "1.0.0"


def rectangle_area(width: float, height: float) -> float:
    """Функция с параметрами: площадь прямоугольника.

    :param width: ширина
    :param height: высота
    """
    return width * height


def greet(name: str, punctuation: str = "!", polite: bool = True) -> str:
    """Функция с несколькими параметрами со значениями по умолчанию.

    :param name: имя человека
    :param punctuation: завершающий знак
    :param polite: если True — вежливая форма
    """
    if polite:
        return f"Добрый день, {name}{punctuation}"
    return f"Привет, {name}{punctuation}"
