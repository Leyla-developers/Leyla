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
            title=f"Аватар {'бота' if user.bot else 'пользователя'}",
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
        description="Вывод информации о гильдии"
    )
    async def guild(self, ctx, guild: disnake.Guild):
        guild = self.bot.get_guild(guild.id) if guild else self.bot.get_guild(ctx.guild.id)
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

        await ctx.reply(embed=embed)

    @commands.slash_command(
        description="Поиск пользователей через дискриминатор (среди людей, на серверах которых есть бот)"
    )
    async def discriminator(self, ctx, discriminator: str):
        if 4 < len(str(discriminator)) > 4:
            raise CustomError("Слишком маленький/большой дискриминатор.")
        else:
            members = list(filter(lambda i: i.discriminator == discriminator, self.bot.users))
            await ctx.reply(embed=await self.bot.embeds.simple(
                title=f"Пользователей с таким дискриминатором: {len(members)}",
                description="\n".join(members)
            )
        )

def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
