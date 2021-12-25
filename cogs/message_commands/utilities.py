import typing

import disnake
from disnake.ext import commands

from Tools.links import fotmat_links_for_avatar
from Tools.decoders import Decoder


TEST_GUILD = 885541278908043304

class Utilities(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def avatar(self, ctx: commands.Context, user: disnake.User=None):
        user = user if user else ctx.author.avatar
        embed = await ctx.embed(
            title=f"Аватар {'бота' if user.bot else 'пользователя'}",
            image=user.display_avatar.url
        )
        return await ctx.reply(embed=embed)

    @commands.slash_command(
        usage='<to/from> <Текст>'
    )
    async def morse(self, ctx, variant: typing.Literal['to', 'from'], *, code):
        if variant == 'to':
            morse = Decoder().to_morse(code)
        elif variant == 'from':
            morse = Decoder().from_morse(code)
        embed = await ctx.embed(
            title='Декодер морзе',
            description=morse
        )
        await ctx.reply(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
