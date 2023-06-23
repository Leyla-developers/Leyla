import asyncio
import random
from contextlib import suppress

from disnake import Webhook
from aiohttp import ClientSession


class LeylaTasks:
    def __init__(self, bot) -> None:
        self.bot = bot

    async def nsfw(self):
        nsfw_categories = [
            "ass", "anal", "bdsm",
            "classic", "cum", "creampie",
            "manga", "femdom", "hentai",
            "incest", "masturbation",
            "public", "ero", "orgy",
            "elves", "yuri", "pantsu",
            "pussy", "glasses", "cuckold",
            "blowjob", "boobjob", "handjob",
            "footjob", "boobs", "thighs",
            "ahegao", "uniform", "gangbang",
            "tentacles", "gif", "nsfwNeko",
            "nsfwMobileWallpaper", "zettaiRyouiki",
        ]

        async for i in self.bot.config.DB.nsfw.find():
            try:
                url = self.bot.get_channel((await self.bot.config.DB.nsfw.find_one({"_id": i['_id']}))['hook'])

                with suppress(Exception):
                    async with ClientSession() as session:
                        hook = Webhook.from_url(url=url, session=session)
                        if hook.channel.is_nsfw():
                            async with self.bot.session.get(f'https://hmtai.hatsunia.cfd/nsfw/{random.choice(nsfw_categories)}') as response:
                                await hook.send((await response.json())['url'])

            except AttributeError:
                await self.bot.config.DB.nsfw.delete_one({"_id": i['_id'], "channel": i['channel']})

        await asyncio.sleep(30)

    async def start_tasks(self):
        await self.nsfw()
