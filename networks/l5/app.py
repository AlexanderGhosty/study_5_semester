from flask import Flask, request, jsonify, send_from_directory
import math

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.post('/api/calc')
def api_calc():
    # Принимаем application/x-www-form-urlencoded
    op = (request.form.get('op') or '').strip().lower()
    op1_raw = (request.form.get('op1') or '').strip()
    op2_raw = (request.form.get('op2') or '').strip()

    def parse_float(val, name):
        try:
            return float(val)
        except Exception:
            raise ValueError(f"Поле '{name}' должно быть числом")

    # Какие операции бинарные, а какие унарные
    unary_ops = {'sin', 'cos', 'tan', 'cot'}
    binary_ops = {'add', 'sub', 'mul', 'div', 'pow', 'root'}

    if op not in unary_ops | binary_ops:
        return jsonify(ok=False, error="Неизвестная операция"), 400

    try:
        a = parse_float(op1_raw, 'op1')
        b = parse_float(op2_raw, 'op2') if op in binary_ops else None
    except ValueError as e:
        return jsonify(ok=False, error=str(e)), 400

    try:
        # Вычисления
        if op == 'add':
            result = a + b
        elif op == 'sub':
            result = a - b
        elif op == 'mul':
            result = a * b
        elif op == 'div':
            if b == 0:
                raise ZeroDivisionError('Деление на ноль невозможно')
            result = a / b
        elif op == 'pow':
            result = math.pow(a, b)
        elif op == 'root':
            # n‑ая корень из a: a ** (1/n)
            # Требуем целый n (b)
            if b == 0:
                raise ValueError('Степень корня (n) не должна быть нулём')
            # b должен быть целым
            if not float(b).is_integer():
                raise ValueError('Степень корня (n) должна быть целым числом')
            n = int(b)
            if a < 0 and n % 2 == 0:
                raise ValueError('Чётный корень из отрицательного числа не является вещественным')
            # Корректная обработка отрицательных для нечётного n
            if a < 0 and n % 2 == 1:
                result = -((-a) ** (1.0 / n))
            else:
                result = a ** (1.0 / n)
        elif op in unary_ops:
            # Угол в градусах
            rad = math.radians(a)
            eps = 1e-15
            if op == 'sin':
                result = math.sin(rad)
            elif op == 'cos':
                result = math.cos(rad)
            elif op == 'tan':
                # Неопределённость при cos≈0
                if abs(math.cos(rad)) < eps:
                    raise ValueError('tan не определён для этого угла (cos≈0)')
                result = math.tan(rad)
            elif op == 'cot':
                # cot = 1/tan, не определён при sin≈0
                if abs(math.sin(rad)) < eps:
                    raise ValueError('cot не определён для этого угла (sin≈0)')
                result = math.cos(rad) / math.sin(rad)
        else:
            raise ValueError('Неподдерживаемая операция')

        return jsonify(ok=True, result=result)

    except ZeroDivisionError as zde:
        return jsonify(ok=False, error=str(zde)), 400
    except ValueError as ve:
        return jsonify(ok=False, error=str(ve)), 400
    except Exception:
        return jsonify(ok=False, error='Внутренняя ошибка сервера'), 500


if __name__ == '__main__':
    # Запуск dev-сервера
    app.run(debug=True)