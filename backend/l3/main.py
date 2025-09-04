"""Лабораторная работа №3."""
from src.simple_funcs import app_version, rectangle_area, greet
from src.typed_funcs import scale_point, weighted_mean
from src.varargs_funcs import sum_positive, build_url
from src.calls_other_funcs import perimeter_of_triangle
from src.hof_funcs import apply_twice, transform, keep_if
from src.local_funcs import normalize_text, sort_by_length
from src.lambdas_defs import now_unix, pair_to_str, timeit
from src.closures import make_counter, make_multiplier, memoize


def demo_calls() -> None:
    """Демонстрация различных функций."""
    # 1) без параметров
    print("version:", app_version())

    # 2) с параметрами
    print("rect area 3x4:", rectangle_area(3, 4))

    # 3) c умолчаниями
    print(greet("Александр"))
    print(greet("Александр", punctuation=".", polite=False))

    # 4) с аннотациями типов
    print("scale (1,2) * 3:", scale_point(1, 2, 3))
    print("weighted mean:", weighted_mean(10, 20, wa=1, wb=3))

    # 5) *args
    print("sum_positive:", sum_positive(-5, 1, 2.5, 0, 7))

    # 6) **kwargs
    print("url:", build_url("https://example.com", q="test", page="2"))

    # 7) функция вызывает функцию
    print("triangle perimeter:",
          perimeter_of_triangle((0, 0), (3, 0), (3, 4)))

    # 8) приём функции
    print("apply_twice:", apply_twice(lambda x: x * 2, 5))
    print("transform:", transform([1, 2, 3], lambda x: x + 10))
    print("keep_if:", keep_if(range(10), lambda x: x % 2 == 0))

    # 9) локальные функции
    print("normalize_text:", normalize_text("Hello, World. HELLO"))
    print("sort_by_length:", sort_by_length(["bbb", "a", "cc"]))

    # 10) лямбда без параметров
    print("now_unix:", now_unix())

    # 11) лямбда с параметрами
    print("pair_to_str:", pair_to_str(10, 20))

    # 12) функция, принимающая лямбду
    result, took = timeit(lambda x: x ** 2, 12345)
    print(f"timeit: result={result}, seconds={took:.6f}")

    # 13) замыкания
    counter = make_counter(5)
    print("counter:", counter(), counter(), counter())

    times3 = make_multiplier(3)
    print("times3(7):", times3(7))

    @memoize
    def slow_fib(n: int) -> int:
        if n < 2:
            return n
        return slow_fib(n - 1) + slow_fib(n - 2)

    print("fib(35) memoized:", slow_fib(35))


if __name__ == "__main__":
    demo_calls()
