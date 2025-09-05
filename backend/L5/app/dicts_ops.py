""" Функции со словарями. """
from __future__ import annotations
from typing import Any

def dict_pick(d: dict[str, Any], *keys: str) -> dict[str, Any]:
    """
    Возвращает новый словарь только с указанными ключами, если они есть.
    """
    return {k: d[k] for k in keys if k in d}

def dict_flip(d: dict[Any, Any]) -> dict[Any, Any]:
    """
    Меняет местами ключи и значения (если значения хешируемые и уникальные).
    """
    flipped: dict[Any, Any] = {}
    for k, v in d.items():
        if v in flipped:
            # демонстрация поведения при конфликте
            continue
        flipped[v] = k
    return flipped

def dict_sum_values(d: dict[str, int]) -> int:
    """
    Возвращает сумму всех целочисленных значений словаря.
    """
    return sum(d.values())

def count_key_presence(key: str, *dicts_: dict[str, Any]) -> int:
    """
    Считает, в скольких словарях присутствует заданный ключ.
    """
    return sum(1 for d in dicts_ if key in d)

def deep_find(data: dict[str, Any], path: list[str] | tuple[str, ...] | None = None,
              target_key: str | None = None) -> Any | None:
    """
    Поиск в комплексном словаре c минимум 3 уровнями вложенности.
    Два режима:
      1) Если задан path (список ключей до самого глубокого уровня) — идём по пути.
      2) Если задан target_key — ищем в глубину ключ и возвращаем его значение при первом совпадении.
    Если не найдено — возвращаем None.
    """
    if path:
        cur: Any = data
        for k in path:
            if not isinstance(cur, dict) or k not in cur:
                return None
            cur = cur[k]
        return cur

    if target_key:
        # DFS
        stack: list[Any] = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if target_key in node:
                    return node[target_key]
                stack.extend(node.values())
        return None

    return None
