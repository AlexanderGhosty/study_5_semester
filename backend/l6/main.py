"""
Главный модуль для демонстрации функциональности всех созданных модулей.

Этот модуль импортирует и запускает функции из различных модулей:
- m1_catalog: демонстрация импорт-цепочек с промокодами
- m4_random_tools: инструменты для работы со случайными значениями
- m5_math_tools: математические утилиты
- m6_locale_tools: инструменты для работы с локализацией
- m7_decimal_models: модели для работы с денежными значениями
"""
from decimal import Decimal
from app.m1_catalog import demo_import_chain, demo_import_chain_with_promo
from app.m4_random_tools import pick_random, sample_unique, shuffle_inplace, random_walk
from app.m5_math_tools import distance_2d, mean_sqrt, safe_isclose
from app.m6_locale_tools import set_locale, format_currency, locale_sort
from app.m7_decimal_models import Money


def run_all() -> None:
    """Вызывает все функции из пунктов 2–9."""
    print("== Импорт-цепочка ==")
    total = demo_import_chain()
    print("total без промо:", total)

    total_promo = demo_import_chain_with_promo("VIP")
    print("total c VIP:", total_promo)

    print("\n== random ==")
    print("pick_random:", pick_random(["red", "green", "blue"]))
    print("sample_unique:", sample_unique([1,2,3,4,5], k=3))
    print("shuffle_inplace:", shuffle_inplace([1,2,3,4]))
    print("random_walk:", random_walk(steps=5))

    print("\n== math ==")
    print("distance_2d:", distance_2d(0,0,3,4))
    print("mean_sqrt:", mean_sqrt([1,4,9,16]))
    print("safe_isclose:", safe_isclose(0.1+0.2, 0.3, rel_tol=1e-9))

    print("\n== locale ==")
    loc = set_locale()  # ставим системную
    print("locale set to:", loc)
    print("format_currency:", format_currency(Money(Decimal("1234.56"), "RUB")))
    print("locale_sort:", locale_sort(["ёж", "Ель", "яблоко", "Юла"]))

    print("\nГoтoвo.")

if __name__ == "__main__":
    run_all()
