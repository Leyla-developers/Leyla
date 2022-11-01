from disnake.errors import Forbidden
from disnake.ext.commands import Context


class LeylaContext(Context):
    async def reply(self, content: str = None, **kwargs):
        try:
            await self.message.reply(content, **kwargs)
        except Forbidden:
            await self.message.channel.send(content, **kwargs)
