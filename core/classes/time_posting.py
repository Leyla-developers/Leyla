import asyncio
import random
from contextlib import suppress


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
                channel = self.bot.get_channel((await self.bot.config.DB.nsfw.find_one({"_id": i['_id']}))['channel'])

                with suppress(Exception):
                    if channel.is_nsfw():
                        async with self.bot.session.get(f'https://hmtai.hatsunia.cfd/nsfw/{random.choice(nsfw_categories)}') as response:
                            await channel.send((await response.json())['url'])
                            await asyncio.sleep(30)

            except AttributeError:
                await self.bot.config.DB.nsfw.delete_one({"_id": i['_id'], "channel": i['channel']})

    async def start_tasks(self):
        await self.nsfw()
