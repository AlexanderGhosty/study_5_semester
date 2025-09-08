"""
Хранилище данных для FastAPI приложения.

Простое in-memory хранилище пользователей вместо базы данных.
"""
from __future__ import annotations
from typing import List, Optional
from .models import User

# Храним данные в памяти вместо БД (для упрощения)

USERS: List[User] = [
    User(id=1, username="alice", email="alice@example.com", password="alicepwd"),
    User(id=2, username="bob", email="bob@example.com", password="bobpwd"),
]


def get_user_by_id(uid: int) -> Optional[User]:
    """Получает пользователя по его ID."""
    for user in USERS:
        if user.id == uid:
            return user
    return None


def add_user(user: User) -> None:
    """Добавляет пользователя в хранилище."""
    USERS.append(user)


def next_user_id() -> int:
    """Возвращает следующий доступный ID для пользователя."""
    return max((user.id for user in USERS), default=0) + 1
