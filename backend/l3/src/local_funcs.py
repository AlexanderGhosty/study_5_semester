"""Примеры локальных (вложенных) функций."""
from __future__ import annotations


def normalize_text(text: str) -> list[str]:
    """Нормализует строку: токенизация + приведение к нижнему регистру.

    Внутри объявляются локальные функции tokenize() и norm().
    """
    def tokenize(s: str) -> list[str]:
        return [t for t in s.replace(",", " ").replace(".", " ").split() if t]

    def norm(tokens: list[str]) -> list[str]:
        return [t.lower() for t in tokens]

    return norm(tokenize(text))


def sort_by_length(words: list[str]) -> list[str]:
    """Сортирует слова по длине с использованием локальной функции key_fn()."""
    def key_fn(w: str) -> int:
        return len(w)

    return sorted(words, key=key_fn)
