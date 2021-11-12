from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, models, oauth2
from sqlalchemy.orm.session import Session
from ..database import get_db


router = APIRouter(prefix="/posts", tags=['Posts'])


# def create_posts(payload: dict = Body(...)):
# title str*, content str*
@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.Post, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@ router.get("/")
def get_posts(db: Session = Depends(get_db)):
    POSTS = db.query(models.Post).all()
    return POSTS


@ router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    POSTS = db.query(models.Post).filter(models.Post.id == id).first()
    if not POSTS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return POSTS


@ router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    POSTS = db.query(models.Post).filter(models.Post.id == id)
    if not POSTS.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    POSTS.delete(synchronize_session=False)
    db.commit()
    return {'data': status.HTTP_204_NO_CONTENT}


@ router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    POSTS = db.query(models.Post).filter(models.Post.id == id)
    if not POSTS.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    POSTS.update(post.dict(), synchronize_session=False)
    db.commit()
    return POSTS.first()
