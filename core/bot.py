import aiohttp
from os import listdir
from datetime import datetime

import disnake
import humanize
from disnake.ext import commands
from disnake.gateway import DiscordWebSocket
from jishaku.modules import find_extensions_in
from logg import Logger

from .classes.embeds import Embeds
from .classes import LeylaTasks
from .classes.another_embeds import LeylaEmbed
from .classes.custom_context import LeylaContext

from Tools.mobile_status import leyla_mobile_identify
from config import Config


class Leyla(commands.AutoShardedBot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs['command_prefix'] = self.get_prefix
        kwargs['config'] = Config()
        log = Logger()

        self.config = Config()
        self.uptime = datetime.now()
        self.checks = LeylaTasks(self)
        self.embeds = Embeds(0xa8a6f0)
        self.session = aiohttp.ClientSession()
        self.ignore_cogs = []
        self.wavelink = None
        self.humanize = humanize.i18n.activate("ru_RU")
        self.embed = LeylaEmbed

        DiscordWebSocket.identify = leyla_mobile_identify

        for folder in listdir('cogs'):
            for cog in find_extensions_in(f'cogs/{folder}'):
                if not cog.split('.')[-1] in self.ignore_cogs:
                    try:
                        self.load_extension(cog)
                        log.info(f'{cog} loaded!')
                    except Exception as e:
                        log.error(f'{folder}.{cog} fucked up by Hueila: {e}')
                        print(e)


    def __getitem__(self, item: str) -> commands.Command:
        return self.get_command(item)


    def __delitem__(self, item: str) -> commands.Command:
        return self.remove_command(item)


    async def on_socket_raw_receive(self, data):
        message = disnake.utils._from_json(data)
        return self.dispatch("socket_response", message)


    async def get_context(self, message, *, cls=LeylaContext):
        return await super().get_context(message=message, cls=cls)


    async def get_prefix(self, message):
        if message.guild.id in [i.id for i in self.guilds]:
            if await self.config.DB.prefix.count_documents({"_id": message.guild.id}) == 0:
                prefix = 'l.'
            else:
                prefix = dict(await self.config.DB.prefix.find_one({"_id": message.guild.id}))['prefix']

        return commands.when_mentioned_or(*[prefix.lower(), prefix.upper()])(self, message)
