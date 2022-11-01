from os import environ
from typing import Union

import disnake
from disnake.ext import commands
import wavelink
from dotenv import load_dotenv

load_dotenv()

class MusicSelectDropdown(disnake.ui.Select):
    def __init__(
        self, 
        options: list[disnake.SelectOption], 
        song_author: str,
        song_name: str,
        player: wavelink.Player,
        dj: disnake.Member
    ) -> None:
        super().__init__(
            placeholder="Выберите песню", 
            options=options,
            custom_id="music_select_drop"
        )
        self.song_author = song_author
        self.song_name = song_name
        self.dj = dj
        self.player = player

    async def callback(self, interaction: disnake.ApplicationCommandInteraction):
        if self.dj.id == interaction.author.id:
            self.player.play()

class TestMusic(commands.Cog, name="тест музыки", description="Тест новой музыки"):
    COG_EMOJI = "<:leyla_middle_finger:975200963612803174>"

    def __init__(self, bot: commands.Bot):
        bot.loop.create_task(self.initialize_and_connect_nodes(bot=bot))

    async def initialize_and_connect_nodes(self, bot: commands.Bot):
        await bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=bot,
            host=environ.get("LAVA_HOST"),
            port=environ.get("LAVA_PORT"),
            password=environ.get("LAVA_PASS")
        )

    async def play_command_callback(
        self, 
        context: Union[commands.Context, disnake.ApplicationCommandInteraction], *,
        track: Union[
            wavelink.YouTubeMusicTrack,
            wavelink.YouTubePlaylist,
            wavelink.YouTubeTrack
        ]
    ):
        if not context.voice_client:
            voice_client: wavelink.Player = await context.author.voice.channel.connect(cls=wavelink.Player)
        else:
            voice_client = context.voice_client

        match track:
            case wavelink.YouTubeTrack:
                options = [disnake.SelectOption(label=f"{i.title} - {i.author}") for i in wavelink.YouTubeTrack.search(track)]
            case wavelink.YouTubePlaylist:
                await voice_client.play(track)
            case wavelink.YouTubeMusicTrack:
                options = [disnake.SelectOption(label=f"{i.title} - {i.author}") for i in wavelink.YouTubeMusicTrack.search(track)]

        await context.send(view=...)

    @commands.command(name="t-play", description="Послушать песенку, там, да..", usage="<трек>")
    async def music_play_command(self, ctx: commands.Context, *, search: Union[wavelink.YouTubeMusicTrack, wavelink.YouTubePlaylist, wavelink.YouTubeTrack]):
        await self.play_command_callback(context=ctx, track=search)
    

def setup(bot: commands.Bot):
    bot.add_cog(TestMusic(bot))
