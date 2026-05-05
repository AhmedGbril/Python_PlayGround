from pydantic_settings import BaseSettings


class Settinges(BaseSettings):
    SQLALCHEMY_DATABASE_URL:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int

    class Config:
        env_file=".env"


settinges=Settinges()