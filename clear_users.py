import asyncio

from aiogram import Bot
from aiogram.types import ChatActions
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated

import config
from models import User
from models.base import on_shutdown, on_startup


async def send_admin(message: str):
    await bot.send_message(config.ADMIN_ID, message)


async def parse():
    await on_startup()
    print('Bot: @{}'.format((await bot.get_me()).username))
    users = await User.query.gino.all()
    for u in users:
        try:
            await bot.send_chat_action(u.user_id, ChatActions.TYPING)
        except UserDeactivated:
            await u.delete()
            await send_admin('User deactivated from {}'.format(u.full_name))
        except BotBlocked:
            await u.delete()
            await send_admin('Bot blocked from {}'.format(u.full_name))
        except ChatNotFound:
            await u.delete()
            await send_admin('Chat not found {} from {}'.format(u.user_id, u.full_name))
        await asyncio.sleep(1)
    await on_shutdown()


if __name__ == '__main__':
    bot = Bot(token=config.API_TOKEN)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse())
