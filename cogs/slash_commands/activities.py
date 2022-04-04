from typing import Literal
from os import environ

import disnake
from disnake.ext import commands


class Activities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.apps = { 
            'youtube': '755600276941176913',
            'poker': '755827207812677713',
            'betrayal': '773336526917861400',
            'fishing': '814288819477020702',
            'chess': '832012774040141894',
            'letter-tile': '879863686565621790',
            'word-snack': '879863976006127627',
            'doodle-crew': '878067389634314250',
        }

    @commands.slash_command(description="Всякие разные развлечения для голосового кАнальчика")
    async def activity(
        self, 
        inter, 
        voice_channel: disnake.VoiceChannel = commands.Param(
            name="Голосовой чат", 
            description="Выбор голосового чата"
        ), 
        activity: Literal['youtube', 'poker', 'betrayal', 'fishing', 'chess', 'letter-tile', 'word-snack', 'doodle-crew'] = 'youtube'
    ):
        data = {
            'max_age': 604800,
            'max_uses': 100,
            'target_application_id': self.apps[activity],
            'target_type': 2,
            'temporary': False,
            'validate': None
        }

        async with self.bot.session.post(f'https://discord.com/api/v10/channels/{voice_channel.id}/invites', json=data, headers={"Authorization": f"Bot {environ['TOKEN']}"}) as response:
            channel_data = await response.json()

        await inter.send(
            embed=await self.bot.embeds.simple(
                title=f'Активность "{activity.capitalize()}"', 
                description=f"Ссылка на активность: https://discord.gg/{channel_data['code']}",
                footer={'text': f'ID активности: {self.apps[activity]}', 'icon_url': self.bot.user.avatar.url}
            )
        )

def setup(bot):
    bot.add_cog(Activities(bot))
