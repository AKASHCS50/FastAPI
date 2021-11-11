from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value
    # rating: Optional[int] = None  # optional field defaulting to None


class PostResponse(Post):
    # title: str
    # content: str
    # published: bool
    created_at: datetime

    class Config:
        orm_mode = True
        

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

class UserResponse(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True
        

