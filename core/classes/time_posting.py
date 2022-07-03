import random
from datetime import datetime

from disnake.ext import tasks
import hmtai


class LeylaTasks:

    def __init__(self, bot):
        self.bot = bot

    NSFWS = [
        'ass',
        'bdsm',
        'cum',
        'creampie',
        'manga',
        'femdom',
        'hentai',
        'incest',
        'masturbation',
        'public',
        'ero',
        'orgy',
        'elves',
        'yuri',
        'pantsu',
        'glasses',
        'cuckold',
        'blowjob',
        'boobjob',
        'foot',
        'thighs',
        'ahegao',
        'uniform',
        'gangbang',
        'tentacles',
    ]

    @tasks.loop(seconds=30)
    async def nsfw(self):
        async for i in self.bot.config.DB.nsfw.find():
            try:
                channel = self.bot.get_channel(dict(await self.bot.config.DB.nsfw.find_one({"_id": i['_id']}))['channel'])
                if channel.is_nsfw():
                    await channel.send(hmtai.useHM('29', random.choice(self.NSFWS)))

            except AttributeError:
                await self.bot.config.DB.nsfw.delete_one({"_id": i['_id'], "channel": i['channel']})
