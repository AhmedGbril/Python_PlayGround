from uuid import UUID

from jose import jwt,JWTError
from datetime import datetime,timedelta
from . import Schema
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from .config import settinges
#SECRET_KEY
#Algorithm
#Expiration_TIME

oauth2_schema=OAuth2PasswordBearer(tokenUrl="login")



def create_access_token(data:dict):
    to_encode=data.copy()
    expire= datetime.now() + timedelta(minutes=settinges.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_iwt=jwt.encode(to_encode,settinges.SECRET_KEY,algorithm=settinges.ALGORITHM)

    return encoded_iwt

def verfiy_token(access_token:str,credential_exception):
    try:

        payload= jwt.decode(access_token,settinges.SECRET_KEY,algorithms=settinges.ALGORITHM)
        id:UUID=payload.get("user_id")

        if id is None:
            raise credential_exception
        
        token_data= Schema.TokenData(id=id)

        return token_data
    except JWTError:
        raise credential_exception
    
def get_current_user(token:str= Depends(oauth2_schema)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Colud not Validate credentials", headers={"WWW-Authenticate":"Bearer"})

    return verfiy_token(access_token=token,credential_exception=credential_exception)
