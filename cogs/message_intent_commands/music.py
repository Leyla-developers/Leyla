import os
import re
import random
from datetime import timedelta
from collections import deque
from dotenv import load_dotenv

load_dotenv()

import disnake
from disnake import SelectOption
from disnake.ext import commands
import lavalink
from Tools.exceptions import CustomError
import humanize

url_rx = re.compile(r'https?://(?:www\.)?.+')

class LavalinkVoiceClient(disnake.VoiceClient):

    def __init__(self, client: disnake.Client, channel: disnake.abc.Connectable):
        self.client = client
        self.channel = channel
        if hasattr(self.client, 'lavalink'):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node( 
                os.environ.get('LAVA_HOST'),
                os.environ.get('LAVA_PORT'),
                os.environ.get('LAVA_PASS'),
                'us',
                'default-node'
            )

            self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        lavalink_data = {
            't': 'VOICE_SERVER_UPDATE',
            'd': data
        }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        lavalink_data = {
            't': 'VOICE_STATE_UPDATE',
            'd': data
        }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool, self_deaf: bool = False, self_mute: bool = False) -> None:
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel, self_mute=self_mute, self_deaf=self_deaf)

    async def disconnect(self, *, force: bool = False) -> None:
        player = self.lavalink.player_manager.get(self.channel.guild.id)

        if not force and not player.is_connected:
            return

        await self.channel.guild.change_voice_state(channel=None)

        player.channel_id = None
        self.cleanup()

class MusicButtons(disnake.ui.View):

    def __init__(self, bot, player, dj):
        super().__init__()
        self.player = player
        self.dj = dj
        self.bot = bot

    @disnake.ui.button(emoji="⏸️")
    async def music_pause(self, button, inter):
        embed = await self.bot.embeds.simple(title='Плеер', fields=[{"name": "Действие", "value": "Пауза"}])

        if inter.author.id == self.dj.id:
            if self.player.paused:
                embed.description = "Пауза была убрана. Приятного прослушивания!"
                await self.player.set_pause(False)
            else:
                embed.description = "Плеер поставлен на паузу. Я подожду("
                await self.player.set_pause(True)
        else:
            embed.description = "Не вы включали плеер, так что, ждите того, кто запустил."
        
        await inter.send(embed=embed, ephemeral=True)

    @disnake.ui.button(emoji="⏹️")
    async def music_stop(self, button, inter):
        embed = await self.bot.embeds.simple(title='Плеер', fields=[{"name": "Действие", "value": "Стоп"}])

        if inter.author.id == self.dj.id:
            if self.player.is_playing:
                self.player.queue.clear()
                await self.player.stop()
                embed.description = "Плеер остановлен!"
            else:
                embed.description = "Плеер и так не играет сейчас"
        else:
            embed.description = "Не вы включали плеер, так что, ждите того, кто запустил."
            
        await inter.send(embed=embed, ephemeral=True)

    @disnake.ui.button(emoji="🔁")
    async def music_repeat(self, button, inter):
        embed = await self.bot.embeds.simple(title='Плеер', fields=[{"name": "Действие", "value": "Повтор"}])

        if inter.author.id == self.dj.id:
            if not self.player.repeat:
                self.player.set_repeat(True)
                embed.description = "Плеер поставлен на повтор :3"
            else:
                self.player.set_pause(False)
                embed.description = "Плеер убран с повтора!"
        else:
            embed.description = "Не вы включали плеер, так что, ждите того, кто запустил."
            
        await inter.send(embed=embed, ephemeral=True)

class Dropdown(disnake.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            SelectOption(label="Низкий"),
            SelectOption(label="Средний"),
            SelectOption(label="Высокий")
        ]

        super().__init__(
            placeholder="Уровень басса",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        if self.values[0].lower() == "низкий":
            
        await interaction.send(f"Басс выбран на уровне :: {self.values[0]}")

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.lavalink = lavalink.Client(self.bot.user.id)
        self.bot.lavalink.add_node(
            os.environ.get('LAVA_HOST'),
            os.environ.get('LAVA_PORT'),
            os.environ.get('LAVA_PASS'),
            'us', 
            'default-node'
        )
        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def ensure_voice(self, ctx):
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise CustomError('Сначала войди в ме... В голосовой канал!')

        if not player.is_connected:
            if not should_connect:
                raise CustomError('Не подключено ничего')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.BotMissingPermissions()

            player.store('channel', ctx.channel.id)

            try:
                await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
            except:
                pass

        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('Вам нужно зайти в мой голосовой канал!')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        state = self.bot.lavalink.player_manager.get(member.guild.id)

        if not state:
            return

        if len(after.channel.members) == 1:
            await state.set_pause(True)
        else:
            await state.set_pause(False)

    @commands.command(name='play')
    async def music_play(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytmsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Я ничего не нашла(')

        embed = await self.bot.embeds.simple()

        track = results['tracks'][0]
        embed.title = f'Трек: {track["info"]["title"]}'
        embed.url = track["info"]["uri"]
        embed.description = f'Длительность: {humanize.naturaldelta(timedelta(milliseconds=track["info"]["length"]))}'
        embed.add_field(name='Автор', value=track['info']['author'])
        track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
        player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed, view=MusicButtons(bot=self.bot, player=player, dj=ctx.author))

        if not player.is_playing:
            await player.play()

    @commands.command(name="stop", description="Выключить плеер")
    async def music_stop(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('Вы не в моём голосовом канале!')

        player.queue.clear()
        await player.stop()
        await ctx.voice_client.disconnect(force=True)
        await ctx.send('Ну и ладно. Я отключилась.')

def setup(bot):
    bot.add_cog(Music(bot))
