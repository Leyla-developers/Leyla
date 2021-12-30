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
        data = {
            str(member.id): reason if reason else "Нет причины"
        }
        if await self.bot.config.DB.moderation.count_documents({"_id": ctx.guild.id}) == 0:
            await self.bot.config.DB.moderation.insert_one({"_id": ctx.guild.id, "warns": data})
        else:
            await self.bot.config.DB.moderation.insert_one({"_id": ctx.guild.id, "warns": data})
