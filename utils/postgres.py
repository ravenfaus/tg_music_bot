import string
import time
import datetime
from random import random

from aiogram import types, Bot
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import (Column, Integer, BigInteger, String,
                        Sequence, TIMESTAMP, Boolean, JSON)
from sqlalchemy import sql

from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASS

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(BigInteger)
    language = Column(String(2))
    full_name = Column(String(100))
    username = Column(String(50))
    favorites = Column(JSON)
    query: sql.Select

    def __repr__(self):
        return "<User(id='{}', fullname='{}', username='{}')>".format(
            self.id, self.full_name, self.username)


class Track(db.Model):
    __tablename__ = 'tracks'
    query: sql.Select

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    track_id = Column(Integer)
    user_id = Column(Integer)
    query_id = Column(String(32))
    request = Column(String(255))
    title = Column(String)
    artist = Column(String)
    url = Column(String)
    duration = Column(Integer)
    first_query = Column(TIMESTAMP)

    def __repr__(self):
        return f"<Track(id='{self.id}', track_id='{self.track_id}'," \
               f"user_id='{self.user_id}', query_id='{self.query_id}'," \
               f"request='{self.request}', title='{self.title}'," \
               f"artist='{self.artist}', url='{self.url}'," \
               f"duration='{self.duration}, first_query='{self.first_query}')>"


class DBCommands:

    async def get_user(self, user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def add_new_user(self):
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name
        await new_user.create()
        return new_user

    async def count_users(self) -> int:
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def add_track(self, track: dict, query_id: str, request: str):
        new_track = Track()
        new_track.request = request
        new_track.query_id = query_id
        new_track.user_id = types.User.get_current().id
        new_track.track_id = track['id']
        new_track.artist = track['artist']
        new_track.title = track['title']
        new_track.duration = track['duration']
        new_track.url = track['url'].split('?extra')[0]
        new_track.first_query = datetime.datetime.now()
        await new_track.create()
        return new_track

    async def get_track_query(self, query_id):
        return await Track.select('request').where(Track.query_id == query_id).gino.scalar()

    async def get_track(self, track_id, user_id):
        track = await Track.query.where(Track.track_id == int(track_id) and Track.user_id == int(user_id)).gino.first()
        return track

    async def get_tracks(self, query_id, limit=8, offset=0):
        tracks = await Track.query.where(Track.query_id == query_id).limit(limit).offset(offset).gino.all()
        return tracks


async def create_db():
    await db.set_bind(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()
