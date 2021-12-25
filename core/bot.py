from disnake import integrations
import yaml
from datetime import datetime
from typing import Iterable

from disnake.ext import commands
from jishaku.modules import find_extensions_in

from .classes.context import Context
from .classes.embeds import Embeds


class Leyla(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = kwargs.get('config')
        self.uptime = datetime.utcnow()
        self.embeds = Embeds(0xa8a6f0)
        self.load_cogs(['cogs/slash_commands', 'cogs/message_commands', 'cogs/events'])

    def __getitem__(self, item: str) -> commands.Command:
        return self.get_command(item)

    def __delitem__(self, item: str):
        return self.remove_command(item)
    
    def load_cogs(self, folders: Iterable, ignore_cogs: Iterable=None):
        for folder in folders:
            for cog in find_extensions_in(folder):
                if not ignore_cogs or ignore_cogs and not cog in ignore_cogs:
                    try:
                        print('Loading cog', cog, '...')
                        self.load_extension(cog)
                    except Exception as e:
                        print(cog, e)

    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message=message, cls=cls)

    async def on_ready(self):
        print(self.user.name, 'started at:', str(self.uptime))
