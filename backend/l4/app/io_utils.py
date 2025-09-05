"""IO-утилиты для демонстрации исключений."""
from __future__ import annotations
from pathlib import Path
from .exceptions import ReportFormatError

def read_text(path: str) -> str:
    """
    Читает текстовый файл.
    Обрабатывает:
      - FileNotFoundError — информируем
      - PermissionError — информируем
    """
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"[read_text] Файл не найден: {path}")
        return ""
    except PermissionError:
        print(f"[read_text] Нет прав на чтение: {path}")
        return ""

def parse_simple_csv(line: str) -> list[str]:
    """
    Наивный парсер CSV одной строки.
    Бросает ReportFormatError при пустой строке или неверном разделителе.
    """
    if not line:
        raise ReportFormatError("Пустая строка отчёта")
    if ";" in line:  # формат должен быть запятая
        raise ReportFormatError("Ожидалась запятая, найден ';'")
    return [x.strip() for x in line.split(",")]

def safe_div(a: float, b: float) -> float | None:
    """
    Безопасное деление.
    Обрабатывает ZeroDivisionError и возвращает None.
    """
    try:
        return a / b
    except ZeroDivisionError:
        print("[safe_div] Деление на ноль — возвращаю None.")
        return None
