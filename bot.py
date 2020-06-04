import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.redis import RedisStorage

import config
import handlers
from middlewares.acl import ACLMiddleware
from middlewares.i18n import I18nMiddleware
from middlewares.logger import LoggerMiddleware
from middlewares.limits import LimitsMiddleware
from middlewares.vk import VKMiddleware

storage = RedisStorage(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB, config.REDIS_PASS)
#logging.basicConfig(filename='music.log', level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
dp.middleware.setup(LoggerMiddleware('music'))
dp.middleware.setup(ACLMiddleware())
dp.middleware.setup(I18nMiddleware(config.I18N_DOMAIN, LOCALES_DIR))
dp.middleware.setup(VKMiddleware(config.VK_TOKEN, config.VK_URL))
dp.middleware.setup(LimitsMiddleware())
handlers.user.setup(dp)
