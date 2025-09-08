"""
Модели данных для FastAPI приложения.

Содержит Pydantic модели для валидации запросов и ответов.
"""
from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr


# ---- Базовые схемы запросов/ответов ----

class LoginForm(BaseModel):
    """Форма для аутентификации пользователя."""

    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=128)


class RegisterPayload(BaseModel):
    """Данные для регистрации нового пользователя."""

    username: str = Field(min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


# ---- User (как «класс») ----

class User(BaseModel):
    """Модель пользователя системы."""

    id: int
    username: str
    email: EmailStr
    password: str  # в проде используют хэш
