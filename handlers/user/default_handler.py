from aiogram import types

from middlewares.i18n import I18nMiddleware


async def all_other_messages(message: types.Message, _: I18nMiddleware.gettext):
    if message.content_type == types.ContentType.AUDIO:
        await message.answer(_('You have a good taste 👍'))
