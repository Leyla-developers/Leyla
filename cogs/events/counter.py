from string import digits

import disnake
from disnake.ext import commands


class Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.bot.config.DB.counter.count_documents({"_id": member.guild.id}) == 0:
            return

        data = await self.bot.config.DB.counter.find_one({"_id": member.guild.id})
        channel: disnake.TextChannel = self.bot.get_channel(data['channel'])
        channel_digits = ''.join([i for i in channel.name if i in digits])
        modified_name = channel.name.replace(channel_digits, str(len(member.guild.members)))

        await channel.edit(name=modified_name)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if await self.bot.config.DB.counter.count_documents({"_id": member.guild.id}) == 0:
            return

        data = await self.bot.config.DB.counter.find_one({"_id": member.guild.id})
        channel: disnake.TextChannel = self.bot.get_channel(data['channel'])
        channel_digits = ''.join([i for i in channel.name if i in digits])
        modified_name = channel.name.replace(channel_digits, str(len(member.guild.members)))
        
        await channel.edit(name=modified_name)


def setup(bot):
    bot.add_cog(Counter(bot))
