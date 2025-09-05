"""Точка входа лабораторной №4 (исключения)."""

from app.validators import validate_quantity, validate_sku, normalize_prices, compute_discount
from app.services import reserve_stock, calc_shipping, call_payment_api, process_payment, checkout
from app.io_utils import read_text, parse_simple_csv, safe_div
from app.exceptions import ReportFormatError


def run_all_demos() -> None:
    """
    Последовательно вызывает все созданные функции.
    """
    print("== Шаг 1: функции без обработчиков ==")
    try:
        print("validate_quantity(5) ->", validate_quantity(5))
        print("validate_sku('ABC-001') ->", validate_sku("ABC-001"))
        # Демонстрация ошибки:
        # validate_quantity(0) 
    except Exception as e:
        print(f"[run_all_demos] Поймал исключение из шага 1: {e}")

    print("\n== Шаг 2: один обработчик Exception ==")
    print("normalize_prices(['10', 'x', -5, 2.5]) ->", normalize_prices(["10", "x", -5, 2.5]))

    print("\n== Шаг 3: один обработчик + finally ==")
    print("compute_discount(150, 'sale10') ->", compute_discount(150, "sale10"))
    print("compute_discount(80, 'sale10') ->", compute_discount(80, "sale10"))  # не применится

    print("\n== Шаг 4: несколько обработчиков разных типов ==")
    stock = {"ABC-001": 5, "XYZ-777": 1}
    reserve_stock(stock, "ABC-001", 2)   # ок
    reserve_stock(stock, "NO-SUCH", 1)   # KeyError
    reserve_stock(stock, "XYZ-777", 5)   # RuntimeError
    reserve_stock(stock, "ABC-001", -1)  # ValueError
    print("stock после операций ->", stock)

    print("calc_shipping('MSK', 2.5) ->", calc_shipping("MSK", 2.5))
    print("calc_shipping('LA', 1.0)  ->", calc_shipping("LA", 1.0))     # LookupError
    print("calc_shipping('SPB', 500) ->", calc_shipping("SPB", 500))    # OverflowError

    print("call_payment_api(100) ->", call_payment_api(100))

    print("\n== Шаг 5: функция сама генерирует и сама обрабатывает ==")
    print("process_payment('ORD123', 777) ->", process_payment("ORD123", 777))
    print("process_payment('O', 10)     ->", process_payment("O", 10))      # ValueError
    print("process_payment('ORD999', 100001) ->", process_payment("ORD999", 100001))  # PermissionError

    print("\n== Шаг 6/7: пользовательские исключения и их использование ==")
    cart = [("ABC-001", 2, 10.0), ("XYZ-777", 1, 999.0)]
    print("checkout(cart, budget=1200) ->", checkout(cart, budget=1200))  # ок
    print("checkout([], budget=1000)   ->", checkout([], budget=1000))    # CartEmptyError
    print("checkout(cart, budget=500)  ->", checkout(cart, budget=500))   # OutOfBudgetError

    print("\n== Шаг 8: дополнительные функции ==")
    print("read_text('no_such.txt') ->", repr(read_text("no_such.txt")))
    try:
        print("parse_simple_csv('a,b,c') ->", parse_simple_csv("a,b,c"))
        print("parse_simple_csv('a;b;c') ->", parse_simple_csv("a;b;c"))  # бросит ReportFormatError
    except ReportFormatError as e:
        print(f"[run_all_demos] Поймал ReportFormatError: {e}")
    print("safe_div(10, 0) ->", safe_div(10, 0))
    print("safe_div(10, 2) ->", safe_div(10, 2))

    print("\nВсе демо-вызовы завершены без необработанных исключений.")


if __name__ == "__main__":
    run_all_demos()
