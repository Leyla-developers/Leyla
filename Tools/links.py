import aiohttp


def fotmat_links_for_avatar(avatar) -> dict:
    formats = ['png', 'jpeg', 'webp']
    if avatar.is_animated():
        formats.append('gif')

    return {format_name: avatar.replace(format=format_name, size='1024').url for format_name in formats}

async def emoji_converter(format, url):
    async with aiohttp.ClientSession().get(url) as response:
        data = str(response)

    if '415' in data:
        url = url.replace('gif', format)

    return url

async def emoji_formats(url):
    formats = ['png', 'jpeg', 'webp']
    async with aiohttp.ClientSession().get(url) as response:
        data = str(response)

    if 'image/gif' in data:
        formats.append('gif')
    
    return {format_name: url.replace('webp', format_name) for format_name in formats}
