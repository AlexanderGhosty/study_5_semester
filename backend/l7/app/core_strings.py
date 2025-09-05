"""
Модуль core_strings содержит основные функции для работы со строками:
- форматирование строк и профилей
- поиск подстрок
- работа с палиндромами
- нормализация пробелов
- обработка предложений
"""
from __future__ import annotations
from typing import Iterable, Tuple, List
import re

def _greet(name: str) -> str:
    return f"Привет, {name.strip().title()}!"

def render_profile_line(name: str, a: int, b: int) -> str:
    """
    Внутри есть шаблон строки, куда подставляем:
      - строковый параметр (name)
      - результат арифм. операции (a + b)
      - результат вызова другой функции (_greet)
    Возвращаем финальную строку.
    """
    template = "{hello} Сумма ваших чисел {x} и {y} равна {s}."
    return template.format(hello=_greet(name), x=a, y=b, s=a + b)

def repeat_combo(lines: Iterable[str], times: int) -> None:
    """
    Формируем строку из повторений комбинации других строк и
    выводим каждые повторения на новой строке.
    """
    combo = " | ".join(str(s) for s in lines)
    for i in range(times):
        print(f"{i+1:02d}: {combo}")

def count_substring_ci(haystack: str, needle: str) -> int:
    """
    Считает количество вхождений подстроки без учёта регистра.
    """
    if not needle:
        return 0
    return haystack.lower().count(needle.lower())

def slice_one_liner(s: str, i: int, j: int) -> str:
    """
    Выводит подстроку между индексами i и j.
    Условие: 0 < i < j < len(s) - 1.
    Тело — В ОДНУ строку.
    """
    return s[i:j] if (0 < i < j < len(s) - 1) else ""

# Латинские буквы, визуально схожие с кириллицей (гомоглифы)
_LATIN_HOMO = set("AaBCcEeHKkMmOoPpTtXx")

def detect_latin_homoglyphs(*texts: str) -> Tuple[List[str], int]:
    """
    Принимает произвольное число строк (кириллица, возможны латинские гомоглифы).
    Ищет слова, внутри которых есть ЛАТИНСКИЕ буквы (из набора _LATIN_HOMO).
    Возвращает:
      - список исходных строк, где обнаружены такие слова,
      - количество САМИХ слов с латинскими буквами (минимум одна латинская буква в слове).
    """
    re_word = re.compile(r"[A-Za-zА-Яа-яЁё]+", re.UNICODE)
    strings_with_latin: list[str] = []
    words_with_latin_count = 0

    for text in texts:
        found_in_this = False
        for w in re_word.findall(text):
            if any(ch in _LATIN_HOMO for ch in w):
                words_with_latin_count += 1
                found_in_this = True
        if found_in_this:
            strings_with_latin.append(text)
    return strings_with_latin, words_with_latin_count

def is_palindrome(s: str) -> bool:
    """
    Определяет, является ли строка палиндромом (буквы/цифры).
    Игнорируем регистр и неалфанумерик.
    """
    only = [ch.lower() for ch in s if ch.isalnum()]
    return only == only[::-1]

def normalize_spaces_length(s: str) -> int:
    """
    Убираем все лишние пробелы:
      - в начале/конце — полностью
      - между словами — оставляем один пробел
    Возвращаем длину строки после нормализации.
    """
    normalized = " ".join(s.split())
    return len(normalized)

def sentence_to_lines(text: str) -> str:
    """
    Заменяем символы окончания предложения (., !, ?, … и их группы)
    на перевод строки. Лишние пробелы вокруг убираем.
    """
    # Заменим группы .!?… (включая сочетания) на один \n
    result = re.sub(r"[\.!\?…]+", "\n", text)
    # Уберём лишние пробелы у краёв каждой строки
    result = "\n".join(part.strip() for part in result.split("\n"))
    # Удалим пустые строки, возникшие из подряд идущих знаков
    result = "\n".join(line for line in result.split("\n") if line)
    return result
