import disnake
from disnake.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(
        description="Можете теперь спокойно выдавать предупреждения uwu."
    )
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: disnake.Member, *, reason: str=None):
        embed = await self.bot.embeds.simple()


def setup(bot):
    bot.add_cog(Moderation(bot))