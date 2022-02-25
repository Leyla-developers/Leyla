import disnake
from disnake.ext import commands


class Welcome(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.bot.config.DB.welcome.count_documents({"_id": member.guild.id}) == 0:
            return
        else:
            if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['channel']:
                if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['message']:
                    data = dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))
                    data['message'] = data['message'].replace('[memberMention]', member.mention)
                    data['message'] = data['message'].replace('[member]', member.name)
                    data['message'] = data['message'].replace('[guild]', member.guild.name)
                    data['message'] = data['message'].replace('[guildMembers]', str(len(member.guild.members)))

                    await member.guild.get_channel(data['channel']).send(data['message'])

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if await self.bot.config.DB.welcome.count_documents({"_id": member.guild.id}) == 0:
            return
        else:
            if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['goodbye_channel']:
                if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['goodbye_message']:
                    data = dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))
                    data['goodbye_message'] = data['goodbye_message'].replace('[memberMention]', member.mention)
                    data['goodbye_message'] = data['goodbye_message'].replace('[member]', member.name)
                    data['goodbye_message'] = data['goodbye_message'].replace('[guild]', member.guild.name)
                    data['goodbye_message'] = data['goodbye_message'].replace('[guildMembers]', str(len(member.guild.members)))

                    await member.guild.get_channel(data['channel']).send(data['goodbye_message'])

def setup(bot):
    bot.add_cog(Welcome(bot))
