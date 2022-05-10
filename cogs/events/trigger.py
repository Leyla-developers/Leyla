import disnake
from disnake.ext import commands


class TriggerEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        db = self.bot.config.DB
        if await db.trigger.count_documents({"guild": message.guild.id, "trigger_message": message.content.lower()}) == 0:
            return

        if message.author.bot:
            return

        data = await db.trigger.find_one({"guild": message.guild.id, "trigger_message": message.content.lower()})

        return await message.channel.send(data['response'])


def setup(bot):
    bot.add_cog(TriggerEvent(bot))
