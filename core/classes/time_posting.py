import random
from contextlib import suppress

from disnake.ext import tasks
import hmtai


class LeylaTasks:

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=30)
    async def nsfw(self):
        nsfw_categories = [
            'ass', 'bdsm', 'cum', 'creampie',
            'manga', 'femdom', 'hentai',
            'incest', 'masturbation', 'public',
            'ero', 'orgy', 'elves', 'yuri',
            'pantsu', 'glasses', 'cuckold',
            'blowjob', 'boobjob', 'thighs',
            'ahegao', 'uniform', 'gangbang',
            'tentacles',
        ]
        async for i in self.bot.config.DB.nsfw.find():
            try:
                channel = self.bot.get_channel((await self.bot.config.DB.nsfw.find_one({"_id": i['_id']}))['channel'])

                with suppress(Exception):
                    if channel.is_nsfw():
                        await channel.send(hmtai.useHM('29', random.choice(self.nsfw_categories)))

            except AttributeError:
                await self.bot.config.DB.nsfw.delete_one({"_id": i['_id'], "channel": i['channel']})
