from aiogram import types
from utils.postgres import DBCommands

db = DBCommands()


async def start_message(message: types.Message):
    user = await db.add_new_user()
    text = f'Добро пожаловать, {user.full_name}!\n' \
           f'Чтобы начать искать песни, введи исполнителя и/или название песни. Я постараюсь найти эту песню:)'
    await message.answer(text)