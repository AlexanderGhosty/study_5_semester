"""
Инструменты для работы с локализацией и форматированием.

Модуль предоставляет функции для работы с различными локалями:
- Установка системной локали
- Форматирование денежных сумм согласно локали
- Сортировка строк с учетом правил локали

Функции:
    - set_locale: установка локали операционной системы
    - format_currency: форматирование денежных значений
    - locale_sort: сортировка с учетом локали
"""

from __future__ import annotations
import locale
from typing import Iterable
from .m7_decimal_models import Money, dec_round

def set_locale(loc: str | None = None) -> str:
    """Устанавливаем локаль; возвращаем фактическую строку локали."""
    try:
        return locale.setlocale(locale.LC_ALL, loc or "")
    except locale.Error:
        return locale.setlocale(locale.LC_ALL, "C")

def format_currency(m: Money) -> str:
    """Форматирование валюты через locale.currency, после безопасного округления."""
    m2 = dec_round(m, 2)
    return locale.currency(float(m2.amount), grouping=True, international=(m2.currency != "RUB"))

def locale_sort(strings: Iterable[str]) -> list[str]:
    """Сортировка с учётом локали с помощью locale.strxfrm."""
    key = locale.strxfrm
    return sorted(strings, key=key)
