from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, utils, oauth2
from sqlalchemy.orm.session import Session
from ..database import get_db


router = APIRouter(tags=["Authentication"])


@ router.post("/login", response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    USER = db.query(models.User).filter(models.User.email == user.username).first()
    
    if not USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.passwd_verify(user.password, USER.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        
    # create a jwt token
    access_token = oauth2.create_access_token(data={"user_id": USER.id})
    return {"access_token": access_token, "token_type": "bearer"}
