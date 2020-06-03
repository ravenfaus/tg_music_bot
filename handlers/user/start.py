from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from middlewares.limits import LimitsMiddleware
from models import User

limits = LimitsMiddleware()


async def start_message(message: types.Message):
    args: str = message.get_args()
    if args:
        if args.isdigit():
            user = await User.get(int(message.from_user.id))
            if not user.referral_id:
                await user.update(referral_id=int(args)).apply()
    text = f'Добро пожаловать, {message.from_user.full_name}!\n' \
           f'Чтобы начать искать песни, введи исполнителя и/или название песни. Я постараюсь найти эту песню.\n' \
           f'Также я могу искать песни в inline режиме. Нажми на кнопку, чтобы попробовать. Надеюсь понравится:)'
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Попробовать', switch_inline_query_current_chat=''))
    await message.answer(text, reply_markup=kb)
