"""
Главный модуль для демонстрации функций работы со строками.
Содержит функцию run_all_strings_demo(), которая последовательно вызывает
все функции из модулей core_strings и extras_strings.
"""
# main.py
from app.core_strings import (
    render_profile_line, repeat_combo, count_substring_ci, slice_one_liner,
    detect_latin_homoglyphs, is_palindrome, normalize_spaces_length, sentence_to_lines,
)
from app.extras_strings import most_common_words, snake_to_camel, wrap_text


def run_all_strings_demo() -> None:
    """Последовательно вызывает все функции пунктов 1–9."""
    print("== Пункт 1 ==")
    print(render_profile_line("александр", 7, 5))

    print("\n== Пункт 2 ==")
    repeat_combo(["foo", "бар", "42"], times=3)

    print("\n== Пункт 3 ==")
    print("count_substring_ci('abracadabra','BRA') =", count_substring_ci("abracadabra", "BRA"))

    print("\n== Пункт 4 ==")
    print("slice_one_liner('hello world', 1, 5) =", slice_one_liner("hello world", 1, 5))

    print("\n== Пункт 5 ==")
    rows, cnt = detect_latin_homoglyphs("МОРОЗ И СОЛНЦЕ", "KOT и КОТ", "ТЕСТ", "MAMA МАМА")
    print("строки с латиницей:", rows, " | слов с латиницей:", cnt)

    print("\n== Пункт 6 ==")
    for s in ["А роза упала на лапу Азора", "123abcCBA321", "не палиндром"]:
        print(s, "->", is_palindrome(s))

    print("\n== Пункт 7 ==")
    s = "   Привет   мир    это   строка  "
    print("len after normalize =", normalize_spaces_length(s))

    print("\n== Пункт 8 ==")
    text = "Привет! Как дела?.. Хорошо. А у тебя?"
    print(sentence_to_lines(text))

    print("\n== Пункт 9 ==")
    print("most_common_words:", most_common_words("тест тест слово слово слово ещё ещё"))
    print("snake_to_camel:", snake_to_camel("user_display_name"))
    long_text = "Это пример ручной переноски текста по словам, чтобы показать алгоритм."
    print("wrap_text:\n", wrap_text(long_text, width=20))

    print("\nГотово: все функции вызваны без необработанных исключений.")


if __name__ == "__main__":
    run_all_strings_demo()
