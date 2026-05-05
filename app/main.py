from fastapi import FastAPI
from . import models
from .database import engine
from .routes import post,user,Auth
from .config import settinges

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(Auth.router)
app.include_router(post.router)
app.include_router(user.router)

