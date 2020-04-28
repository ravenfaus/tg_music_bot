from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from .default_handler import all_other_messages
from .start import start_message
from .tracks import search_music, send_list, send_tracks, send_track
from .tracks import list_callback, show_callback, track_callback


def setup(dp: Dispatcher):
    # Commands handlers
    dp.register_message_handler(start_message, commands='start')
    # Tracks handlers
    dp.register_callback_query_handler(send_list, list_callback.filter())
    dp.register_callback_query_handler(send_tracks, show_callback.filter())
    dp.register_callback_query_handler(send_track, track_callback.filter())
    dp.register_message_handler(search_music, content_types=types.ContentType.TEXT)
    # Other
    dp.register_message_handler(all_other_messages, content_types=types.ContentType.ANY, state='*')
