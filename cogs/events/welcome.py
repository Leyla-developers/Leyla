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
                    message = {
                        "[memberMention]": member.mention,
                        '[member]': member.name,
                        '[guild]': member.guild.name,
                        '[guildMembers]': str(len(member.guild.members)),
                    }

                    for i in message.keys():
                        ...
                        for j in message.values():
                            ...

                    await member.guild.get_channel(data['channel']).send(data['message'].replace(i, j))

def setup(bot):
    bot.add_cog(Welcome(bot))
