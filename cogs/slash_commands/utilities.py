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
    async def avatar(self, ctx: commands.Context, user: disnake.User=None):
        user = user if user else ctx.author
        embed = await self.embed.simple(
            title=f"Аватар {'бота' if user.bot else 'пользователя'} {user.name}",
            image=user.display_avatar.url
        )
        return await ctx.send(embed=embed)

    @commands.slash_command(
        description='Перевод в/из азбуки морзе.'
    )
    async def morse(self, ctx: commands.Context, variant: typing.Literal['to', 'from'], *, code):
        if variant == 'to':
            morse = Decoder().to_morse(code)
        elif variant == 'from':
            morse = Decoder().from_morse(code)

        embed = await self.embed.simple(
            title='Decoder/Encoder морзе.',
            description=morse
        )
        await ctx.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации о гильдии",
    )
    async def guild(self, ctx, guild: disnake.Guild = commands.Param(lambda ctx: ctx.guild)):
        information = (
            f'Участников: **{len(guild.members)}**',
            f'Эмодзи: **{len(guild.emojis)}**',
            f'Ролей: **{len(guild.roles)}**',
        )
        embed = await self.bot.embeds.simple(
            title=f'Информация о гильдии {guild.name}',
            description="\n".join(information)
        )

        if guild.banner:
            embed.set_thumbnail(guild.banner.url)

        if guild.icon:
            embed.set_thumbnail(guild.icon)

        await ctx.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации о юзере"
    )
    async def user(self, ctx, user: disnake.User = commands.Param(lambda ctx: ctx.author)):
        embed = await self.bot.embeds.simple()

        if user.banner:
            embed.set_image(url=user.banner.url)

        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")
        
        information = [
            f"Зарегистрировался: **{round(user.created_at.timestamp())}**",
            f"Полный никнейм: **{str(user)}**",
        ]

        if user in ctx.guild.members:
            user_to_member = ctx.guild.get_member(user.id)
            message = await ctx.original_message()
            information.append(
                f"Зашёл(-ла) на сервер: **{round(user_to_member.joined_at.timestamp())}**",
                f"Количество ролей: **{len(list(filter(lambda role: role, user_to_member.roles)))}**",
                f"Находится дней на сервере: **{(message.created_at - user.created_at).days}**"
            )

        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
 