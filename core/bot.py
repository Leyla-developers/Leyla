from os import listdir
import aiohttp

from datetime import datetime
from disnake.ext import commands
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

        for folder in listdir('cogs'):
            for cog in find_extensions_in(f'cogs/{folder}'):
                try:
                    self.load_extension(cog)
                except Exception as e:
                    print(f'{folder}.{cog} fucked up by Huela', e)

    def __getitem__(self, item: str) -> commands.Command:
        return self.get_command(item)

    def __delitem__(self, item: str):
        return self.remove_command(item)

    async def on_ready(self):
        print(self.user.name, 'started at:', str(self.uptime))
