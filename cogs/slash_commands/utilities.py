import re
from datetime import datetime
import typing

import disnake
from disnake.ext import commands

from Tools.links import fotmat_links_for_avatar
from Tools.decoders import Decoder
from Tools.exceptions import CustomError


TEST_GUILD = 885541278908043304

class Utilities(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embed = self.bot.embeds

    @commands.slash_command(
        description="Вывод аватара участника"
    )
    async def avatar(self, interaction: commands.Context, user: disnake.User=None):
        user = user if user else interaction.author
        embed = await self.embed.simple(
            title=f"Аватар {'бота' if user.bot else 'пользователя'} {user.name}",
            image=user.display_avatar.url
        )
        return await interaction.send(embed=embed)

    @commands.slash_command(
        description='Перевод в/из азбуки морзе.'
    )
    async def morse(self, interaction: commands.Context, variant: typing.Literal['to', 'from'], *, code):
        if variant == 'to':
            morse = Decoder().to_morse(code)
        elif variant == 'from':
            morse = Decoder().from_morse(code)

        embed = await self.embed.simple(
            title='Decoder/Encoder морзе.',
            description=morse
        )
        await interaction.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации о гильдии",
    )
    async def guild(self, interaction):
        information = (
            f'Участников: **{len(interaction.guild.members)}**',
            f'Эмодзи: **{len(interaction.guild.emojis)}**',
            f'Ролей: **{len(interaction.guild.roles)}**',
        )
        embed = await self.bot.embeds.simple(
            title=f'Информация о гильдии {interaction.guild.name}',
            description="\n".join(information)
        )

        if interaction.guild.banner:
            embed.set_thumbnail(interaction.guild.banner.url)

        if interaction.guild.icon:
            embed.set_thumbnail(interaction.guild.icon)

        await interaction.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации о юзере"
    )
    async def user(self, interaction, user: disnake.User = commands.Param(lambda interaction: interaction.author)):
        embed = await self.bot.embeds.simple(title=f'Информация о {"боте" if user.bot else "пользователе"} {user.name}')

        if user.banner:
            embed.set_image(url=user.banner.url)

        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")
        
        main_information = [
            f"Зарегистрировался: **<t:{round(user.created_at.timestamp())}:R>**",
            f"Полный никнейм: **{str(user)}**",
        ]

        if user in interaction.guild.members:
            user_to_member = interaction.guild.get_member(user.id)
            second_information = [
                f"Зашёл(-ла) на сервер: **<t:{round(user_to_member.joined_at.timestamp())}:R> | {(datetime.utcnow() - user.created_at.replace(tzinfo=None)).days} дней**",
                f"Количество ролей: **{len(list(filter(lambda role: role, user_to_member.roles)))}**",
            ]

        embed.description = "\n".join(main_information) + "\n" + "\n".join(second_information) if user in interaction.guild.members else "\n".join(main_information)

        await interaction.send(embed=embed)

    @commands.slash_command(
        description="Получить эмодзик"
    )
    async def emoji(self, interaction, emoji):
        await interaction.send(embed=await self.bot.embeds.simple(image=self.bot.get_emoji(re.findall(r'[0-9]', emoji))))


def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
