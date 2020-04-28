from aiogram import types

print('init default')


async def all_other_messages(message: types.Message):
    print('all_other')
    if message.content_type == 'text':
        await message.answer('Некорректный запрос.')
    else:
        await message.answer('Я понимаю только буквы.')