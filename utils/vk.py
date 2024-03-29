import asyncio
from time import time

import aiofiles as aiofiles
import aiohttp


class Vk:
    VK_VERSION = '5.99'
    headers = {
        'User-Agent': 'KateMobileAndroid/56 lite-460 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; en)'}
    requests = 0
    last_query = 0
    limit = 1

    def __init__(self, token, base_url):
        self.token = token
        self.url = base_url
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))

    async def __check_limit(self):
        cur_time = time()
        if self.requests < 3:
            self.last_query = cur_time
            self.requests += 1
            return
        else:
            if cur_time - self.last_query < self.limit:
                await asyncio.sleep(self.limit)
            self.requests = 0

    async def __request(self, method, params):
        params['access_token'] = self.token
        params['v'] = self.VK_VERSION
        await self.__check_limit()
        r = await self.session.get(self.url.format(method), params=params, headers=self.headers)
        return await r.text()

    async def get_user_id(self, username):
        params = {'user_ids': username}
        return await self.__request('users.get', params)

    async def search_audio(self, query, count=100, offset=0):
        params = {'q': query, 'count': count, 'offset': offset}
        return await self.__request('audio.search', params)

    async def get_similar(self, owner_id, track_id):
        params = {'target_audio': f"{owner_id}_{track_id}"}
        return await self.__request('audio.getRecommendations', params)

    async def get_audio(self, owner_id=None, count=100, offset=0, playlist_id=None, access_key=None):
        params = {'count': count, 'offset': offset}
        if owner_id:
            params['owner_id'] = owner_id
        if playlist_id:
            params['playlist_id'] = playlist_id
        if access_key:
            params['access_key'] = access_key
        return await self.__request('audio.get', params)

    async def get_playlists(self, owner_id, count=100, offset=0):
        params = {'owner_id': owner_id, 'count': count, 'offset': offset}
        return await self.__request('audio.getPlaylists', params)

    async def download(self, url, destination):
        async with self.session.get(url) as resp:
            if resp.status == 200:
                file = await aiofiles.open(destination, mode='wb')
                await file.write(await resp.read())
                await file.close()
