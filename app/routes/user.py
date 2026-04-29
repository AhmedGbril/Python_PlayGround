from fastapi import Depends, APIRouter, Response, status, HTTPException
from typing import List
from .. import utils,Schema,models
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
   prefix="/Users",
   tags=["User"]
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=Schema.ResUsers)
def create_user(user:Schema.Users,db: Session=Depends(get_db)):
  #hasing the user password
  user.password=utils.hash_password(user.password)
  cereated_user=models.user(** user.model_dump())
  db.add(cereated_user)
  db.commit()
  db.refresh(cereated_user)
  return cereated_user


@router.get('/{id}',response_model=Schema.ResUsers)
def get_user(id:str,db:Session=Depends(get_db)):
   user_query=db.query(models.user).filter(models.user.id==id)
   user=user_query.first()
   return user