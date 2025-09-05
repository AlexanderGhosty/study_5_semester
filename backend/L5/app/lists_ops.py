""" Функции со списками. """
from __future__ import annotations
from typing import Any, Callable, Iterable, Sequence
import random

def reverse_list(items: list[Any]) -> list[Any]:
    """
    Принимает список и возвращает перевёрнутый список.
    """
    return items[::-1]

def mutate_list(items: list[int], delta: int = 1, inplace: bool = False) -> list[int]:
    """
    Модифицирует одно/несколько/все значения списка.
    Параметры:
      - delta: на сколько увеличить каждый элемент
      - inplace: True — изменяем исходный список, False — возвращаем копию
    """
    target = items if inplace else items.copy()
    for i in range(len(target)):
        target[i] += delta
    return target

def all_equal(*lists: list[Any]) -> bool:
    """
    Сравнивает >=2 списков. Возвращает True, если все равны.
    """
    if len(lists) < 2:
        raise ValueError("Передайте два или более списков")
    first = lists[0]
    return all(lst == first for lst in lists[1:])

def slice_with_step(items: Sequence[Any], start: int | None, stop: int | None,
                    step: int = 1, safe: bool = True) -> list[Any]:
    """
    Возвращает диапазон значений из списка с заданным шагом.
    Учитываем ситуации: None, отрицательные индексы, step=0, выход за границы.
    - safe=True: корректируем step/границы «мягко».
    """
    if step == 0:
        if safe:
            step = 1
        else:
            raise ValueError("step не может быть 0")
    return list(items[slice(start, stop, step)])

def build_list(start: int = 0, count: int = 5, transform: Callable[[int], Any] | None = None) -> list[Any]:
    """
    Создаёт список на основе параметров.
    По умолчанию — последовательность start..start+count-1,
    опционально применяет transform к каждому элементу.
    """
    base = list(range(start, start + count))
    return list(map(transform, base)) if transform else base

def insert_at(items: list[Any], value: Any, pos: int) -> list[Any]:
    """
    Вставляет элемент в заданную позицию. Возвращает изменённый список (копию).
    """
    result = items.copy()
    if pos >= len(result):
        result.append(value)
    else:
        result.insert(pos, value)
    return result

def merge_and_sort(*lists: list[int], reverse: bool = False, unique: bool = False) -> list[int]:
    """
    Объединяет >=2 списков и сортирует.
    Параметры:
      - reverse: сортировка по убыванию
      - unique: оставить только уникальные элементы (порядок за счёт сортировки)
    """
    merged: list[int] = []
    for lst in lists:
        merged.extend(lst)
    if unique:
        merged = list(set(merged))
    return sorted(merged, reverse=reverse)

def odd_center_demo() -> None:
    """
    Создаём случайный список целых чисел произвольной длины.
    Пока длина чётная — сообщаем и генерируем новый.
    Когда длина нечётная — находим центральный элемент и считаем,
    сколько элементов имеют то же значение, что и центральный.
    Печатаем результаты (для демонстрации).
    """
    while True:
        size = random.randint(2, 10)   # произвольная длина
        nums = [random.randint(0, 5) for _ in range(size)]
        print(f"[odd_center_demo] создан список: {nums} (len={len(nums)})")
        if len(nums) % 2 == 0:
            print("[odd_center_demo] длина чётная — генерируем снова\n")
            continue
        mid = len(nums) // 2
        center = nums[mid]
        same_count = nums.count(center)
        print(f"[odd_center_demo] длина нечётная, центральный={center}, таких элементов={same_count}\n")
        break

def extend_with_limit(base: list[Any], *others: Iterable[Any], limit: int = 10,
                      trim_from: str = "tail") -> list[Any]:
    """
    Прибавляет к первому списку другие списки (в конец).
    Если длина > limit — обрезаем до лимита.
    Параметр trim_from: 'tail' (с конца) или 'head' (с начала).
    Мутируем base (по условию «прибавляем к первому»).
    """
    for it in others:
        base.extend(it)
    if len(base) > limit:
        overflow = len(base) - limit
        if trim_from == "tail":
            del base[-overflow:]
        else:
            del base[:overflow]
    return base

def sort_by_abs(nums: list[int]) -> list[int]:
    """Сортировка по модулю."""
    return sorted(nums, key=abs)

def sort_by_len(strings: list[str]) -> list[str]:
    """Сортировка строк по длине."""
    return sorted(strings, key=len)

def sort_case_insensitive(strings: list[str]) -> list[str]:
    """Сортировка строк без учёта регистра."""
    return sorted(strings, key=str.lower)

def sort_even_first(nums: list[int]) -> list[int]:
    """Чётные вперёд, внутри групп — по возрастанию."""
    return sorted(nums, key=lambda x: (x % 2, x))

# --- функции, использующие map() ---
def sort_by_mapped_square(nums: list[int]) -> list[int]:
    """Сортируем по квадратам значений (map для предрасчёта)."""
    mapped = list(map(lambda x: (x * x, x), nums))
    # сортировка по квадрату, возвращаем исходные x по порядку
    mapped.sort(key=lambda t: t[0])
    return [x for _, x in mapped]

def sort_words_by_vowel_count(words: list[str]) -> list[str]:
    """Сортировка слов по числу гласных."""
    vowels = set("aeiouyаеёиоуыэюя")
    def count_vowels(s: str) -> int:
        return sum(1 for ch in s.lower() if ch in vowels)
    mapped = list(map(lambda w: (count_vowels(w), w.lower(), w), words))
    mapped.sort(key=lambda t: (t[0], t[1]))
    return [orig for _, _, orig in mapped]

def sort_products_by_price_with_map(products: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """
    Сортируем список пар (имя, цена) по цене, затем по имени.
    map используется для предвычисления ключей.
    """
    mapped = list(map(lambda p: (p[1], p[0].lower(), p), products))
    mapped.sort(key=lambda t: (t[0], t[1]))
    return [orig for _, _, orig in mapped]

def pop_min(items: list[int]) -> int:
    """
    Извлекает с удалением минимальный элемент списка.
    Возвращает минимальный элемент.
    """
    if not items:
        raise ValueError("Список пуст")
    m = min(items)
    items.remove(m)
    return m

def make_matrix(*lists_: list[int], fill: int = 0, width: int | None = None) -> list[list[int]]:
    """
    Формирует «двумерный» список (матрицу) из переданных списков.
    Если width задан, каждая строка дополняется/обрезается до указанной ширины.
    """
    matrix: list[list[int]] = []
    if width is None:
        width = max((len(x) for x in lists_), default=0)
    for row in lists_:
        r = row[:width] + [fill] * max(0, width - len(row))
        matrix.append(r)
    return matrix
