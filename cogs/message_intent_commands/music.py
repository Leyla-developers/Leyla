"""
https://github.com/PythonistaGuild/Wavelink
"""
import os
import random
from datetime import timedelta
from collections import deque
from dotenv import load_dotenv

load_dotenv()

import disnake
from disnake.ext import commands
import wavelink
from Tools.exceptions import CustomError
import humanize


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host=os.environ.get('LAVA_HOST'),
            port=os.environ.get('LAVA_PORT'),
            password=os.environ.get('LAVA_PASS'),
        )

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track, reason):
        if not player.queue.is_empty:
            await player.play(player.queue.get())

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node: <{node.identifier}> is ready!')

    @commands.command(name="play", description="Включу вам любую музыку, какую вам нужно (ну почти)) :3")
    async def music_play(self, ctx, *, search: wavelink.YouTubeTrack):
        if not ctx.author.voice:
            raise CustomError("Подключитесь к голосовому каналу!")
        elif not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            await vc.play(search)
            await ctx.send(
                embed=await self.bot.embeds.simple(
                    title=f'Трек: {search.title}', 
                    description=f'Длительность песни: **{humanize.naturaldelta(timedelta(seconds=search.duration))}**', 
                    thumbnail=search.thumb,
                    url=search.uri,
                    fields=[{"name": "Автор", "value": search.author}]
                )
            )
        else:
            await vc.queue.put_wait(search)
            await ctx.reply(f"Трек добавлен в очередь :eyes:\n— **{search.author}** - {search.title}")

    @commands.command(name="queue", description="Посмотреть, какие треки там в очереди...")
    async def music_queue(self, ctx):
        if not ctx.voice_client:
            raise CustomError("На данный момент, здесь не играет плееров")
        else:
            data = [f'**{i+1}** | [{j.author} - {j.title}]({j.uri})' for i, j in enumerate(ctx.voice_client.queue._queue)]
            
            if bool(data):
                await ctx.send(embed=await self.bot.embeds.simple(title=f'Очередь треков [{len(data)}]', description='\n'.join(data)))
            else:
                await ctx.send(embed=await self.bot.embeds.simple(description="Очередь пуста."))

    @commands.command(name="skip", description="Пропустить песню. Не нравится прям так?")
    async def music_skip(self, ctx):
        vc = ctx.voice_client

        if bool(list(vc.queue._queue)):
            await vc.play(vc.queue.get())
            await ctx.send("Песня была пропущена, хорошо.")
        else:
            raise CustomError("Нет треков в очереди.")

    @commands.command(name='shuffle', description="Перемешать песни в очереди")
    async def music_shuffle(self, ctx):
        queue = list(ctx.voice_client.queue)
        random.shuffle(queue)
        data = [f'**{i+1}** | [{j.author} - {j.title}]({j.uri})' for i, j in enumerate(queue)]
        ctx.voice_client.queue._queue = deque(queue)

        if bool(data):
            await ctx.send(embed=await self.bot.embeds.simple(title=f'Очередь треков [{len(data)}]', description='\n'.join(data)))
        else:
            await ctx.send(embed=await self.bot.embeds.simple(description="Очередь пуста."))

    @commands.command(name='stop', description='Прекратить проигрывание музыки')
    async def music_stop(self, ctx):
        vc = ctx.voice_client
        await vc.stop()
        await ctx.send('Проигрывание музыки остановлено!')

    @music_shuffle.before_invoke
    @music_skip.before_invoke
    @music_queue.before_invoke
    @music_stop.before_invoke
    async def ensure_voice(self, ctx):
        if not ctx.voice_client:
            raise CustomError("Сейчас на сервере не играет плееров!")
        
        if not ctx.author.voice:
            raise CustomError("Подключитесь к голосовому каналу!")


def setup(bot):
    bot.add_cog(Music(bot))
