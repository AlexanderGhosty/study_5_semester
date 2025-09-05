"""
Модуль extras_strings содержит дополнительные функции для работы со строками:
- поиск самых частых слов
- преобразование snake_case в camelCase
- перенос текста по заданной ширине
"""

from __future__ import annotations
import re
from collections import Counter

def most_common_words(text: str, top_k: int = 3) -> list[tuple[str, int]]:
    """
    Находит top_k самых частых слов (регистр игнорируем).
    Словом считаем последовательности букв/цифр, длина >=2.
    """
    tokens = re.findall(r"[A-Za-zА-Яа-яЁё0-9]{2,}", text.lower())
    cnt = Counter(tokens)
    return cnt.most_common(top_k)

def snake_to_camel(s: str) -> str:
    """
    Преобразование snake_case -> camelCase (напр., user_name -> userName).
    """
    parts = s.strip("_").split("_")
    if not parts:
        return ""
    head, *tail = parts
    return head.lower() + "".join(p.capitalize() for p in tail)

def wrap_text(text: str, width: int = 16) -> str:
    """
    Ручная «переноска» по словам на заданную ширину.
    Не разрывает слова, переносит по пробелам.
    """
    words = text.split()
    lines: list[str] = []
    buf: list[str] = []
    cur_len = 0
    for w in words:
        add = len(w) + (1 if buf else 0)
        if cur_len + add > width:
            lines.append(" ".join(buf))
            buf = [w]
            cur_len = len(w)
        else:
            buf.append(w)
            cur_len += add
    if buf:
        lines.append(" ".join(buf))
    return "\n".join(lines)
