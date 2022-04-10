"""
https://github.com/PythonistaGuild/Wavelink
"""

import disnake
from disnake.ext import commands
import wavelink


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        if not hasattr(bot, "wavelink"):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        await self.bot.wavelink.initiate_node(
            host="localhost",
            port=7000,
            rest_uri="http://127.0.0.1:7000",
            password="test",
        )

    async def connect_(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        *,
        channel: disnake.VoiceChannel = None,
    ):
        if not channel:
            try:
                channel = interaction.author.voice.channel
            except AttributeError:
                raise disnake.DiscordException("No channel to join. Please either specify a valid channel or join one.")

        player = self.bot.wavelink.get_player(interaction.guild.id)
        await interaction.response.send_message(f"Connecting to **`{channel.name}`**")
        await player.connect(channel.id)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')

    @commands.slash_command()
    async def play(self, inter, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")

        if not tracks:
            return await inter.followup.send("Could not find any songs with that query.")

        player = self.bot.wavelink.get_player(inter.guild.id)
        if not player.is_connected:
            await self.connect_(inter)

        await inter.edit_original_message(content=f"Added {str(tracks[0])} to the queue.")
        await player.play(tracks[0])

def setup(bot):
    bot.add_cog(Music(bot))
