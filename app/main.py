from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@ app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)



