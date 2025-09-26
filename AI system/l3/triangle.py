from __future__ import annotations

def almost_equal(x: float, y: float, eps: float = 1e-9) -> bool:
    return abs(x - y) <= eps

def triangle_type(a: float, b: float, c: float, eps: float = 1e-9) -> str:
    if a <= 0 or b <= 0 or c <= 0:
        return "Ошибка: стороны должны быть > 0."
    # Неравенство треугольника
    if not (a + b > c and a + c > b and b + c > a):
        return "Треугольник не существует (нарушено неравенство треугольника)."

    x, y, z = sorted([a, b, c])

    # Классификация по сторонам
    if almost_equal(a, b, eps) and almost_equal(b, c, eps):
        side_kind = "равносторонний"
    elif almost_equal(a, b, eps) or almost_equal(a, c, eps) or almost_equal(b, c, eps):
        side_kind = "равнобедренный"
    else:
        side_kind = "разносторонний"

    # Классификация по углам по теореме косинусов:
    x2, y2, z2 = x*x, y*y, z*z
    if almost_equal(z2, x2 + y2, eps):
        angle_kind = "прямоугольный"
    elif z2 < x2 + y2 - eps:
        angle_kind = "остроугольный"
    else:
        angle_kind = "тупоугольный"

    return f"{side_kind}-{angle_kind}"

def main():
    print("Определение типа треугольника")
    try:
        a = float(input("a = "))
        b = float(input("b = "))
        c = float(input("c = "))
    except ValueError:
        print("Ошибка ввода: ожидаются числа (float).")
        return
    print(triangle_type(a, b, c))

if __name__ == "__main__":
    main()
