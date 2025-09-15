from __future__ import annotations
from typing import Iterable
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from .models import User, Post

# --- Добавление данных ---
def add_users(db: Session, users: list[tuple[str, str, str]]) -> None:
    """
    users: список кортежей (username, email, password)
    """
    for u, e, p in users:
        db.add(User(username=u, email=e, password=p))
    db.commit()

def add_posts(db: Session, posts: list[tuple[str, str, int]]) -> None:
    """
    posts: список кортежей (title, content, user_id)
    """
    for t, c, uid in posts:
        db.add(Post(title=t, content=c, user_id=uid))
    db.commit()

# --- Извлечение данных ---
def get_all_users(db: Session) -> list[User]:
    return list(db.scalars(select(User)).all())

def get_all_posts_with_users(db: Session) -> list[tuple[Post, User]]:
    stmt = select(Post, User).join(User, Post.user_id == User.id)
    return list(db.execute(stmt).all())

def get_posts_by_username(db: Session, username: str) -> list[Post]:
    stmt = select(Post).join(User).where(User.username == username)
    return list(db.scalars(stmt).all())

# --- Обновление данных ---
def update_user_email(db: Session, username: str, new_email: str) -> int:
    stmt = update(User).where(User.username == username).values(email=new_email).execution_options(synchronize_session="fetch")
    res = db.execute(stmt)
    db.commit()
    return res.rowcount or 0

def update_post_content(db: Session, post_id: int, new_content: str) -> int:
    stmt = update(Post).where(Post.id == post_id).values(content=new_content).execution_options(synchronize_session="fetch")
    res = db.execute(stmt)
    db.commit()
    return res.rowcount or 0

# --- Удаление данных ---
def delete_post(db: Session, post_id: int) -> int:
    stmt = delete(Post).where(Post.id == post_id)
    res = db.execute(stmt)
    db.commit()
    return res.rowcount or 0

def delete_user_and_posts(db: Session, username: str) -> int:
    user = db.scalar(select(User).where(User.username == username))
    if not user:
        return 0
    db.delete(user)
    db.commit()
    return 1
