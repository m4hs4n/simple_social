#HTTPException to handle error
from fastapi import FastAPI, HTTPException  
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

#automatically runs this function as soon as the app is started
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

#create a dictionary
text_posts = {1:{"title": "New Post", "Content" : "Cool test post"}}

@app.get("/posts")
#i added a query "limit" which by default is none so it's not mandatory to add
def get_all_posts(limit: int =None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse : #whatever return from this function is going to be this type
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post