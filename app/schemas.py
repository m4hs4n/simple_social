#we use this file in order to define the kind of data enters or exits
#it kinda validates the data 

#pydantic is a python library used for validation
#base model is a prepared class in pydantic library
#it also converts to json
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    title: str
    content: str    


    