"""Пользовательские исключения домена магазина."""

class CartEmptyError(Exception):
    """Корзина пуста."""

class OutOfBudgetError(Exception):
    """Покупка превышает бюджет пользователя."""

class ReportFormatError(Exception):
    """Неверный формат отчёта/файла для импорта."""
