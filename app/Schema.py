from typing import Optional
from uuid import UUID
from pydantic import BaseModel,EmailStr
from datetime import datetime


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(BasePost):
    pass

class ResUsers(BaseModel):
        id:UUID
        name:str
        email:EmailStr
        created_at:datetime

        class config:
             from_attributes=True

class Post(BasePost):
    id:int
    user_id:UUID
    user_mod:ResUsers
    created_at:datetime

    class Config:
        from_attributes=True

# NEW: This matches the structure of your JOIN query
class PostOut(BaseModel):
    post: Post    # Note: Use the class name of the model in the query
    vot: int     # Matches the .label("vot") in your query

    class Config:
        from_attributes = True

class Users(BaseModel):
        name:str
        email:EmailStr
        password:str





class UserLogin(BaseModel):
     Email:EmailStr
     Password:str

class AccessToken(BaseModel):
     access_token:str
     token_type:str

class TokenData(BaseModel):
     id:Optional[UUID]=None