#ORM = Object Relational Mapping
#it allows us to write python code instead of SQL or NoSQL
#ORM used in this project is called SQLAlchemy

from collections.abc import AsyncGenerator
#we can generate unique identifier with uuid
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

#these are used for saving users
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from fastapi import Depends


#it allows us to connect to a local database file on our computer called test.db
#we can change it if we want to work with a different database
DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

#data model = the type of data that we wanna store

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    posts = relationship("Post", back_populates="user")

#by using DeclerativeBase, it knows that we are making this a data model
#we generate a new id each time we insert sth new in our database
class Post(Base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    #foreign key is the refrence to another table
    #it's one to many relationship. each user can have many posts. so we add the foreign key in posts
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False) #it has to have a value
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")

#now we actually create our database
engine = create_async_engine(DATABASE_URL)
async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False) 

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
