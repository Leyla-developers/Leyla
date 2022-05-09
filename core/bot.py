from os import listdir
import aiohttp

import disnake
import humanize
from datetime import datetime
from disnake.ext import commands
from jishaku.modules import find_extensions_in
from .classes.embeds import Embeds
from .classes import LeylaTasks


class Leyla(commands.AutoShardedBot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = kwargs.get('config')
        self.uptime = datetime.utcnow()
        self.checks = LeylaTasks(self)
        self.embeds = Embeds(0xa8a6f0)
        self.session = aiohttp.ClientSession()
        self.ignore_cogs = ['music']
        self.wavelink = None
        self.humanize = humanize.i18n.activate("ru_RU")

    def load_cogs(self):
        for folder in listdir('cogs'):
            for cog in find_extensions_in(f'cogs/{folder}'):
                try:
                    self.load_extension(cog)
                except Exception as e:
                    print(f'{folder}.{cog} fucked up by Hueila', e)

    def __getitem__(self, item: str) -> commands.Command:
        return self.get_command(item)

    def __delitem__(self, item: str) -> commands.Command:
        return self.remove_command(item)

    async def on_socket_raw_receive(self, data):
        message = disnake.utils._from_json(data)
        return self.dispatch("socket_response", message)

    def start_checkers(self):
        self.checks.giveaway_check.start()
        self.checks.nsfw.start()

    async def get_prefix(self, message):
        if message.guild.id in [i.id for i in self.guilds]:
            if await self.config.DB.prefix.count_documents({"_id": message.guild.id}) == 0:
                prefix = 'l.'
            else:
                prefix = dict(await self.config.DB.prefix.find_one({"_id": message.guild.id}))['prefix']

        return commands.when_mentioned_or(*[prefix.lower(), prefix.upper()])(self, message)

    async def on_connect(self):
        self.load_cogs()
        self.start_checkers()
