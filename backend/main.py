import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from sqlalchemy import select

import database

app = FastAPI(title = "Meme Hosting API")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

@app.on_event("startup")
async def startup_event():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

@app.get("/api/posts")
async def get_posts():
    """Получить список всех постов"""
    
    async with database.AsyncSessionLocal() as db:
        statement = select(database.Post).order_by(database.Post.created_at.desc())
        result = await db.execute(statement)
        posts = result.scalars().all()
        return posts
    
@app.post("/api/posts")
async def create_post(
    author_name: str = Form(...),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """ Создать новый пост (картинка, текст или всё вместе) """
    image_path = None

    if file:
        file_name = f"{datetime.utcnow().timestamp()}_{file.filename}"
        file_location = MEDIA_DIR / file_name
        file_content = await file.read()
        with open(file_location, "wb+") as file_object:
            file_object.write(file_content)
        image_path = f"/media/{file_name}"
        
    new_post = database.Post(
        author_name=author_name,
        content=content,
        image_path=image_path
    )
    
    async with database.AsyncSessionLocal() as db:
        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)
        return {"status": "success", "post": new_post}

@app.post("/api/posts/{post_id}/like")
async def like_post(post_id: int):
    """ Поставить лайк посту по id """
    
    async with database.AsyncSessionLocal() as db:
        post = await db.get(database.Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")
        
        post.likes_count += 1
        await db.commit()
        return {"status": "success", "likes_count": post.likes_count}

@app.post("/api/posts/{post_id}/comments")
async def create_comment(post_id: int, author_name: str = Form(...), text: str = Form(...)):
    """Оставить комментарий к посту"""
    
    async with database.AsyncSessionLocal() as db:
        post = await db.get(database.Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")
        
        new_comment = database.Comment(
            post_id=post_id,
            author_name=author_name,
            text=text
        )
        
        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)
        return {"status": "success", "comment": new_comment}

@app.get("/api/posts/{post_id}/comments")
async def get_comments(post_id: int):
    """Получить все комментарии к посту"""
    
    async with database.AsyncSessionLocal() as db:
        post = await db.get(database.Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")
        
        statement = select(database.Comment).where(database.Comment.post_id == post_id).order_by(database.Comment.created_at.asc())
        result = await db.execute(statement)
        comments = result.scalars().all()
        return comments
