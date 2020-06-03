from aiogram import Dispatcher
from aiogram import types

from .admin import get_users, count_tracks, send_command, send_to_all, count_downloaded
from .default_handler import all_other_messages
from .start import start_message
from .tracks import list_callback, show_callback, track_callback, get_album, show_similar, similar_callback
from .tracks import search_music, send_list, send_tracks, send_track, inline_search, inline_chosen_track
from .admin import MessageOrder
import config


def setup(dp: Dispatcher):
    # Admin commands
    dp.register_message_handler(get_users, lambda message: message.from_user.id == config.ADMIN_ID, commands='users')
    dp.register_message_handler(count_tracks, lambda message: message.from_user.id == config.ADMIN_ID, commands='tracks')
    dp.register_message_handler(count_downloaded, lambda message: message.from_user.id == config.ADMIN_ID,
                                commands='downloaded')
    dp.register_message_handler(send_command, lambda message: message.from_user.id == config.ADMIN_ID, commands='send')
    dp.register_message_handler(send_to_all, state=MessageOrder.message_text)
    # Commands handlers
    dp.register_message_handler(start_message, commands='start')
    dp.register_message_handler(get_album, commands='album')
    # Tracks handlers
    dp.register_callback_query_handler(send_list, list_callback.filter())
    dp.register_callback_query_handler(send_tracks, show_callback.filter())
    dp.register_callback_query_handler(send_track, track_callback.filter())
    dp.register_callback_query_handler(show_similar, similar_callback.filter())
    dp.register_message_handler(search_music, content_types=types.ContentType.TEXT)
    # Inline
    dp.register_inline_handler(inline_search)
    dp.register_chosen_inline_handler(inline_chosen_track)
    # Other
    dp.register_message_handler(all_other_messages, content_types=types.ContentType.ANY, state='*')
