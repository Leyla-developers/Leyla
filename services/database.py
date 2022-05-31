from os import environ

from disnake.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient


class DB:

    # MONGO_CLIENT = AsyncIOMotorClient(environ['DB']) 
    # DB = MONGO_CLIENT.Leyla

    # OLD_MONGO_CLIENT = AsyncIOMotorClient(environ['OLD_DB'])
    # OLD_DB = OLD_MONGO_CLIENT.Seriable.main.Seriable

    def __init__(self, mongo_client):
        self.mongo_client = mongo_client

    async def find(self, query):
        return await self.mongo_client.find_one(query)