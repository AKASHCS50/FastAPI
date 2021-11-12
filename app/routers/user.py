from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, models, utils
from sqlalchemy.orm.session import Session
from ..database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_passwd(user.password)
    user.password = hashed_password
    try:
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email: {user.email} already exists")


@ router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    USER = db.query(models.User).filter(models.User.id == id).first()
    if not USER:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")
    return USER
