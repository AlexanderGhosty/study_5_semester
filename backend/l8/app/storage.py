from __future__ import annotations
from typing import List, Optional
from .models import User

# Храним данные в памяти вместо БД (для упрощения)
USERS: List[User] = [
    User(id=1, username="alice", email="alice@example.com", password="alicepwd"),
    User(id=2, username="bob", email="bob@example.com", password="bobpwd"),
]

def get_user_by_id(uid: int) -> Optional[User]:
    for u in USERS:
        if u.id == uid:
            return u
    return None

def add_user(u: User) -> None:
    USERS.append(u)

def next_user_id() -> int:
    return max((u.id for u in USERS), default=0) + 1
