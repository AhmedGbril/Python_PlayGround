from uuid import UUID
from pydantic import BaseModel,EmailStr
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
        email:EmailStr
        password:str



class ResUsers(BaseModel):
        id:UUID
        name:str
        email:EmailStr
        created_at:datetime

        class config:
             from_attributes=True

class UserLogin(BaseModel):
     Email:EmailStr
     Password:str