from sqlalchemy.sql.expression import false, null
from .database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import TIMESTAMP, String, Integer, Boolean


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default='now()')