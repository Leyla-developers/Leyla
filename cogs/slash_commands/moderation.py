import random

import disnake
from disnake.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def role_check(ctx, member):
        if ctx.author.top_role.position <= member.top_role.position:
            return False
        
        else:
            return True

    @commands.slash_command(
        description="Можете теперь спокойно выдавать предупреждения uwu."
    )
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: disnake.Member, *, reason: str = None):
        warn_id = random.randint(10000, 99999)
        embed = await self.bot.embeds.simple(thumbnail=ctx.message.author.display_avatar.url)
        embed.set_footer(text=f"ID: {warn_id} | {reason}")
        
        if await self.role_check(ctx):
            embed.description = f"**{member.name}** было выдано предупреждение"
            await self.bot.config.DB.moderation.insert_one({"_id": ctx.guild.id, "member": member.id, "reason": reason if reason else "Нет причины", "warn_id": warn_id})
        
        else:
            embed.description = "У вас недостаточно прав."

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
