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
            if dict(await self.bot.config.DB.welcome.find_one({"_id": message.guild.id}))['message']:
                data = dict(await self.bot.config.DB.welcome.find_one({"_id": message.guild.id}))
                message = {
                    "[memberMention]": member.mention,
                    '[member]': member.name,
                    '[guild]': member.guild.name,
                    '[guildMembers]': len(member.guild.members),
                }

                await member.guild.get_channel(data['channel']).send(message[data['message']])

def setup(bot):
    bot.add_cog(Welcome(bot))
