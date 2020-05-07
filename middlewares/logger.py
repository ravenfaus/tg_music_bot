import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from models import TrackLog, Track


class LoggerMiddleware(BaseMiddleware):
    def __init__(self, logger=__name__):
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        self.logger = logger
        super(LoggerMiddleware, self).__init__()

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        data['logger'] = {}

    async def on_pre_process_chosen_inline_result(self, chosen_inline_result: types.ChosenInlineResult, data: dict):
        data['logger'] = {}

    async def on_post_process_chosen_inline_result(self, chosen_inline_result: types.ChosenInlineResult,
                                                   data: dict, logger: dict):
        if 'track' in logger['logger']:
            await self.add_log(logger['logger']['track'], logger['logger']['timeout'], 'inline')

    async def on_post_process_callback_query(self, callback_query: types.CallbackQuery,
                                             data: dict, logger: dict):
        if 'track' in logger['logger'] and 'timeout' in logger['logger']:
            track = logger['logger']['track']
            timeout = logger['logger']['timeout']
            if isinstance(logger['logger']['track'], list):
                for i in range(len(track)):
                    await self.add_log(track[i], timeout[i], 'callback')
            else:
                await self.add_log(track, timeout, 'callback')

    async def add_log(self, track: Track, timeout: int, request_type: str):
        log = TrackLog()
        log.track_id = track.track_id
        log.user_id = track.user_id
        log.title = track.title
        log.artist = track.artist
        log.first_query = track.first_query
        log.type = request_type
        log.timeout = timeout
        await log.create()
