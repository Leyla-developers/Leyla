import disnake
from disnake.ext import commands

from Tools.links import fotmat_links_for_avatar


class Utilities(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def avatar(self, ctx: commands.Context, user: disnake.User=None):
        user = user if user else ctx.author.avatar
        embed = ctx.embed(
            title=f"Аватар {'бота' if user.bot else 'пользователя'}",
            image=user.display_avatar.url
        )
        return await ctx.reply(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
