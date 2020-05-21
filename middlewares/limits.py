import asyncio
from datetime import datetime, timezone
from typing import Optional, Union

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class LimitsMiddleware(BaseMiddleware):
    data = {'send': {'global': [], 'chat': {}}}
    limits = {'send': {'global': 60 / (60 * 30), 'chat': 60 / 20}}

    async def on_make_request(self, chat_id, func, *args, **kwargs):
        print('on_make_request')
        print('args:')
        print(*args)
        while True:
            res = await self.check_timeout_send(chat_id)
            if res:
                print('sleep')
                await asyncio.sleep(res)
            else:
                print('post')
                await func(*args, **kwargs)
                break

    async def check_timeout_send(self, chat_id: Union[str, int]):
        curr_time = datetime.now().timestamp()
        while self.data['send']['global']:
            if abs(self.data['send']['global'][-1] - curr_time) >= 1:
                self.data['send']['global'].pop(-1)
            else:
                break
        if chat_id in self.data['send']['chat']:
            while self.data['send']['chat'][chat_id]:
                if abs(self.data['send']['chat'][chat_id][-1] - curr_time) >= 60:
                    self.data['send']['chat'][chat_id].pop(-1)
                else:
                    break
        else:
            self.data['send']['chat'][chat_id] = []
        if len(self.data['send']['global']) <= (60 / self.limits['send']['global']):
            if len(self.data['send']['chat'][chat_id]) <= (60 / self.limits['send']['chat']):
                self.data['send']['chat'][chat_id].append(curr_time)
                self.data['send']['global'].append(curr_time)
                return 0
            else:
                return 60 - abs(self.data['send']['chat'][chat_id][-1] - curr_time)
        else:
            return 60 - abs(self.data['send']['global'][-1] - curr_time)
