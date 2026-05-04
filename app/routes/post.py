
from uuid import UUID

from fastapi import Depends, APIRouter, Response, status, HTTPException
from typing import List
from .. import Schema,models,oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
   prefix="/Posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[Schema.Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.post).all()
    return posts


@router.get("/{id}")
def get_post_byId(id:int,db: Session= Depends(get_db)):
   post_query= db.query(models.post).filter(models.post.id==id)
   post=post_query.first()
   return {"data":post}

@router.post("/",status_code= status.HTTP_201_CREATED ,response_model=Schema.Post)
def create_post(post:Schema.CreatePost,db: Session= Depends(get_db),get_current_user:UUID=Depends(oauth2.get_current_user)):
  
   
   add_post=models.post(user_id=get_current_user.id,** post.model_dump())
   db.add(add_post)
   db.commit()
   db.refresh(add_post)
   return add_post

@router.put("/{id}")
def update_post(post:Schema.CreatePost,id:int,db: Session= Depends(get_db),get_current_user:UUID=Depends(oauth2.get_current_user)):
    
    updated_post=db.query(models.post).filter(models.post.id==id, models.post.user_id==get_current_user.id)
  
    if updated_post.first()== None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"There is no post with the Id:{id} to delete")
      
    updated_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    
    return {"data":updated_post.first()}

@router.delete("/{id}")
def delete_post(id:int,db: Session = Depends(get_db)):
   deleted_post=db.query(models.post).filter(models.post.id==id)
   if deleted_post.first()== None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"There is no post with the Id:{id} to delete")
   deleted_post.delete(synchronize_session=False)
   db.commit()
   return Response(status_code=status.HTTP_204_NO_CONTENT)