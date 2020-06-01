import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from aiohttp import web

import config
from bot import dp
from models import base


async def on_startup(dp):
    await base.on_startup(dp)
    await dp.bot.delete_webhook()
    await dp.bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    await base.on_shutdown(dp)


if __name__ == '__main__':
    start_webhook(dispatcher=dp,
                  webhook_path='/',
                  on_startup=on_startup,
                  on_shutdown=on_shutdown,
                  skip_updates=True,
                  host=config.WEBAPP_HOST,
                  port=config.WEBAPP_PORT,
                  )