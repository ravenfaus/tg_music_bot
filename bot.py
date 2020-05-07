import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram import types
import aiopg
import config
import handlers
from middlewares.logger import LoggerMiddleware
from utils.postgres import create_db

storage = RedisStorage(config.REDIS_HOST, config.REDIS_PORT, 0, config.REDIS_PASS)
#logging.basicConfig(filename='music.log', level=logging.INFO)
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggerMiddleware('music'))
handlers.user.setup(dp)
