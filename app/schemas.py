#we use this file in order to define the kind of data enters or exits
#it kinda validates the data 

#pydantic is a python library used for validation
#base model is a prepared class in pydantic library
#it also converts to json
from pydantic import BaseModel

from fastapi_users import schemas
import uuid

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    title: str
    content: str    

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass


    