import datetime

from aiogram import types, Bot
from aiogram.dispatcher.middlewares import BaseMiddleware

import config
from models.user import User


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, user: types.User):
        user_id = user.id
        db_user = await User.get(user_id)
        if db_user is None:
            new_user = await User.create(user_id=user.id, language=user.language_code, full_name=user.full_name,
                                         username=user.username)
            await Bot.get_current().send_message(config.ADMIN_ID, f'New user:\n{new_user.user_id} '
                                                                  f'{new_user.full_name} @{new_user.username}')

    async def update_action(self, user: types.User):
        user_id = user.id
        db_user = await User.get(user_id)
        if db_user:
            await db_user.update(last_action=datetime.datetime.now()).apply()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(message.from_user)

    async def on_post_process_message(self, message: types.Message, data: dict):
        await self.update_action(message.from_user)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(query.from_user)

    async def on_pre_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        await self.setup_chat(inline_query.from_user)
