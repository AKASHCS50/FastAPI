from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Depends
# from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from . import schemas 
from . import models
from .database import engine, get_db

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='AKASHpostgresql121', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected Successfully...")
        break
    except Exception as error:
        print("Could not connect to database...")
        print("Error: ", error)
        time.sleep(2)


@ app.get("/")
def root():
    return {"message": "Hello World"}


@ app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    POSTS = db.query(models.Post).all()
    return POSTS


# def create_posts(payload: dict = Body(...)):
# title str*, content str*
@ app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@ app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    POSTS = db.query(models.Post).filter(models.Post.id == id).first()
    if not POSTS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return POSTS


@ app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    POSTS = db.query(models.Post).filter(models.Post.id == id)
    if not POSTS.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    POSTS.delete(synchronize_session=False)
    db.commit()
    return {'data': status.HTTP_204_NO_CONTENT}


@ app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    POSTS = db.query(models.Post).filter(models.Post.id == id)
    if not POSTS.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    POSTS.update(post.dict(), synchronize_session=False)
    db.commit()
    return POSTS.first()
