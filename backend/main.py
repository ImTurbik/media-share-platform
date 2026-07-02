import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

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

TEMP_DB = []

@app.get("/api/posts")
def get_posts():
    """Получить список всех постов"""
    return TEMP_DB

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
        
    new_post = {
        "id": len(TEMP_DB) + 1,
        "author_name": author_name,
        "content": content,
        "image_path": image_path,
        "likes_count": 0,
        "created_at": datetime.utcnow()
    }
    
    TEMP_DB.append(new_post)
    return {"status": "success", "post": new_post}

@app.post("/api/posts/{post_id}/like")
def like_post(post_id: int):
    """ Поставить лайк посту по id """
    for post in TEMP_DB:
        if post["id"] == post_id:
            post["likes_count"] += 1
            return {"status": "success", "likes_count": post["likes_count"]}
        return {"status": "error", "message": "Пост не найден"}