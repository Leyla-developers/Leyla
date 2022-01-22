import random

import disnake
from disnake.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        description="Можете теперь спокойно выдавать предупреждения uwu."
    )
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: disnake.Member, *, reason: str = None):
        warn_id = random.randint(10000, 99999)
        embed = await self.bot.embeds.simple(description=f"**{member.name}** было выдано предупреждение")
        embed.add_field(name="Причина", value=reason)
        embed.set_footer(text=f"ID: {warn_id}")

        await self.bot.config.DB.moderation.insert_one({"_id": ctx.guild.id, "member": member.id, "reason": reason if reason else "Нет причины", "warn_id": warn_id})
        await ctx.send(embed=embed)
