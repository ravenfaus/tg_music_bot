from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from middlewares.i18n import I18nMiddleware
from models import User

lang_callback = CallbackData('lang', 'choose', 'first')


def get_language_markup(first_launch: bool = False):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton('🇺🇸 English', callback_data=lang_callback.new(choose='en', first=first_launch)),
        InlineKeyboardButton('🇷🇺 Русский', callback_data=lang_callback.new(choose='ru', first=first_launch)))


async def start_message(message: types.Message, _: I18nMiddleware.gettext):
    args: str = message.get_args()
    if args:
        if args.isdigit():
            user = await User.get(int(message.from_user.id))
            if not user.referral_id:
                await user.update(referral_id=int(args)).apply()
    text_en = '✋You are welcome, <b>{}</b>. Please, choose your language below.'.format(message.from_user.full_name)
    text_ru = '✋Добро пожаловать, <b>{}</b>. Пожалуйста, выбери свой язык.'.format(message.from_user.full_name)
    result = text_en + '\n\n' + text_ru

    await message.answer(result, reply_markup=get_language_markup(True))


async def set_language(clb: types.CallbackQuery, user: User, _: I18nMiddleware.gettext, callback_data: dict):
    await user.update(language=callback_data['choose']).apply()
    await clb.answer()
    await clb.message.answer(_('Success! Your language is English 🇺🇸. You can change it by /language command',
                               locale=user.language))
    if callback_data['first'] == 'True':
        await clb.message.answer(_('🎵Welcome to RavenMusBot! 🎵\n'
                                   '🔍Write to me artist or/and song and i will try to find music for you!\n'
                                   '🔎Also you can search music via inline mode. Press the button below to try this',
                                   locale=user.language),
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(_('Try it!'), switch_inline_query_current_chat='')))


async def cmd_language(message: types.Message, _: I18nMiddleware.gettext):
    text = _('Choose your language below')
    await message.answer(text, reply_markup=get_language_markup())
