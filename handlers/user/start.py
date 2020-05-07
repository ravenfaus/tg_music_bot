from aiogram import types

from models.user import User


async def start_message(message: types.Message, user: User):
    text = f'Добро пожаловать, {user.full_name}!\n' \
           f'Чтобы начать искать песни, введи исполнителя и/или название песни. Я постараюсь найти эту песню:)'
    await message.answer(text)