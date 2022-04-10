"""
https://github.com/PythonistaGuild/Wavelink
"""

import disnake
from disnake.ext import commands
import wavelink


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.bot,
                                            host='localhost',
                                            port=7000,
                                            password='test')

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')

    @commands.slash_command()
    async def play(self, inter, search: wavelink.YouTubeTrack):
        """Play a song with the given search query.

        If not connected, connect to our voice channel.
        """
        if not inter.voice_client:
            vc: wavelink.Player = await inter.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = inter.voice_client

        await vc.play(search)
        await inter.send(embed=await self.bot.embeds.simple(title=f'Трек: ({search.title})[{search.uri}]', description=f'Длительность песни: `{search.duration}`', thumbnail=search.thumb))


def setup(bot):
    bot.add_cog(Music(bot))
