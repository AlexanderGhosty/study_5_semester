from __future__ import annotations

def f(x: float) -> float:
    return x**3 - 4*x + 1

def main():
    print("Табулирование f(x) на [A, B] с шагом H")
    try:
        A = float(input("A = "))
        B = float(input("B = "))
        H = float(input("H = "))
    except ValueError:
        print("Ошибка ввода: ожидаются числа (float).")
        return

    if H == 0:
        print("Шаг H не может быть нулевым.")
        return
    if (B - A) * H < 0:
        print("Знак H должен соответствовать направлению от A к B.")
        return

    # Заголовок таблицы
    print("-" * 27)
    print(f"| {'x':>10} | {'f(x)':>10} |")
    print("-" * 27)

    x = A
    def done(x, B, H):
        return x > B + 1e-12 if H > 0 else x < B - 1e-12

    while not done(x, B, H):
        y = f(x)
        print(f"| {x:>10.4f} | {y:>10.4f} |")
        x += H

    print("-" * 27)

if __name__ == "__main__":
    main()
