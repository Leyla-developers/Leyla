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
        return await ctx.response.send_message(embed=embed)

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
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(
        description="Вывод информации о гильдии",
    )
    async def guild(self, ctx):
        information = (
            f'Участников: **{len(ctx.guild.members)}**',
            f'Эмодзи: **{len(ctx.guild.emojis)}**',
            f'Ролей: **{len(ctx.guild.roles)}**',

        )
        embed = await self.bot.embeds.simple(
            title=f'Информация о гильдии {ctx.guild.name}',
            description="\n".join(information)
        )

        if ctx.guild.banner:
            embed.set_thumbnail(ctx.guild.banner.url)

        if ctx.guild.icon:
            embed.set_thumbnail(ctx.guild.icon)

        await ctx.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
