from sqlalchemy import sql, Column, Integer, String, TIMESTAMP, BigInteger

from .base import BaseModel


class TrackLog(BaseModel):
    __tablename__ = 'track_logs'
    query: sql.Select
    id = Column(Integer, unique=True, primary_key=True)
    track_id = Column(Integer)
    user_id = Column(BigInteger)
    title = Column(String)
    artist = Column(String)
    first_query = Column(TIMESTAMP)
    type = Column(String)
    timeout = Column(Integer)
    file_id = Column(String)
