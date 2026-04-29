from fastapi import Depends, FastAPI, Response, status, HTTPException
from typing import Optional,List
from . import Schema
from . import models
from sqlalchemy.orm import Session
from .database import engine, Sessionlocal, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)




@app.get("/post",response_model=List[Schema.Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.post).all()
    return posts


@app.get("/post/{id}")
def get_post_byId(id:int,db: Session= Depends(get_db)):
   post_query= db.query(models.post).filter(models.post.id==id)
   post=post_query.first()
   return {"data":post}

@app.post("/post",status_code= status.HTTP_201_CREATED ,response_model=Schema.Post)
def create_post(post:Schema.CreatePost,db: Session= Depends(get_db)):
   add_post=models.post(** post.model_dump())
   db.add(add_post)
   db.commit()
   db.refresh(add_post)
   return add_post

@app.put("/post/{id}")
def update_post(post:Schema.CreatePost,id:int,db: Session= Depends(get_db)):
    
    updated_post=db.query(models.post).filter(models.post.id==id)
  
    if updated_post.first()== None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"There is no post with the Id:{id} to delete")
      
    updated_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    
    return {"data":updated_post.first()}

@app.delete("/post/{id}")
def delete_post(id:int,db: Session = Depends(get_db)):
   deleted_post=db.query(models.post).filter(models.post.id==id)
   if deleted_post.first()== None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"There is no post with the Id:{id} to delete")
   deleted_post.delete(synchronize_session=False)
   db.commit()
   return Response(status_code=status.HTTP_204_NO_CONTENT)


###################################USERS###########################################

@app.post('/Users',status_code=status.HTTP_201_CREATED)
def create_user(user:Schema.Users,db: Session=Depends(get_db)):
   cereated_user=models.user(** user.model_dump())
   db.add(cereated_user)
   db.commit()
   db.refresh(cereated_user)
   return cereated_user