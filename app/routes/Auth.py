from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, Schema, oauth2, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/Auth", tags=["Authentication"])


@router.post("/login")
def user_login(user_login: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):

    user_query = db.query(models.user).filter(models.user.email == user_login.username)
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ivalid Cerdential"
        )

    if not utils.verify(user_login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Ivalid Cerdential"
        )
    
    access_toke = oauth2.create_access_token(data={"user_id": str(user.id)})
   
    return {"access_token": access_toke, "token_type": "bearer"}
