from aiogram import types


async def all_other_messages(message: types.Message):
    if message.content_type == types.ContentType.TEXT:
        await message.answer('Некорректный запрос.')
    elif message.content_type == types.ContentType.AUDIO:
        await message.answer('У тебя хороший вкус:)')
