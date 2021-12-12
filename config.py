from os import environ

from disnake import Guild
from disnake.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient


class Config:

    TOKEN = environ('TOKEN')
    MONGO_CLIENT = AsyncIOMotorClient(environ['DB']) 
    DB = MONGO_CLIENT.main.Leyla
    DEFAULT_GUILD_DATA = {'prefix': 'l.', 'color': ...}

    def __init__(self, bot):
        self.bot = bot
        self.bot.config = self

    async def get_prefix(self, bot, message):
        if message.guild:
            prefix = await self.get_guild_data(message.guild.id, key='prefix')
            return commands.when_mentioned_or(*[prefix.lower(), prefix.upper()])(bot, message)

    async def get_guild_data(self, guild: Guild, key: str=None) -> dict:
        if await self.DB.guilds.count_documents({"_id": guild.id}) != 0:
            data = await self.DB.guilds.find_one({"_id": guild.id})
        else:
            data = self.DEFAULT_GUILD_DATA
        return data.get(key) if key else data
