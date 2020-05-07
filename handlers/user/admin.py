import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import User, Track, db, InlineTrack


class MessageOrder(StatesGroup):
    message_text = State()


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


async def send_command(message: types.Message):
    await MessageOrder.message_text.set()
    await message.answer('Напиши текст для рассылки.')


async def send_to_all(message: types.Message, state: FSMContext):
    users = await User.query.gino.all()
    for user in users:
        await message.bot.send_message(user.user_id, message.text)
        await asyncio.sleep(1)
    await message.answer('Рассылка завершена')
    await state.finish()
