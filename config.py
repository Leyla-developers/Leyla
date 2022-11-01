import os

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_CLIENT = AsyncIOMotorClient(os.environ['DB']) 
    DB = MONGO_CLIENT.Leyla
    DEFAULT_GUILD_DATA = {'color': 0xa8a6f0}
    OLD_MONGO_CLIENT = AsyncIOMotorClient(os.environ['OLD_DB'])
    OLD_DB = OLD_MONGO_CLIENT.Seriable.main.Seriable
