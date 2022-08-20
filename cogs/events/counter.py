from string import digits

from disnake.ext import commands


class Counter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.bot.config.DB.counter.count_documents({"_id": member.guild.id}) == 0:
            return

        data = await self.bot.config.DB.counter.find_one({"_id": member.guild.id})
        channel = self.bot.get_channel(data['channel'])
        await channel.edit(name=''.join([i for i in channel.name if not i in digits]) + f'{len(member.guild.members)}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if await self.bot.config.DB.counter.count_documents({"_id": member.guild.id}) == 0:
            return

        data = await self.bot.config.DB.counter.find_one({"_id": member.guild.id})
        channel = self.bot.get_channel(data['channel'])
        await channel.edit(name=''.join([i for i in channel.name if not i in digits]) + f'{len(member.guild.members)}')


def setup(bot):
    bot.add_cog(Counter(bot))
