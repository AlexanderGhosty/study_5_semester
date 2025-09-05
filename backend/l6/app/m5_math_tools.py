"""
Математические утилиты и вспомогательные функции.

Модуль содержит часто используемые математические функции:
- Вычисление расстояний в 2D пространстве
- Среднее квадратическое значение
- Безопасное сравнение чисел с плавающей точкой

Функции:
    - distance_2d: расчет евклидова расстояния между двумя точками
    - mean_sqrt: среднее арифметическое квадратных корней
    - safe_isclose: безопасное сравнение float значений
"""

from __future__ import annotations
import math
from typing import Iterable
from .m6_locale_tools import set_locale, format_currency  # демонстрация импорта вниз

def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
    """Дистанция через math.hypot."""
    return math.hypot(x2 - x1, y2 - y1)

def mean_sqrt(nums: Iterable[float]) -> float:
    """Среднее от корней значений: использует math.sqrt."""
    nums = list(nums)
    if not nums:
        return float("nan")
    return sum(math.sqrt(abs(x)) for x in nums) / len(nums)

def safe_isclose(a: float, b: float, rel_tol: float = 1e-9, abs_tol: float = 0.0) -> bool:
    """Сравнение с math.isclose для демонстрации доп. метода."""
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

# демонстрация взаимодействия с локалью
def demo_math_with_locale(amount_rub: float) -> str:
    """Комбинируем math и locale: округлим вверх и выведем валютой."""
    set_locale()  # текущая системная
    ceil_val = math.ceil(amount_rub)
    return format_currency(type("Tmp", (), {"amount": ceil_val, "currency": "RUB"})())  # mock
