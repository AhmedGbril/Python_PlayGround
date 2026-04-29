from fastapi import APIRouter,Depends,Response,status,HTTPException
from .. import models,Schema,utils
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
    prefix="/Auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=Schema.ResUsers)
def user_login(user_login:Schema.UserLogin,db:Session= Depends(get_db)):
 user_query= db.query(models.user).filter(models.user.email==user_login.Email)
 user=user_query.first()

 if not user:
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Ivalid Cerdential")
 
 if not utils.verify(user_login.Password,user.password):
  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Ivalid Cerdential")
 
 return user
