import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice.channel:
            await ctx.author.voice.channel.connect()
        else:
            raise CustomError("Ты забыл(-а) подключиться к голосовому каналу, Зайка!")


def setup(bot):
    bot.add_cog(Music(bot))
