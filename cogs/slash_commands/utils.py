import disnake
from disnake.ext import commands


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command()
    async def ping(self, ctx):
        await ctx.response.send_message("Бип-буп, буп-бип... ", round(self.bot.latency * 1000))


def setup(bot):
    bot.add_cog(Utils(bot))
