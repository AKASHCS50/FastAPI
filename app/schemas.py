from pydantic import BaseModel
from datetime import datetime


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
