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