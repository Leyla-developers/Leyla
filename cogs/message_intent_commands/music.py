import os
import re
import math
from datetime import timedelta

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

    async def connect(self, *, timeout: float, reconnect: bool, self_deaf: bool = False,
                      self_mute: bool = False) -> None:
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
        if self.player.paused:
            embed.description = "Пауза была убрана. Приятного прослушивания!"
            await self.player.set_pause(False)
        else:
            embed.description = "Плеер поставлен на паузу. Я подожду("
            await self.player.set_pause(True)

        await inter.send(embed=embed, ephemeral=True)

    @disnake.ui.button(emoji="⏹️")
    async def music_stop(self, button, inter):
        embed = await self.bot.embeds.simple(title='Плеер', fields=[{"name": "Действие", "value": "Стоп"}])

        if self.player.is_playing:
            vc = LavalinkVoiceClient(self.bot, inter.me.voice.channel)
            self.player.queue.clear()
            await self.player.stop()
            await vc.disconnect(force=True)
            embed.description = "Плеер остановлен!"
        else:
            embed.description = "Плеер и так не играет сейчас"

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

            await inter.send(embed=embed, ephemeral=True)
        else:
            await inter.send('Не вы заказывали музыку!', ephemeral=True)

    @disnake.ui.button(emoji='🔊')
    async def music_volume(self, button, inter):
        embed = await self.bot.embeds.simple(title='Плеер', fields=[{"name": "Действие", "value": "Изменение звука"}])
        view = ForDropdownCallbackViews(inter.author, self.bot)
        embed.description = "Выберите то, какой уровень звука вы хотите указать :р."

        await inter.send(embed=embed, view=view, ephemeral=True)

    @disnake.ui.button(emoji="🔀")
    async def music_shuffle(self, button, inter):
        embed = await self.bot.embeds.simple(title='Плеер',
                                             fields=[{"name": "Действие", "value": "Перемешка плейлиста"}])
        if len(self.player.queue) <= 1:
            embed.description = "Слишком мало песен в плейлисте."
        else:
            if self.player.shuffle:
                embed.description = "Плейлист и так перемешан"
            else:
                self.player.set_shuffle(True)
                embed.description = "Плейлист перемешан!"

        await inter.send(embed=embed, ephemeral=True)

    @disnake.ui.button(emoji="➡️")
    async def music_skip(self, button, inter):
        embed = await self.bot.embeds.simple(title='Плеер',
                                             description="Трек пропущен!",
                                             fields=[{"name": "Действие", "value": "Пропуск трека"}])
        await self.player.skip()
        await inter.send(embed=embed, ephemeral=True)

class Dropdown(disnake.ui.Select):
    def __init__(self, query, bot, dj, select_options):
        self.dj = dj
        self.bot = bot
        self.query = query
        options = select_options

        super().__init__(
            placeholder="Выберите трек",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="music_dropdown"
        )

    async def callback(self, inter):
        await inter.response.defer()

        if inter.author.id == self.dj.id:
            player = self.bot.lavalink.player_manager.get(inter.guild.id)
            results = await player.node.get_tracks(self.query)
            track = [i for i in results['tracks'] if
                     self.values[0] == "{author} - {title}".format(author=i['info']['author'],
                                                                   title=i['info']['title'])][0]
            player.add(requester=inter.author.id, track=track)
            embed = await self.bot.embeds.simple(
                title=f'Трек: {track["info"]["title"]}',
                url=track["info"]["uri"],
                description=f'Длительность: {humanize.naturaldelta(timedelta(milliseconds=track["info"]["length"]))}',
                fields=[{"name": "Автор", "value": track['info']['author']}],
                thumbnail=f'https://i.ytimg.com/vi/{track["info"]["identifier"]}/maxresdefault.jpg'
            )

            await inter.send(embed=embed, view=MusicButtons(self.bot, player, inter.author))

            if not player.is_playing:
                await player.play()
        else:
            await inter.send('Не вы заказывали музыку!', ephemeral=True)


class VolumeDropdown(disnake.ui.Select):
    def __init__(self, dj, bot):
        self.bot = bot
        self.dj = dj
        options = [
            SelectOption(label="Низко", description="Установить громкость звука на 100"),
            SelectOption(label="Средне", description="Установить громкость звука на 300"),
            SelectOption(label="Высоко", description="Установить громкость звука на 600")
        ]

        super().__init__(
            placeholder="Выберите громкость",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="music_volume_dropdown"
        )

    async def callback(self, inter):
        await inter.response.defer()

        if inter.author.id == self.dj.id:
            player = self.bot.lavalink.player_manager.get(inter.guild.id)

            match self.values[0].lower():
                case 'низко':
                    await player.set_volume(100)
                case 'средне':
                    await player.set_volume(300)
                case 'высоко':
                    await player.set_volume(600)

            await inter.send(f'Громкость установлена на уровне **{self.values[0].title()}**', ephemeral=True)
        else:
            await inter.send('Не вы заказывали музыку!', ephemeral=True)


class Views(disnake.ui.View):

    def __init__(self, query, bot, dj, options):
        super().__init__()
        self.add_item(Dropdown(query, bot, dj, options))


class ForDropdownCallbackViews(disnake.ui.View):

    def __init__(self, dj, bot):
        super().__init__()
        self.add_item(VolumeDropdown(dj, bot))


class Music(commands.Cog, name="музыка", description="Всякие команды по музыке и... И всё."):

    COG_EMOJI = '🎵'

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

    async def ensure_voice(self, ctx):
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise CustomError('Сначала войди в ме... В голосовой канал!')

        if not player.is_connected:
            if not should_connect:
                raise CustomError('Не подключено ничего')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                raise commands.BotMissingPermissions(['connect'])

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
        
        channel = self.bot.get_channel(int(state.channel_id))
        if len(channel.members) == 1:
            player = self.bot.lavalink.player_manager.get(member.guild.id)
            vc = LavalinkVoiceClient(self.bot, channel)
            player.queue.clear()
            await player.stop()
            await vc.disconnect(force=True)

    @commands.command(name='play', description="Спою... Точнее, включу песню, которую вы попросите :р")
    async def music_play(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytmsearch:{query}'

        results = await player.node.get_tracks(query)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            await ctx.reply(f'Плейлист: **{results["playlistInfo"]["name"]}** добавлен в очередь\nКоличество песен: **{len(tracks)}**', view=MusicButtons(self.bot, player, ctx.author))
            
            if not player.is_playing:
                await player.play()
        else:
            if not results or not results['tracks']:
                return await ctx.send('Я ничего не нашла(')

            data = []
            songs_list = [f"{i['info']['author']} - {i['info']['title']}" for i in results['tracks']]

            for i in list(dict.fromkeys(songs_list)):
                data.append(SelectOption(label=i))

            await ctx.reply(view=Views(query, self.bot, ctx.author, data[:5]))

    @commands.command(name='queue', description="Вывод очереди песен")
    async def music_queue(self, ctx, page: int = 1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for i, j in enumerate(player.queue[start:end], start=start):
            queue_list += f'[{i + 1} | {j.author} - {j.title} | {humanize.naturaldelta(timedelta(milliseconds=j.duration))}]({j.uri})\n'

        embed = await self.bot.embeds.simple(
            title=f"Очередь песен — {len(player.queue)}",
            description=queue_list if player.queue else "В очереди нет песен, *буп*",
            footer={"text": f"Страница: {page}/{pages}", "icon_url": ctx.author.display_avatar.url}
        )
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
