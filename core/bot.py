from os import listdir
import aiohttp

import lavalink
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
        self.music = lavalink.Client(self.user.id)
        self.music.add_node('localhost', 7000, 'testing', 'na', 'music-node')
        self.add_listener(self.music.voice_update_handler, 'on_socket_response')
        self.music.add_event_hook(self.track_hook)

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
        self.times.nsfw.start()
