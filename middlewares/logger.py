import time
import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class LoggerMiddleware(BaseMiddleware):
    def __init__(self, logger=__name__):
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        self.logger = logger
        super(LoggerMiddleware, self).__init__()

    async def on_pre_process_message(self, update: types.Update, data: dict):
        data['logger'] = self.logger

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        data['logger'] = self.logger
