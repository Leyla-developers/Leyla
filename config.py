from os import environ
from typing import Union

from disnake import Guild
from disnake.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient


class Config:

    def __init__(self) -> None:
        self.MONGO_CLIENT = AsyncIOMotorClient(environ['DB']) 
        self.DB = self.MONGO_CLIENT.Leyla
        self.DEFAULT_GUILD_DATA = {'prefix': 'l.', 'color': 0xa8a6f0}


    async def get_prefix(self, bot, message):
        if message.guild:
            prefix = await self.get_guild_data(message.guild.id, key='prefix')
            return commands.when_mentioned_or(*[prefix.lower(), prefix.upper()])(bot, message)

    async def get_guild_data(self, guild: Union[Guild, int], key: str=None) -> dict:
        guild_id = guild.id if isinstance(guild, Guild) else guild
        if await self.DB.guilds.count_documents({"_id": guild_id}) != 0:
            data = await self.DB.guilds.find_one({"_id": guild_id})
        else:
            data = self.DEFAULT_GUILD_DATA
        return data.get(key) if key is not None else data
