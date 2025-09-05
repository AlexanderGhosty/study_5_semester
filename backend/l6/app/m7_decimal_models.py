"""
Модели данных для работы с точными денежными вычислениями.

Модуль содержит классы для безопасной работы с денежными значениями,
используя Decimal для избежания ошибок округления при работе с float.

Классы:
    - Money: класс для представления денежных сумм с валютой

Особенности:
    - Использование Decimal для точности вычислений
    - Поддержка различных валют
    - Безопасные математические операции
"""

from __future__ import annotations
from dataclasses import dataclass, replace
from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Iterable

getcontext().prec = 28  #  точность для денег

# ---------- data-классы ----------
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "RUB"

@dataclass(frozen=True)
class Item:
    sku: str
    name: str
    price: Money

@dataclass
class OrderLine:
    item: Item
    qty: int

# ---------- decimal-функции ----------
def dec_round(m: Money, ndigits: int = 2) -> Money:
    """Округление Decimal до ndigits банковским правилом."""
    q = Decimal(10) ** -ndigits
    return replace(m, amount=m.amount.quantize(q, rounding=ROUND_HALF_UP))

def dec_apply_percent(m: Money, percent: Decimal) -> Money:
    """Применение процентной надбавки/скидки к Money."""
    factor = (Decimal(1) + percent / Decimal(100))
    return replace(m, amount=(m.amount * factor))

def total_amount(lines: Iterable[OrderLine]) -> Money:
    """Вспомогательная: сумма по позициям (qty * price)."""
    total = sum((ol.item.price.amount * ol.qty for ol in lines), Decimal(0))
    if not lines:
        return Money(Decimal(0))
    currency = next(iter(lines)).item.price.currency
    return Money(total, currency)
