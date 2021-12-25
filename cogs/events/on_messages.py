import disnake
from disnake.ext import commands


class OnMessages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        pass

def setup(bot):
    bot.add_cog(OnMessages(bot))
