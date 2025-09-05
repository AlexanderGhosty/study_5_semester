from app.lists_ops import (
    reverse_list, mutate_list, all_equal, slice_with_step, build_list, insert_at,
    merge_and_sort, odd_center_demo, extend_with_limit, sort_by_abs, sort_by_len,
    sort_case_insensitive, sort_even_first, sort_by_mapped_square,
    sort_words_by_vowel_count, sort_products_by_price_with_map, pop_min, make_matrix
)
from app.tuples_ops import tuple_concat, tuple_stats, types_of_tuple, tuple_contains
from app.dicts_ops import dict_pick, dict_flip, dict_sum_values, count_key_presence, deep_find


def run_all_demos() -> None:
    """Вызывает все функции шагов 1–18 последовательно (минимальные примеры)."""
    print("— Шаг 1:", reverse_list([1, 2, 3]))
    print("— Шаг 2:", mutate_list([1, 2, 3], delta=5, inplace=False))
    print("— Шаг 3:", all_equal([1, 2], [1, 2], [1, 2]))
    print("— Шаг 4:", slice_with_step([10, 20, 30, 40, 50], 1, None, 2))
    print("— Шаг 5:", build_list(3, 4, transform=lambda x: x * 10))
    print("— Шаг 6:", insert_at([1, 2, 3], 99, 1))
    print("— Шаг 7:", merge_and_sort([3, 1], [2, 2], reverse=False, unique=True))

    print("— Шаг 8:")
    odd_center_demo()

    base = [1, 2, 3]
    print("— Шаг 9:", extend_with_limit(base, [4, 5, 6, 7], limit=5, trim_from="head"))

    print("— Шаг 10a:", sort_by_abs([3, -1, -4, 2]))
    print("— Шаг 10b:", sort_by_len(["bbb", "a", "cc"]))
    print("— Шаг 10c:", sort_case_insensitive(["Bob", "alice", "AL"]))
    print("— Шаг 10d:", sort_even_first([5, 2, 8, 1, 3, 4]))
    print("— Шаг 10e (map):", sort_by_mapped_square([3, -2, 1, -4]))
    print("— Шаг 10f (map):", sort_words_by_vowel_count(["тест", "авиа", "дом", "идея"]))
    print("— Шаг 10g (map):", sort_products_by_price_with_map([("A", 99.0), ("b", 10.0), ("C", 10.0)]))

    nums = [5, 2, 9, 1]
    print("— Шаг 11 pop_min:", pop_min(nums), "остаток:", nums)

    print("— Шаг 12 concat:", tuple_concat((1, 2), (3,)))
    print("— Шаг 12 stats:", tuple_stats((5, 1, 4)))
    print("— Шаг 13 types:", types_of_tuple((1, "x", 3.14, True)))
    print("— Шаг 14 contains:", tuple_contains(("Alice", "bob"), "BOB", case_insensitive=True))

    print("— Шаг 15 matrix:", make_matrix([1, 2, 3], [4, 5], [6], width=4, fill=0))

    d = {"name": "Alice", "age": 30, "city": "SPB"}
    print("— Шаг 16 pick:", dict_pick(d, "name", "city"))
    print("— Шаг 16 flip:", dict_flip({"a": 1, "b": 2}))
    print("— Шаг 16 sum:", dict_sum_values({"x": 10, "y": 5}))

    print("— Шаг 17 count presence:",
          count_key_presence("name", {"name": 1}, {"age": 2}, {"name": 3, "city": 4}))

    nested = {
        "catalog": {
            "electronics": {
                "phones": {"best": "PX-10", "stock": 5},
                "laptops": {"best": "LX-5", "stock": 2},
            },
            "home": {"kitchen": {"best": "Mixer-2"}}
        }
    }
    print("— Шаг 18 path:", deep_find(nested, path=["catalog", "electronics", "phones", "best"]))
    print("— Шаг 18 target:", deep_find(nested, target_key="best"))

    print("\nВсе демонстрации завершены.")

if __name__ == "__main__":
    run_all_demos()
