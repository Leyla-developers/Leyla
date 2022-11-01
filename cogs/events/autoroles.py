import disnake
from disnake.ext import commands


class AutoRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.bot.config.DB.autoroles.count_documents({"guild": member.guild.id}) == 0:
            return
        
        db = self.bot.config.DB.autoroles

        for role in dict(await db.find_one({"guild": member.guild.id}))['roles']:
            try:
                await member.add_roles(member.guild.get_role(role))
            except commands.RoleNotFound:
                await db.update_one({"guild": member.guild.id}, {"$pull": {"roles": role}})


def setup(bot):
    bot.add_cog(AutoRoles(bot))
