import random
from datetime import datetime

import disnake
from disnake.ext import tasks
import hmtai
import wavelink


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

    @tasks.loop(seconds=1)
    async def giveaway_check(self):
        await self.bot.wait_until_ready()
        async for i in self.bot.config.DB.giveaway.find({"time": {"$lte": datetime.now()}}):
            message = await self.bot.get_channel(i['channel']).fetch_message(i['message_id'])
            embed = await self.bot.embeds.simple(
                title='> Розыгрыш окончен!', 
                description=f"**Приз:** {i['prize']}\n**Победитель:** {''.join(random.choices([i.mention async for i in message.reactions[0].users()], k=i['count']))}",
            )
            await message.edit(embed=embed)
            await self.bot.config.DB.giveaway.delete_one({"guild": i['guild'], 'prize': i['prize']})

