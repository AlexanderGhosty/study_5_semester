"""
Модуль аутентификации и авторизации.

Содержит функции для работы с JWT токенами.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError

SECRET = "dev-secret-change-me"
ALGO = "HS256"
ACCESS_MIN = 30


def create_access_token(sub: str, minutes: int = ACCESS_MIN) -> str:
    """Создает JWT access токен для пользователя."""
    now = datetime.now(tz=timezone.utc)
    payload = {"sub": sub, "iat": int(now.timestamp()), "exp": int((now + timedelta(minutes=minutes)).timestamp())}
    return jwt.encode(payload, SECRET, algorithm=ALGO)


def verify_token(token: str) -> Optional[str]:
    """Проверяет JWT токен и возвращает subject (username) или None."""
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        return data.get("sub")
    except JWTError:
        return None
