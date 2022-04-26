from os import environ
from abc import ABC, abstractmethod

import disnake
from motor.motor_asyncio import AsyncIOMotorClient

MyStrVariable = str

class Repository(ABC):
  @abstractmethod
  async def insert_data(user_id: int) -> disnake.User:
    ...

class LeylaDB(Repository):

    MONGO_CLIENT = AsyncIOMotorClient(environ['DB'])
    OLD_MONGO_CLIENT = AsyncIOMotorClient(environ['OLD_DB'])

    def __init__(self):
        self.db = self.MONGO_CLIENT.Leyla
        self.old_db = self.OLD_MONGO_CLIENT.Seriable.main.Seriable

    async def insert_data(self, collection_name: MyStrVariable, dict_data: dict):
        return await self.db.get_collection(name=collection_name).insert_one(dict_data)
