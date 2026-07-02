import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select

import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title = "Meme Hosting API")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

@app.get("/api/posts")
def get_posts():
    """Получить список всех постов"""
    
    with database.SessionLocal() as db:
        statement = select(database.Post).order_by(database.Post.created_at.desc())
        posts = db.scalars(statement).all()
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
        file_location = f"{MEDIA_DIR}/{datetime.utcnow().timestamp()}_{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        image_path = file_location
        
    new_post = database.Post(
        author_name=author_name,
        content=content,
        image_path=image_path
    )
    
    with database.SessionLocal() as db:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {"status": "success", "post": new_post}

@app.post("/api/posts/{post_id}/like")
def like_post(post_id: int):
    """ Поставить лайк посту по id """
    
    with database.SessionLocal() as db:
        post = db.get(database.Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")
        
        post.likes_count += 1
        db.commit()
        return {"status": "success", "likes_count": post.likes_count}