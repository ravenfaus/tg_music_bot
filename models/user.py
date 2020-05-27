from sqlalchemy import sql, Column, BigInteger, String, TIMESTAMP, func

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, unique=True)
    language = Column(String(2))
    full_name = Column(String(100))
    username = Column(String(50))
    last_action = Column(TIMESTAMP(), nullable=False, default=func.now())
    query: sql.Select
