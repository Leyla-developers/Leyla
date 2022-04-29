from os import listdir
import aiohttp

import disnake
import humanize
from datetime import datetime
from disnake.ext import commands
from Tools.exceptions import CustomError
from jishaku.modules import find_extensions_in
from .classes.embeds import Embeds
from .classes import LeylaTasks


class Leyla(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = kwargs.get('config')
        self.uptime = datetime.utcnow()
        self.checks = LeylaTasks(self)
        self.embeds = Embeds(0xa8a6f0)
        self.session = aiohttp.ClientSession()
        self.ignore_cogs = []
        self.wavelink = None
        self.humanize = humanize.i18n.activate("ru_RU")

        for folder in listdir('cogs'):
            for cog in find_extensions_in(f'cogs/{folder}'):
                try:
                    for ignore_cog in self.ignore_cogs:
                        if cog in f'cogs.{folder}.{ignore_cog}':
                            raise CustomError(f"Игнорируемый ког замечен {cog}")
                    else:
                        self.load_extension(cog)
                except Exception as e:
                    print(f'{folder}.{cog} fucked up by Hueila', e)
                    print(f'https://stackoverflow.com/{e}')
                    
    def __getitem__(self, item: str) -> commands.Command:
        return self.get_command(item)

    def __delitem__(self, item: str) -> commands.Command:
        return self.remove_command(item)

    async def on_socket_raw_receive(self, data):
        message = disnake.utils._from_json(data)
        self.dispatch("socket_response", message)

    async def get_prefix(self, message):
        if message.guild.id in [i.id for i in self.guilds]:
            if await self.config.DB.prefix.count_documents({"_id": message.guild.id}) == 0:
                prefix = 'l.'
            else:
                prefix = dict(await self.config.DB.prefix.find_one({"_id": message.guild.id}))['prefix']

        return commands.when_mentioned_or(*[prefix.lower(), prefix.upper()])(self, message)

