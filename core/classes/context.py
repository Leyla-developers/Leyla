from typing import Optional, Any

import disnake
from disnake.ext import commands


class Context(commands.Context):

    def __init__(self, **kwargs):
        self.send = self.reply
        super().__init__(**kwargs)

    async def reply(self, content: Optional[str]=None, **kwargs: Any) -> disnake.Message:
        try:
            return await super().reply(content=content, **kwargs)
        except disnake.HTTPException:
            return await super().send(content=content, **kwargs)
