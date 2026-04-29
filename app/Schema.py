from pydantic import BaseModel
from datetime import datetime

class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(BasePost):
    pass

class Post(BasePost):
    id:int
    created_at:datetime
    
    class Config:
        from_attributes=True


class Users(BaseModel):
        name:str
        email:str
        password:str



class ResUsers(Users):
        id:str
        created_at:datetime

        class config:
             from_attributes=True
