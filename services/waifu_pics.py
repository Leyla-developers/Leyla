import aiohttp


__all__ = ['get_image']

BASE_URL = 'https://api.waifu.pics'


async def get_image(type: str, category: str, session = aiohttp.ClientSession()):
    async with session.get(f'/{BASE_URL}/{type}/{category}') as response:
        data = await response.json()
        return data.get('url')
