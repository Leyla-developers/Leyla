import disnake
from disnake.ext import commands

from classes.context import Context


class Leyla(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __getitem__(self, item: str) -> commands.Command:
        return self.get_command(item)
    
    def __delitem__(self, item: str):
        return self.remove_command(item)

    async def get_context(self, message, *, cls):
        return await super().get_context(message, cls=Context)

    async def on_ready(self):
        ...
