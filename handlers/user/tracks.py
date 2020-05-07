import datetime
import json
import logging
import os
import random
import string
import time
import types

from aiogram import types
from aiogram.utils.callback_data import CallbackData

from models import InlineTrack
from models.track import Track
from utils.vk import Vk
import config

track_callback = CallbackData('song', 'id')
list_callback = CallbackData('list', 'q', 'off', 'd')
show_callback = CallbackData('show', 'q', 'off')
vk = Vk(config.VK_TOKEN)


async def inline_search(inline_query: types.InlineQuery):
    request = inline_query.query
    if request:
        offset = inline_query.offset if inline_query.offset else 0
        next_offset = int(offset) + 10
        sample_audio = config.WAIT_MP3
        results = []
        search_result = json.loads(await vk.search_audio(request, 10, offset))
        query_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
        kb = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Пожалуйста, подождите...', callback_data='loading'))
        for track in search_result['response']['items']:
            item = await add_inline_track(track, inline_query.from_user.id)
            results.append(types.InlineQueryResultAudio(id=item.track_id, audio_url=sample_audio,
                                                        title=item.title, performer=item.artist,
                                                        audio_duration=item.duration, reply_markup=kb))
        await inline_query.answer(results, next_offset=next_offset)


async def add_inline_track(track: dict, user_id: int):
    new_track = InlineTrack()
    new_track.user_id = user_id
    new_track.track_id = track['id']
    new_track.artist = track['artist']
    new_track.title = track['title']
    new_track.duration = track['duration']
    new_track.url = track['url'].split('?extra')[0]
    new_track.first_query = datetime.datetime.now()
    await new_track.create()
    return new_track


async def inline_chosen_track(chosen_inline_query: types.ChosenInlineResult):
    track = await InlineTrack.query.where(InlineTrack.track_id == int(chosen_inline_query.result_id))\
        .where(InlineTrack.user_id == chosen_inline_query.from_user.id).order_by(InlineTrack.first_query.desc()).gino.first()
    file_name = f'{track.artist} - {track.title}.mp3'
    await vk.download(track.url, file_name)
    try:
        with open(file_name, 'rb') as audio:
            cached_track = await chosen_inline_query.bot.send_audio(config.CHANNEL_ID, audio, performer=track.artist,
                                                                    title=track.title, duration=track.duration)
            input_media = types.InputMediaAudio(media=cached_track.audio.file_id)
            await chosen_inline_query.bot.edit_message_media(media=input_media,
                                                             inline_message_id=chosen_inline_query.inline_message_id)
        os.remove(file_name)
    except FileNotFoundError:
        await chosen_inline_query.bot.edit_message_caption(inline_message_id=chosen_inline_query.inline_message_id,
                                                           caption='Извините, возникли неполадки... Попробуйте еще раз:)')


async def search_music(message: types.Message, logger: logging.Logger):
    request = message.text
    start_time = time.time()
    result = json.loads(await vk.search_audio(request, 8))
    timeout = round((time.time() - start_time) * 1000)
    logger.info(f'Search tracks in {timeout} ms')
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    query_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
    for track in result['response']['items']:
        item = await add_track(track, query_id, request, message.from_user.id)
        m, s = divmod(item.duration, 60)
        text = f'{m}:{s} | {item.artist} - {item.title}'
        data = track_callback.new(id=item.track_id)
        keyboard_markup.add(types.InlineKeyboardButton(text, callback_data=data))

    keyboard_markup.row(
        types.InlineKeyboardButton('<', callback_data=list_callback.new(q=query_id, off=0, d=0)),
        types.InlineKeyboardButton('All', callback_data=show_callback.new(q=query_id, off=0)),
        types.InlineKeyboardButton('>', callback_data=list_callback.new(q=query_id, off=8, d=1)),
    )
    await message.answer(request, reply_markup=keyboard_markup)


async def add_track(track: dict, query_id: str, request: str, user_id: int):
    new_track = Track()
    new_track.request = request
    new_track.query_id = query_id
    new_track.user_id = user_id
    new_track.track_id = track['id']
    new_track.artist = track['artist']
    new_track.title = track['title']
    new_track.duration = track['duration']
    new_track.url = track['url'].split('?extra')[0]
    new_track.first_query = datetime.datetime.now()
    await new_track.create()
    return new_track


async def send_list(clb: types.CallbackQuery, callback_data: dict):
    await clb.answer()
    query_id = callback_data['q']
    offset = int(callback_data['off'])
    next_offset = offset + 8
    prev_offset = (offset - 8) if offset > 0 else 0
    query = await Track.select('request').where(Track.query_id == query_id).gino.scalar()
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    direction = callback_data['d']
    if direction:
        tracks = json.loads(await vk.search_audio(query, 8, offset))
        for track in tracks['response']['items']:
            item = await add_track(track, query_id, query, clb.from_user.id)
            m, s = divmod(item.duration, 60)
            text = f'{m}:{s} | {item.artist} - {item.title}'
            data = track_callback.new(id=item.track_id)
            keyboard_markup.add(types.InlineKeyboardButton(text, callback_data=data))
    else:
        tracks = await Track.query.where(Track.query_id == query_id).limit(8).offset(offset).gino.all()
        for track in tracks:
            m, s = divmod(track.duration, 60)
            text = f'{m}:{s} | {track.artist} - {track.title}'
            data = track_callback.new(id=track.id)
            keyboard_markup.add(types.InlineKeyboardButton(text, callback_data=data))
    keyboard_markup.row(
        types.InlineKeyboardButton('<', callback_data=list_callback.new(q=query_id, off=prev_offset, d=0)),
        types.InlineKeyboardButton('All', callback_data=show_callback.new(q=query_id, off=offset)),
        types.InlineKeyboardButton('>', callback_data=list_callback.new(q=query_id, off=next_offset, d=1)),
    )
    await clb.message.edit_reply_markup(reply_markup=keyboard_markup)


async def send_tracks(clb: types.CallbackQuery, callback_data: dict, logger: logging.Logger):
    await clb.answer()
    chat_id = clb.from_user.id
    query_id = callback_data['q']
    offset = callback_data['off']
    tracks = await Track.query.where(Track.query_id == query_id).limit(8).offset(offset).gino.all()
    for track in tracks:
        await clb.bot.send_chat_action(chat_id, 'upload_audio')
        await send_audio(chat_id, track, logger)


async def send_track(clb: types.CallbackQuery, callback_data: dict, logger: logging.Logger):
    await clb.answer()
    user_id = clb.from_user.id
    await clb.bot.send_chat_action(user_id, 'upload_audio')
    track_id = callback_data['id']
    track = await Track.query.where(Track.track_id == int(track_id)).where(Track.user_id == int(user_id)) \
        .order_by(Track.first_query.desc()).gino.first()
    await send_audio(clb, track, logger)


async def send_audio(clb: types.CallbackQuery, track: Track, logger: logging.Logger):
    file_name = f'{track.artist} - {track.title}.mp3'
    start = time.time()
    await vk.download(track.url, file_name)
    timeout = round((time.time() - start) * 1000)
    logger.info(f'Download audio in {timeout} ms')
    start = time.time()
    with open(file_name, 'rb') as audio:
        await clb.message.answer_audio(audio, '<a href="t.me/RavenMusBot">🎧RavenMusic</a>',
                                       performer=track.artist, title=track.title)
    timeout = round((time.time() - start) * 1000)
    logger.info(f'Send audio in {timeout} ms')
    os.remove(file_name)
