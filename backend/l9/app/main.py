from __future__ import annotations
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select, join
from .database import get_db, engine, Base
from .models import User, Post
from .schemas import UserCreate, UserOut, PostCreate, PostOut

app = FastAPI(title="Lab09 SQLAlchemy + FastAPI")
templates = Jinja2Templates(directory="app/templates")

# Создаём таблицы при первом старте (для учебной работы допустимо)
Base.metadata.create_all(bind=engine)

# ---------- USERS: HTML ----------
@app.get("/users", response_class=HTMLResponse)
def users_page(request: Request, db: Session = Depends(get_db)):
    users = db.scalars(select(User)).all()
    return templates.TemplateResponse("users_list.html", {"request": request, "users": users})

@app.get("/users/new", response_class=HTMLResponse)
def users_new(request: Request):
    return templates.TemplateResponse("users_form.html", {"request": request, "user": None, "action": "/users"})

@app.post("/users")
def users_create(username: str = Form(...), email: str = Form(...), password: str = Form(...),
                 db: Session = Depends(get_db)):
    if db.scalar(select(User).where((User.username == username) | (User.email == email))):
        raise HTTPException(status_code=400, detail="username/email already exists")
    u = User(username=username, email=email, password=password)
    db.add(u); db.commit()
    return RedirectResponse(url="/users", status_code=303)

@app.get("/users/{user_id}/edit", response_class=HTMLResponse)
def users_edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users_form.html", {"request": request, "user": user, "action": f"/users/{user_id}"})

@app.post("/users/{user_id}")
def users_update(user_id: int, username: str = Form(...), email: str = Form(...), password: str | None = Form(None),
                 db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.email = email
    if password:
        user.password = password
    db.commit()
    return RedirectResponse(url="/users", status_code=303)

@app.post("/users/{user_id}/delete")
def users_delete(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user:
        db.delete(user); db.commit()
    return RedirectResponse(url="/users", status_code=303)

# ---------- POSTS: HTML ----------
@app.get("/posts", response_class=HTMLResponse)
def posts_page(request: Request, db: Session = Depends(get_db)):
    # Выведем посты с именами пользователей (джойн)
    stmt = select(Post, User).join(User, Post.user_id == User.id)
    rows = db.execute(stmt).all()
    return templates.TemplateResponse("posts_list.html", {"request": request, "posts": rows})

@app.get("/posts/new", response_class=HTMLResponse)
def posts_new(request: Request):
    return templates.TemplateResponse("posts_form.html", {"request": request, "post": None, "action": "/posts"})

@app.post("/posts")
def posts_create(title: str = Form(...), content: str = Form(...), user_id: int = Form(...),
                 db: Session = Depends(get_db)):
    if not db.get(User, user_id):
        raise HTTPException(status_code=400, detail="user_id does not exist")
    p = Post(title=title, content=content, user_id=user_id)
    db.add(p); db.commit()
    return RedirectResponse(url="/posts", status_code=303)

@app.get("/posts/{post_id}/edit", response_class=HTMLResponse)
def posts_edit(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("posts_form.html", {"request": request, "post": post, "action": f"/posts/{post_id}"})

@app.post("/posts/{post_id}")
def posts_update(post_id: int, title: str = Form(...), content: str = Form(...), user_id: int = Form(...),
                 db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not db.get(User, user_id):
        raise HTTPException(status_code=400, detail="user_id does not exist")
    post.title = title
    post.content = content
    post.user_id = user_id
    db.commit()
    return RedirectResponse(url="/posts", status_code=303)

@app.post("/posts/{post_id}/delete")
def posts_delete(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if post:
        db.delete(post); db.commit()
    return RedirectResponse(url="/posts", status_code=303)

# ---------- JSON API (по желанию) ----------
@app.get("/api/users", response_model=list[UserOut])
def api_users(db: Session = Depends(get_db)):
    return db.scalars(select(User)).all()

@app.get("/api/posts", response_model=list[PostOut])
def api_posts(db: Session = Depends(get_db)):
    return db.scalars(select(Post)).all()
