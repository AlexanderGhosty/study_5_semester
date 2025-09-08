from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr

# ---- Базовые схемы запросов/ответов ----
class LoginForm(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=128)

class RegisterPayload(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

# ---- User (как «класс») ----
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str # в проде используют хэш
