from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.vk import Vk


class VKMiddleware(BaseMiddleware):

    def __init__(self, token, base_url):
        super(VKMiddleware, self).__init__()
        self.vk = Vk(token, base_url)

    async def on_pre_process_message(self, message: types.Message, data: dict):
        data['vk'] = self.vk

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        data['vk'] = self.vk

    async def on_pre_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        data['vk'] = self.vk

    async def on_pre_process_chosen_inline_result(self, chosen_inline_result: types.ChosenInlineResult, data: dict):
        data['vk'] = self.vk
