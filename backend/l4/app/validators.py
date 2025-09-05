"""Валидаторы для домена магазина."""

from __future__ import annotations
from typing import Iterable

def validate_quantity(qty: int) -> int:
    """
    Проверяет, что количество товара корректно.
    Требования:
      - >= 1
      - <= 1000 (условное ограничение склада)
    Исключения:
      - ValueError при некорректном значении.
    Обработчиков НЕТ — исключения идут наверх.
    """
    if not isinstance(qty, int):
        raise ValueError("Quantity must be int")
    if qty < 1:
        raise ValueError("Quantity must be >= 1")
    if qty > 1000:
        raise ValueError("Quantity must be <= 1000")
    return qty

def validate_sku(sku: str) -> str:
    """
    Валидирует артикул товара.
    Требования:
      - Строка длиной 3..32, из букв/цифр/дефисов.
    Исключения:
      - ValueError при некорректном значении.
    Обработчиков НЕТ — исключения идут наверх.
    """
    import re

    if not isinstance(sku, str):
        raise ValueError("SKU must be str")
    if not (3 <= len(sku) <= 32):
        raise ValueError("SKU length must be 3..32")
    if not re.fullmatch(r"[A-Za-z0-9\-]+", sku):
        raise ValueError("SKU must contain only letters, digits, hyphen")
    return sku

def normalize_prices(raw: Iterable[object]) -> list[float]:
    """
    Преобразует входные «цены» к списку float.
    - При любых ошибках парсинга ловим общий Exception,
      логируем и возвращаем только успешно распознанные элементы.
    - НИКАКОГО finally здесь.
    """
    normalized: list[float] = []
    try:
        for x in raw:
            # потенциальные ошибки: TypeError, ValueError, др.
            price = float(x)
            if price < 0:
                raise ValueError("Price must be >= 0")
            normalized.append(price)
    except Exception as e:  # ровно один общий обработчик
        print(f"[normalize_prices] Ошибка нормализации: {e}. Частичные данные сохранены.")
    return normalized

def compute_discount(total: float, promo: str | None) -> float:
    """
    Считает скидку по промокоду.
    - Бросает исключения при некорректном total/promo.
    - Ловит общий Exception, внутри — логика fallback.
    - В finally приводит результат к стабильному виду.
    """
    discount = 0.0
    tmp_resource_opened = False
    try:
        if total < 0:
            raise ValueError("Total must be >= 0")
        if promo is None:
            raise ValueError("Promo is required")

        # симуляция «ресурса»
        tmp_resource_opened = True

        promo = promo.strip().upper()
        if promo == "SALE10" and total >= 100:
            discount = total * 0.10
        elif promo == "VIP" and total >= 500:
            discount = 100.0
        else:
            raise LookupError("Promo not applicable")
    except Exception as e:
        print(f"[compute_discount] Ошибка расчёта скидки: {e}. Возвращаю 0.")
        discount = 0.0
    finally:
        # «Закрываем ресурс» и гарантируем нормальный возврат float
        if tmp_resource_opened:
            tmp_resource_opened = False
        discount = float(discount)
    return discount