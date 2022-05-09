from os import environ
from typing import Union

from disnake import Guild
from motor.motor_asyncio import AsyncIOMotorClient


class Config:

    MONGO_CLIENT = AsyncIOMotorClient(environ['DB']) 
    DB = MONGO_CLIENT.Leyla
    DEFAULT_GUILD_DATA = {'color': 0xa8a6f0}
    OLD_MONGO_CLIENT = AsyncIOMotorClient(environ['OLD_DB'])
    OLD_DB = OLD_MONGO_CLIENT.Seriable.main.Seriable

    async def get_guild_data(self, guild: Union[Guild, int], key: str = None) -> dict:
        guild_id = guild.id if isinstance(guild, Guild) else guild

        if await self.DB.guilds.count_documents({"_id": guild_id}) != 0:
            data = await self.DB.guilds.find_one({"_id": guild_id})
        else:
            data = self.DEFAULT_GUILD_DATA
        return data.get(key) if key else data
