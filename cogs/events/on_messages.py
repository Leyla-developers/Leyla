import disnake
from disnake.ext import commands


class OnMessages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        percent = (len(list(filter(lambda i: i.isupper(), message.content))) / len(message.conent)) * 100
        DB_percent = await self.bot.config.DB.automod.find_one({"_id": message.guild.id})
        if not DB_percent:
            return

        if percent >= DB_percent:
            pass

def setup(bot):
    bot.add_cog(OnMessages(bot))
