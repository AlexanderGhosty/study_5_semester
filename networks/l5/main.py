"""main.py"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        print(f"received {data}")
        operand1 = float(data.get('operand1', 0))
        operation = data.get('operation')
        operand2 = float(data.get('operand2', 0)) if data.get('operand2') else None

        result = None

        # Выполнение операций
        if operation == "add":
            result = operand1 + operand2
        elif operation == "subtract":
            result = operand1 - operand2
        elif operation == "multiply":
            result = operand1 * operand2
        elif operation == "divide":
            if operand2 == 0:
                return jsonify({"error": "Division by zero"}), 400
            result = operand1 / operand2
        elif operation == "power":
            result = math.pow(operand1, operand2)
        elif operation == "root":
            if operand2 == 0:
                return jsonify({"error": "Root degree cannot be zero"}), 400
            if operand2 % 2 == 0 and operand1 < 0:
                return jsonify({"error": "Cannot extract even root from negative number"}), 400
            if operand1 < 0 and operand2 % 2 != 0:
                # Нечетный корень из отрицательного числа
                result = -math.pow(abs(operand1), 1 / operand2)
            else:
                result = math.pow(operand1, 1 / operand2)
        elif operation == "sin":
            result = math.sin(math.radians(operand1))
        elif operation == "cos":
            result = math.cos(math.radians(operand1))
        elif operation == "tan":
            # Проверяем критические точки (90°, 270°, etc.)
            angle_deg = operand1 % 360
            if abs(angle_deg - 90) < 1e-10 or abs(angle_deg - 270) < 1e-10:
                return jsonify({"error": "Tangent is undefined at 90° and 270°"}), 400
            result = math.tan(math.radians(operand1))
        elif operation == "cot":
            # Проверяем критические точки (0°, 180°, 360°, etc.)
            angle_deg = operand1 % 360
            if abs(angle_deg) < 1e-10 or abs(angle_deg - 180) < 1e-10 or abs(angle_deg - 360) < 1e-10:
                return jsonify({"error": "Cotangent is undefined at 0°, 180°, and 360°"}), 400
            result = 1 / math.tan(math.radians(operand1))
        else:
            return jsonify({"error": "Invalid operation"}), 400

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
