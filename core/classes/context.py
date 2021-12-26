from typing import Optional, Any

from disnake import Embed, Message, HTTPException, ApplicationCommandInteraction
from disnake.ext.commands import Context


class Context(Context):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.send = self.reply
        self.config = self.bot.config

    async def reply(self, content: Optional[str]=None, **kwargs: Any) -> Message:
        try:
            return await super().reply(content=content, **kwargs)
        except HTTPException:
            return await super().send(content=content, **kwargs)

    async def embed(self, image: str=None, thumbnail: str=None, **kwargs) -> Embed:
        return await self.bot.embeds.simple(self, image, thumbnail, **kwargs)

class Application(ApplicationCommandInteraction):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.send = self.reply
        self.config = self.bot.config

    async def embed(self, image: str=None, thumbnail: str=None, **kwargs) -> Embed:
        return await self.bot.embeds.simple(self, image, thumbnail, **kwargs)
