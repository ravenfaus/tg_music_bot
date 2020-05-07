from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from models.user import User


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, user: types.User):
        user_id = user.id

        if await User.get(user_id) is None:
            await User.create(user_id=user.id, language=user.language_code, full_name=user.full_name,
                              username=user.username)

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(message.from_user)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(query.from_user)

    async def on_pre_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        await self.setup_chat(inline_query.from_user)
