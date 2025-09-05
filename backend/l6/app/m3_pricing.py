"""
Модуль для расчета цен и применения скидок.

Содержит функции для работы с ценообразованием:
- Применение скидок по промокодам
- Создание позиций заказа
- Случайный выбор промокодов
- Расчет общей стоимости заказа с учетом скидок

Функции:
    - price_with_discount: применение скидки по промокоду
    - make_order_line: создание позиции заказа
    - choose_random_promo: случайный выбор промокода
    - calc_order_total: расчет итоговой стоимости заказа
"""

from __future__ import annotations
from decimal import Decimal
from typing import Iterable
from .m4_random_tools import pick_random  # демонстрация глубины импортов
from .m7_decimal_models import Money, Item, OrderLine, dec_apply_percent, dec_round, total_amount

def price_with_discount(m: Money, promo: str | None) -> Money:
    """Применяем скидку: VIP=-10%, SALE5=-5%, иначе без изменений."""
    if promo is None:
        return m
    promo = promo.strip().upper()
    mapping = {"VIP": Decimal("-10"), "SALE5": Decimal("-5")}
    percent = mapping.get(promo, Decimal("0"))
    return dec_round(dec_apply_percent(m, percent), 2)

def make_order_line(item: Item, qty: int) -> OrderLine:
    """Создаём позицию заказа (9.1)."""
    return OrderLine(item=item, qty=qty)

def choose_random_promo() -> str | None:
    """Используем random-модуль косвенно (через m4): выбор промо или None."""
    return pick_random(["VIP", "SALE5", None])

def calc_order_total(lines: Iterable[OrderLine], promo: str | None) -> Money:
    """Итог по заказу с учётом промо."""
    total = total_amount(lines)
    return price_with_discount(total, promo)
