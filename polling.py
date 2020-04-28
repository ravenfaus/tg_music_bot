from aiogram.utils import executor

from bot import dp
from utils.postgres import create_db


async def on_startup():
    await create_db()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
