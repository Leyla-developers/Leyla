from os import listdir
import aiohttp

import lavalink
from datetime import datetime
from disnake.ext import commands
from Tools.exceptions import CustomError
from jishaku.modules import find_extensions_in
from .classes.embeds import Embeds
from .classes.time_posting import LeylaTasks


class Leyla(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = kwargs.get('config')
        self.uptime = datetime.utcnow()
        self.embeds = Embeds(0xa8a6f0)
        self.session = aiohttp.ClientSession()
        self.times = LeylaTasks(self)
        self.music = lavalink.Client(898664959767113729)
        self.ignore_cogs = ['maybe_i_can_create_music']

        for folder in listdir('cogs'):
            for cog in find_extensions_in(f'cogs/{folder}'):
                try:
                    for ignore_cog in self.ignore_cogs:
                        if cog in f'cogs.{folder}.{ignore_cog}':
                            raise CustomError(f"Игнорируемый ког замечен {cog}")
                    else:
                        self.load_extension(cog)
                except Exception as e:
                    print(f'{folder}.{cog} fucked up by Huela', e)

    def __getitem__(self, item: str) -> commands.Command:
        return self.get_command(item)

    def __delitem__(self, item: str) -> commands.Command:
        return self.remove_command(item)

    async def on_ready(self):
        [await self.bot.config.DB.russian_roulette.delete_one({"_id": i['_id']}) async for i in self.bot.config.DB.russian_roulette.find()]
        print(self.user.name, 'started at:', str(self.uptime))
        self.times.nsfw.start()
