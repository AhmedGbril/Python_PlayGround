from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP, text

from .database import Base

class post(Base):
    __tablename__ ="post"

    id =Column(Integer,primary_key=True,nullable=False)
    title =Column(String,nullable=False)
    content =Column(String,nullable=False)
    published =Column(Boolean, server_default='true',nullable=False)
    created_at =Column(TIMESTAMP, server_default=text('now()'),nullable=False)