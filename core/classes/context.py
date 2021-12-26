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
