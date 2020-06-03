from sqlalchemy import sql, Column, Integer, String, TIMESTAMP, ForeignKey

from .base import BaseModel
from .user import User


class Track(BaseModel):
    __tablename__ = 'tracks'
    query: sql.Select

    id = Column(Integer, unique=True, primary_key=True)
    track_id = Column(Integer)
    owner_id = Column(Integer)
    user_id = Column(
        ForeignKey(f"{User.__tablename__}.user_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    query_id = Column(String(32))
    request = Column(String(255))
    title = Column(String)
    artist = Column(String)
    url = Column(String)
    duration = Column(Integer)
    first_query = Column(TIMESTAMP)
