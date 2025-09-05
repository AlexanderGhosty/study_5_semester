"""
Модуль для демонстрации импорт-цепочек и применения промокодов.

Содержит функции для расчета общей стоимости товаров с возможностью
применения различных типов промокодов (скидки, фиксированные суммы).

Функции:
    - demo_import_chain: базовый расчет стоимости товаров
    - demo_import_chain_with_promo: расчет с применением промокода
"""

from __future__ import annotations
from decimal import Decimal
from .m2_orders import build_cart, index_by_sku, change_line_qty, create_item, checkout
from .m7_decimal_models import Money, Item

def seed_items() -> list[Item]:
    """Создаём небольшой каталог."""
    return [
        create_item("SKU-1", "Телефон", Decimal("19990.00")),
        create_item("SKU-2", "Наушники", Decimal("2990.00")),
        create_item("SKU-3", "Чехол", Decimal("790.00")),
    ]

def demo_import_chain() -> Money:
    """Демонстрация цепочки импортов m1→m2→m3→m4→m5→m6→m7."""
    items = seed_items()
    cart = build_cart(items)
    # измеим одну позицию
    change_line_qty(cart[0], 2)
    # проверим индекс по sku
    _idx = index_by_sku(items)
    # расчёт без промо
    total = checkout(cart, promo=None)
    return total

def demo_import_chain_with_promo(promo: str) -> Money:
    """Демонстрация расчёта с промо."""
    items = seed_items()
    cart = build_cart(items)
    return checkout(cart, promo=promo)
