from aiogram import types


async def all_other_messages(message: types.Message):
    if message.content_type == 'text':
        await message.answer('Некорректный запрос.')
    else:
        await message.answer('Я понимаю только буквы.')