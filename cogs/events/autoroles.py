import disnake
from disnake.ext import commands


class Autoroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.bot.config.DB.autoroles.count_documents({"guild": member.guild.id}) == 0:
            return

        for role in dict(await self.bot.config.DB.autoroles.find_one({"guild": member.guild.id}))['roles']:
            await member.add_roles(member.guild.get_role(role))

def setup(bot):
    bot.add_cog(Autoroles(bot))
