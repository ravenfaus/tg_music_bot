import aiofiles as aiofiles
import aiohttp


class Vk:
    VK_VERSION = '5.95'
    url = "https://api.vk.com/method/{}"
    headers = {
        'User-Agent': 'KateMobileAndroid/56 lite-460 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; '
                      'en)'}

    def __init__(self, token):
        self.token = token
        self.session = aiohttp.ClientSession()

    async def __request(self, method, params):
        params['access_token'] = self.token
        params['v'] = self.VK_VERSION
        r = await self.session.get(self.url.format(method), params=params, headers=self.headers)
        return await r.text()

    async def get_user_id(self, username):
        params = {'user_ids': username}
        return await self.__request('users.get', params)

    async def search_audio(self, query, count=100, offset=0):
        params = {'q': query, 'count': count, 'offset': offset}
        return await self.__request('audio.search', params)

    async def get_audio(self, owner_id, count=100, offset=0, playlist_id=None):
        params = {'owner_id': owner_id, 'count': count, 'offset': offset}
        if playlist_id:
            params['playlist_id'] = playlist_id
            return 'true'
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
