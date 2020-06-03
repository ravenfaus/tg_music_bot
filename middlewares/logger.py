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

    async def on_pre_process_message(self, message: types.Message, data: dict):
        data['logger'] = {}

    async def on_post_process_chosen_inline_result(self, chosen_inline_result: types.ChosenInlineResult,
                                                   data: dict, logger: dict):
        if 'track' in logger['logger']:
            await self.add_log(logger['logger']['track'], logger['logger']['timeout'],
                               'inline', logger['logger']['file_id'])

    async def on_post_process_callback_query(self, callback_query: types.CallbackQuery,
                                             data: dict, logger: dict):
        if 'track' in logger['logger'] and 'timeout' in logger['logger'] and 'file_id' in logger['logger']:
            track = logger['logger']['track']
            timeout = logger['logger']['timeout']
            file_id = logger['logger']['file_id']
            if isinstance(track, list):
                for i in range(len(track)):
                    await self.add_log(track[i], timeout[i], 'callback', file_id[i])
            else:
                await self.add_log(track, timeout, 'callback', file_id)

    async def on_post_process_message(self, message: types.Message, data: dict, logger: dict):
        if 'logger' in logger:
            if 'track' in logger['logger'] and 'timeout' in logger['logger'] and 'file_id' in logger['logger']:
                track = logger['logger']['track']
                timeout = logger['logger']['timeout']
                file_id = logger['logger']['file_id']
                if isinstance(track, list):
                    for i in range(len(track)):
                        await self.add_log(track[i], timeout[i], 'album', file_id[i])
                else:
                    await self.add_log(track, timeout, 'album', file_id)

    async def add_log(self, track: Track, timeout: int, request_type: str, file_id: str):
        exist = await TrackLog.query.where(TrackLog.track_id == track.track_id).gino.first()
        if not exist:
            log = TrackLog()
            log.track_id = track.track_id
            log.user_id = track.user_id
            log.title = track.title
            log.artist = track.artist
            log.first_query = track.first_query
            log.type = request_type
            log.timeout = timeout
            log.file_id = file_id
            log.owner_id = track.owner_id
            await log.create()
