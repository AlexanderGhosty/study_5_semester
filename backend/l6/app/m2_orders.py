from __future__ import annotations
from dataclasses import replace
from decimal import Decimal
from typing import Iterable, Dict, List
from .m3_pricing import calc_order_total, make_order_line
from .m7_decimal_models import Money, Item, OrderLine, total_amount

def build_cart(items: Iterable[Item]) -> list[OrderLine]:
    """(9.2) Работа со списком объектов: строим корзину по 1 шт. каждого товара."""
    return [OrderLine(item=i, qty=1) for i in items]

def index_by_sku(items: Iterable[Item]) -> dict[str, Item]:
    """(9.3) Словарь sku -> Item."""
    return {i.sku: i for i in items}

def change_line_qty(line: OrderLine, new_qty: int) -> OrderLine:
    """(9.4) Модификация значения объекта data-класса (qty)."""
    line.qty = max(1, new_qty)
    return line

def create_item(sku: str, name: str, price: Decimal, currency: str = "RUB") -> Item:
    """(9.5) Создание объекта data-класса на основе обычных параметров."""
    return Item(sku=sku, name=name, price=Money(price, currency))

def checkout(lines: list[OrderLine], promo: str | None) -> Money:
    """Финальный расчёт, использует m3."""
    return calc_order_total(lines, promo)
