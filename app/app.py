#HTTPException to handle error
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse, UserRead, UserCreate, UserUpdate
from app.db import Post, create_db_and_tables, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
import shutil
import os
import uuid
import tempfile
from app.users import auth_backend, current_active_user, fastapi_users




#automatically runs this function as soon as the app is started
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

#to create a post, it can be image or video
#we use async operation because we need to wait for smth to accure
@app.post("/upload")
async def upload_file(
    #it means we can receive a file object at this endpoint
    file: UploadFile = File(...),
    caption: str = Form(""),
    #this function won't work if i'm not loged in as an active user
    user: User = Depends(current_active_user),
    #this is a dependency injection
    session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file: 
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name = file.filename,
            options={
                 "use_unique_file_name": True,
                 "tags": ["backend-upload"]
                }
            
            
        )
        
        if upload_result["error"] is None:
            post = Post(
                user_id = user.id, #we are using particular user for each post
                caption=caption,
                url=upload_result["response"]["url"],
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result["response"]["name"])

            #for adding it to database, it's like staging
            session.add(post)
            #then we commit 
            await session.commit()
            await session.refresh(post)
            return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@app.get("/feed")
async def get_feed(
    #we need to access database in order to get all our posts
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    #with execute, we can execute a query
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id: u.email for u in users}

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "Unknown")
            }
        )
    return {"posts": posts_data}

@app.delete("/posts/{post_id}")
async def  delete_post(post_id:str, session:AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_active_user)
                       ):
    try:
        #we need to covert post_id into uuid because {post_id} is going to be a str by default, we need to make it a object to do the comparison in the result
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first() #this will return the exact result 

        if not post:
            raise HTTPException(status_code=404, detail="Post not found!")
        
        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this post")

        await session.delete(post)
        await session.commit()

        return{"success": True, "message": "Post deleted successfully!"}
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))








#the first approach to learn
""""
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

"""