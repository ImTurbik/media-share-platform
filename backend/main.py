from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

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


def serialize_post(post: database.Post) -> dict:
    liked_by = [like.author_name for like in sorted(post.likes, key=lambda like: like.created_at)]
    return {
        "id": post.id,
        "author_name": post.author_name,
        "title": post.title,
        "content": post.content,
        "image_path": post.image_path,
        "tags": post.tags,
        "likes_count": post.likes_count,
        "liked_by": liked_by,
        "created_at": post.created_at,
    }


async def fetch_post_with_likes(db, post_id: int):
    statement = (
        select(database.Post)
        .options(selectinload(database.Post.likes))
        .where(database.Post.id == post_id)
    )
    result = await db.execute(statement)
    return result.scalar_one_or_none()


@app.on_event("startup")
async def startup_event():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)


@app.get("/api/posts")
async def get_posts():
    async with database.AsyncSessionLocal() as db:
        statement = select(database.Post).options(selectinload(database.Post.likes)).order_by(database.Post.created_at.desc())
        result = await db.execute(statement)
        posts = result.scalars().all()
        return [serialize_post(post) for post in posts]


@app.post("/api/posts")
async def create_post(
    author_name: str = Form(...),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
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
        image_path=image_path,
    )

    async with database.AsyncSessionLocal() as db:
        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)
        return {"status": "success", "post": serialize_post(new_post)}


@app.post("/api/posts/{post_id}/like")
async def like_post(post_id: int, author_name: str = Form(...)):
    author_name = author_name.strip()
    if not author_name:
        raise HTTPException(status_code=400, detail="Ник не может быть пустым")

    async with database.AsyncSessionLocal() as db:
        post = await fetch_post_with_likes(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")

        if any(like.author_name == author_name for like in post.likes):
            raise HTTPException(status_code=409, detail="Этот ник уже поставил лайк этому посту")

        post.likes.append(database.Like(author_name=author_name))
        post.likes_count = (post.likes_count or 0) + 1

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=409, detail="Этот ник уже поставил лайк этому посту")

        return {
            "status": "success",
            "likes_count": post.likes_count,
            "liked_by": [like.author_name for like in sorted(post.likes, key=lambda like: like.created_at)],
        }


@app.post("/api/posts/{post_id}/unlike")
async def unlike_post(post_id: int, author_name: str = Form(...)):
    author_name = author_name.strip()
    if not author_name:
        raise HTTPException(status_code=400, detail="Ник не может быть пустым")

    async with database.AsyncSessionLocal() as db:
        post = await fetch_post_with_likes(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")

        like = next((item for item in post.likes if item.author_name == author_name), None)
        if not like:
            raise HTTPException(status_code=404, detail="Лайк от этого ника не найден")

        post.likes.remove(like)
        post.likes_count = max((post.likes_count or 0) - 1, 0)

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=409, detail="Не удалось снять лайк")

        return {
            "status": "success",
            "likes_count": post.likes_count,
            "liked_by": [item.author_name for item in sorted(post.likes, key=lambda item: item.created_at)],
        }


@app.get("/api/posts/{post_id}/likes")
async def get_likes(post_id: int):
    async with database.AsyncSessionLocal() as db:
        post = await fetch_post_with_likes(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")

        liked_by = [like.author_name for like in sorted(post.likes, key=lambda like: like.created_at)]
        return {"post_id": post_id, "likes_count": post.likes_count, "liked_by": liked_by}


@app.post("/api/posts/{post_id}/comments")
async def create_comment(post_id: int, author_name: str = Form(...), text: str = Form(...)):
    async with database.AsyncSessionLocal() as db:
        post = await db.get(database.Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")

        new_comment = database.Comment(
            post_id=post_id,
            author_name=author_name,
            text=text,
        )

        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)
        return {"status": "success", "comment": new_comment}


@app.get("/api/posts/{post_id}/comments")
async def get_comments(post_id: int):
    async with database.AsyncSessionLocal() as db:
        post = await db.get(database.Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")

        statement = select(database.Comment).where(database.Comment.post_id == post_id).order_by(database.Comment.created_at.asc())
        result = await db.execute(statement)
        comments = result.scalars().all()
        return comments
