import disnake
import lavalink
from disnake.ext import commands
from Tools.exceptions import CustomError


class LavalinkVoiceClient(disnake.VoiceClient):
    """
    This is the preferred way to handle external voice sending
    This client will be created via a cls in the connect method of the channel
    see the following documentation:
    https://disnakepy.readthedocs.io/en/latest/api.html#voiceprotocol
    """

    def __init__(self, client: disnake.Client, channel: disnake.abc.Connectable):
        self.client = client
        self.channel = channel
        # ensure there exists a client already
        if hasattr(self.client, 'lavalink'):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(
                    '127.0.0.1',
                    2333,
                    'test',
                    'us',
                    'default-node')
            self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
                't': 'VOICE_SERVER_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
                't': 'VOICE_STATE_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool) -> None:
        """
        Connect the bot to the voice channel and create a player_manager
        if it doesn't exist yet.
        """
        # ensure there is a player_manager when creating a new voice_client
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel)

    async def disconnect(self, *, force: bool) -> None:
        """
        Handles the disconnect.
        Cleans up running player and leaves the voice client.
        """
        player = self.lavalink.player_manager.get(self.channel.guild.id)

        # no need to disconnect if we are not connected
        if not force and not player.is_connected:
            return

        # None means disconnect
        await self.channel.guild.change_voice_state(channel=None)

        # update the channel_id of the player to None
        # this must be done because the on_voice_state_update that
        # would set channel_id to None doesn't get dispatched after the 
        # disconnect
        player.channel_id = None
        self.cleanup()

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.music = lavalink.Client(898664959767113729)
        self.music.add_node('127.0.0.1', 2333, 'test', 'us', 'default-node')
        self.music.add_event_hook(self.track_hook)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            await self.bot.get_guild(int(event.player.guild_id)).disconnect(force=True)

    async def on_socket_raw_receive(self, data):
        message = disnake.utils._from_json(data)
        self.dispatch("socket_response", message)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice.channel:
            await ctx.author.voice.channel.connect()
        else:
            raise CustomError("Ты забыл(-а) подключиться к голосовому каналу, Зайка!")

    @commands.command()
    async def play(self, ctx, *, query):
        player = self.music.player_manager.get(ctx.guild.id)
        query = query.strip('<>')
        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = disnake.Embed(color=disnake.Color.blurple())

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Music(bot))
