import disnake
import lavalink
from disnake.ext import commands
from Tools.exceptions import CustomError


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.music = lavalink.Client(self.bot.user.id)
        self.music.add_node('127.0.0.1', 2333, 'test', 'us', 'default-node')
        self.add_listener(self.music.voice_update_handler, 'on_socket_response')
        self.music.add_event_hook(self.track_hook)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.bot.get_guild(guild_id).voice_client.disconnect(force=True)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice.channel:
            await ctx.author.voice.channel.connect()
        else:
            raise CustomError("Ты забыл(-а) подключиться к голосовому каналу, Зайка!")

def setup(bot):
    bot.add_cog(Music(bot))
