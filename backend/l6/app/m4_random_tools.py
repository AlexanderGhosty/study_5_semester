"""
Инструменты для работы со случайными значениями и выборками.

Модуль предоставляет удобные функции для:
- Случайного выбора элементов из коллекций
- Получения уникальных случайных выборок
- Перемешивания списков на месте
- Генерации случайных блужданий

Функции:
    - pick_random: выбор случайного элемента
    - sample_unique: получение уникальной выборки
    - shuffle_inplace: перемешивание списка на месте
    - random_walk: генерация случайного блуждания
"""

from __future__ import annotations
import random
from typing import Iterable, Sequence
from .m5_math_tools import distance_2d  # демонстрация импорта вниз

def pick_random(items: Sequence[str]) -> str:
    """random.choice — выбрать случайный элемент."""
    if not items:
        raise ValueError("Пустая последовательность")
    return random.choice(items)

def sample_unique(items: Sequence[int], k: int) -> list[int]:
    """random.sample — уникальная выборка k элементов."""
    return random.sample(items, k=min(k, len(items)))

def shuffle_inplace(items: list[int]) -> list[int]:
    """Доп: random.shuffle — перемешивание на месте."""
    random.shuffle(items)
    return items

def random_walk(steps: int = 3) -> float:
    """Комбинируем с math: случайная «прогулка», возвращаем итоговую дистанцию от (0,0)."""
    x = y = 0.0
    for _ in range(steps):
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        x += dx; y += dy
    return distance_2d(0, 0, x, y)
