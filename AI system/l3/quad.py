from __future__ import annotations
import cmath

def solve_quadratic(a: float, b: float, c: float) -> str:
    """
    Возвращает человекочитаемую строку с описанием решения.
    Поддерживаются все случаи (вкл. комплексные корни при D<0).
    """
    if a == 0 and b == 0 and c == 0:
        return "Бесконечно много решений (тождество 0 = 0)."

    if a == 0:
        if b == 0:
            return "Решений нет (противоречие)."
        x = -c / b
        return f"Линейное уравнение: x = {x:g}"

    D = b*b - 4*a*c
    if D > 0:
        sqrtD = D**0.5
        x1 = (-b - sqrtD) / (2*a)
        x2 = (-b + sqrtD) / (2*a)
        return f"D = {D:g} > 0 → два корня: x1 = {x1:g}, x2 = {x2:g}"
    elif D == 0:
        x = -b / (2*a)
        return f"D = 0 → один корень (кратный): x = {x:g}"
    else:
        sqrtD = cmath.sqrt(D)
        x1 = (-b - sqrtD) / (2*a)
        x2 = (-b + sqrtD) / (2*a)
        return f"D = {D:g} < 0 → комплексные корни: x1 = {x1}, x2 = {x2}"

def main():
    print("Решение ax^2 + bx + c = 0")
    try:
        a = float(input("a = "))
        b = float(input("b = "))
        c = float(input("c = "))
    except ValueError:
        print("Ошибка ввода: ожидаются числа (float).")
        return
    print(solve_quadratic(a, b, c))

if __name__ == "__main__":
    main()
