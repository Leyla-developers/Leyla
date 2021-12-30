import disnake
from disnake.ext import commands


class OnErrors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, cmd_error):
        await ctx.response.send_message(cmd_error)
    

def setup(bot):
    bot.add_cog(OnErrors(bot))
