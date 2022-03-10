import random
from types import NoneType

import disnake
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
        'vagina',
        'ahegao',
        'uniform',
        'gangbang',
        'tentacles',
    ]

    @tasks.loop(seconds=30)
    async def nsfw(self):
        async for i in self.bot.config.DB.nsfw.find():
            try:
                if self.bot.get_channel(dict(await self.bot.config.DB.nsfw.find_one({"_id": i['_id']}))['channel']).is_nsfw():
                    await self.bot.get_channel(dict(await self.bot.config.DB.nsfw.find_one({"_id": i['_id']}))['channel']).send(hmtai.useHM('29', random.choice(self.NSFWS)))
                else:
                    return

            except AttributeError:
                await self.bot.config.DB.nsfw.delete_one({"_id": i['_id'], "channel": i['channel']})
