"""
FastAPI приложение для демонстрации основных возможностей.

Включает в себя работу с параметрами, JSON, файлами, авторизацией и JWT.
"""
from __future__ import annotations
from typing import List
from io import StringIO

from fastapi import FastAPI, Request, Response, Depends, Query, Path, Form, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, RedirectResponse

from .models import User, RegisterPayload
from .storage import USERS, get_user_by_id, add_user, next_user_id
from .auth import create_access_token, verify_token


app = FastAPI(title="Lab08 FastAPI Demo", version="1.0.0")

# ---- БАЗОВОЕ API ----

@app.get("/", summary="Hello World")
async def root():
    """Возвращает приветственное сообщение."""
    return {"message": "Hello, World!"}


# ---- ПАРАМЕТРЫ ----

@app.get("/greet/{name}", summary="Параметр пути")
async def greet(name: str = Path(..., min_length=1)):
    """Приветствует пользователя по имени из параметра пути."""
    return {"message": f"Hello, {name}!"}


@app.get("/search", summary="Параметр строки запроса")
async def search(query: str = Query(..., min_length=1)):
    """Возвращает результат поиска по query параметру."""
    return {"message": f"You searched for: {query}"}


# ---- РАЗНЫЕ ТИПЫ ДАННЫХ ----

@app.get("/json", summary="JSON с данными о себе")
async def json_me():
    """Возвращает JSON с персональными данными."""
    return {"name": "Александр", "age": 21, "hobbies": ["Go", "Python", "Cycling"]}


@app.get("/file", response_class=StreamingResponse, summary="Отправка текстового файла")
async def file_download():
    """Генерирует и отправляет текстовый файл для скачивания."""
    text = "Это содержимое сгенерированного текстового файла.\nЛР FastAPI."
    file_obj = StringIO(text)
    response_headers = {"Content-Disposition": 'attachment; filename="sample.txt"'}
    return StreamingResponse(file_obj, media_type="text/plain; charset=utf-8", headers=response_headers)


@app.get("/redirect", summary="Редирект на /")
async def redirect_to_root():
    """Перенаправляет пользователя на главную страницу."""
    return RedirectResponse(url="/")


# ---- ЗАГОЛОВКИ И КУКИ ----

@app.get("/headers", summary="Вернуть заголовки запроса")
async def get_headers(request: Request):
    """Возвращает все заголовки HTTP запроса."""
    return JSONResponse(dict(request.headers))


@app.get("/set-cookie", summary="Установить cookie username=your_name")
async def set_cookie(response: Response):
    """Устанавливает cookie с именем пользователя."""
    response.set_cookie(key="username", value="your_name", httponly=True, samesite="lax")
    return {"message": "Cookie 'username' set"}


@app.get("/get-cookie", summary="Получить cookie username")
async def get_cookie(request: Request):
    """Получает значение cookie username."""
    username = request.cookies.get("username")
    return {"username": username}


# ---- ДАННЫЕ ЗАПРОСА ----
# через форму

@app.post("/login", summary="Логин через форму")
async def login(username: str = Form(...), password: str = Form(...)):
    """Аутентификация пользователя через форму."""
    # простейшая проверка (валидация — в доп. разделе)
    user = next((u for u in USERS if u.username == username and u.password == password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # опционально: JWT
    token = create_access_token(sub=user.username)
    return {"message": f"Welcome, {username}!", "access_token": token, "token_type": "bearer"}


# JSON-пейлоад

@app.post("/register", summary="Регистрация через JSON")
async def register(payload: RegisterPayload):
    """Регистрация нового пользователя через JSON."""
    if any(u.username == payload.username for u in USERS):
        raise HTTPException(status_code=409, detail="Username already exists")
    user = User(id=next_user_id(), username=payload.username, email=payload.email, password=payload.password)
    add_user(user)
    return {"message": f"User {payload.username} registered successfully!"}


# ---- РАБОТА С КЛАССАМИ ----

@app.get("/users", response_model=List[User], summary="Список пользователей")
async def list_users():
    """Возвращает список всех пользователей."""
    return USERS


@app.get("/users/{user_id}", response_model=User, summary="Пользователь по id")
async def get_user(user_id: int = Path(..., ge=1)):
    """Возвращает пользователя по его ID."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---- ЗАГРУЗКА ФАЙЛА ----

@app.post("/upload", summary="Загрузка файла (multipart/form-data)")
async def upload(file: UploadFile = File(...)):
    """Загружает файл и возвращает его информацию."""
    head = await file.read(64)
    return {"filename": file.filename, "content_type": file.content_type, "head_preview": head.decode(errors="ignore")}


# ---- JWT МАРШРУТ ----

def auth_dependency(request: Request) -> str:
    """Возвращает username из JWT или кидает 401."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth.removeprefix("Bearer ").strip()
    sub = verify_token(token)
    if not sub:
        raise HTTPException(status_code=401, detail="Bad or expired token")
    return sub


@app.get("/me", summary="Текущий пользователь (JWT) — опционально")
async def me(current_user: str = Depends(auth_dependency)):
    """Возвращает информацию о текущем пользователе из JWT токена."""
    return {"username": current_user}
