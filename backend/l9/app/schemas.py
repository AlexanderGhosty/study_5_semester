from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field

# Users
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=3)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config:
        from_attributes = True

# Posts
class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    user_id: int

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    class Config:
        from_attributes = True
