from sqlalchemy import sql, Column, Integer, BigInteger, String, JSON

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, unique=True)
    language = Column(String(2))
    full_name = Column(String(100))
    username = Column(String(50))
    favorites = Column(JSON)
    query: sql.Select
