"""
Лабораторная работа №2.
"""

from __future__ import annotations

def prompt_int(message: str) -> int:
    """Запрашивает целое число у пользователя с повтором до успешного ввода."""
    while True:
        raw = input(message)
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")

def menu() -> None:
    """Главное меню."""
    while True:
        print("\nМеню:")
        print("1) Классифицировать число (отрицательное/ноль/положительное, чёт/нечет)")
        print("2) Сумма чётных чисел в диапазоне")
        print("3) Факториал (итеративно и рекурсивно)")
        print("4) n-е число Фибоначчи")
        print("5) Деление: //, %, /")
        print("0) Выход")

        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            x = prompt_int("x = ")
            print(classify_number(x))
        elif choice == "2":
            lo = prompt_int("lo = ")
            hi = prompt_int("hi = ")
            print(f"sum_even = {sum_even(lo, hi)}")
        elif choice == "3":
            n = prompt_int("n = ")
            print(f"fact_iter({n}) = {fact_iter(n)}")
            print(f"fact_rec({n})  = {fact_rec(n)}")
        elif choice == "4":
            n = prompt_int("n = ")
            print(f"fib({n}) = {fib(n)}")
        elif choice == "5":
            a = prompt_int("a = ")
            b = prompt_int("b = ")
            try:
                q, r, d = div_ops(a, b)
                print(f"a // b = {q}, a % b = {r}, a / b = {d}")
            except ValueError as err:
                print(f"Ошибка: {err}")
        elif choice == "0":
            print("До встречи!")
            break
        else:
            print("Нет такого пункта меню.")

def classify_number(x: int) -> str:
    """Возвращает метку числа: negative|zero|positive и even|odd."""
    if x == 0:
        return "zero even"
    sign = "positive" if x > 0 else "negative"
    parity = "even" if x % 2 == 0 else "odd"
    return f"{sign} {parity}"

def sum_even(lo: int, hi: int) -> int:
    """Суммирует чётные числа в диапазоне [lo, hi]."""
    if lo > hi:
        lo, hi = hi, lo
    # приведём старт к чётному
    if lo % 2 != 0:
        lo += 1
    return sum(range(lo, hi + 1, 2))

def fact_iter(n: int) -> int:
    """Итеративный факториал n (n >= 0)."""
    if n < 0:
        raise ValueError("n must be >= 0")
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res

def fact_rec(n: int) -> int:
    """Рекурсивный факториал n (n >= 0)."""
    if n < 0:
        raise ValueError("n must be >= 0")
    return 1 if n in (0, 1) else n * fact_rec(n - 1)

def fib(n: int) -> int:
    """Возвращает n-е число Фибоначчи (n >= 0)."""
    if n < 0:
        raise ValueError("n must be >= 0")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def div_ops(a: int, b: int) -> tuple[int, int, float]:
    """Возвращает (a // b, a % b, a / b). Выбрасывает ValueError при b==0."""
    if b == 0:
        raise ValueError("деление на ноль")
    return (a // b, a % b, a / b)

def main() -> None:
    """Точка входа программы."""
    menu()

if __name__ == "__main__":
    main()
