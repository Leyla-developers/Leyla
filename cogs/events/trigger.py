import disnake
from disnake.ext import commands


class TriggerEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        self.db = self.bot.config.DB
        if await self.db.trigger.count_documents({"guild": message.guild.id, "trigger_message": message.content.lower()}) == 0:
            return

        data = await self.db.trigger.find_one({"guild": message.guild.id, "trigger_message": message.content.lower()})

        await message.channel.send(data['response'].replace('\n', '\n'))

def setup(bot):
    bot.add_cog(TriggerEvent(bot))
