from aiogram import types

from models import User, Track, db, InlineTrack


async def get_users(message: types.Message):
    count = await db.func.count(User.user_id).gino.scalar()
    users = await User.query.gino.all()
    text = 'Count of users: {}\n'.format(count)
    for user in users:
        text += f'{user.user_id} {user.full_name} @{user.username}\n'
    await message.answer(text)


async def count_tracks(message: types.Message):
    count = await db.func.count(Track.id).gino.scalar()
    inline_count = await db.func.count(InlineTrack.id).gino.scalar()
    await message.answer(f'Total count of tracks: {count}\nTotal count of inline tracks: {inline_count}')