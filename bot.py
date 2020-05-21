import logging

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.redis import RedisStorage

import config
import handlers
from middlewares.acl import ACLMiddleware
from middlewares.logger import LoggerMiddleware
from middlewares.limits import LimitsMiddleware

storage = RedisStorage(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB, config.REDIS_PASS)
#logging.basicConfig(filename='music.log', level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggerMiddleware('music'))
dp.middleware.setup(ACLMiddleware())
dp.middleware.setup(LimitsMiddleware())
handlers.user.setup(dp)
