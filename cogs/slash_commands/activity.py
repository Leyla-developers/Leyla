from typing import Literal

import disnake
from disnake.ext import commands
from DiscordActivity import Activity


class Activities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.activity = Activity(bot)


    @commands.slash_command(name="activity", description="Всякие разные голосовые активности для кАнальчика")
    async def discord_activity(self, inter, voice_channel: disnake.VoiceChannel, activity_name: Literal['youtube', 'poker', 'betrayal', 'word-snack', 'doodle-crew']):
        data = await self.activity.send_activity(voice=voice_channel, name=activity_name)
        await inter.send(f'[Кликни сюда, чтобы начать!](https://discord.gg/{data["code"]})')


def setup(bot):
    bot.add_cog(Activities(bot))
