import random

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def checker(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
        if ctx.author == member:
            return False
        else:
            return True

    @commands.slash_command(
        description="Можете теперь спокойно выдавать предупреждения uwu."
    )
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: disnake.Member, *, reason: str = None):
        warn_id = random.randint(10000, 99999)
        embed = await self.bot.embeds.simple(thumbnail=member.display_avatar.url)
        embed.set_footer(text=f"ID: {warn_id} | {reason if reason else 'Нет причины'}")
        
        if await self.checker(ctx, member):
            embed.description = f"**{member.name}** было выдано предупреждение"
            await self.bot.config.DB.moderation.insert_one({"guild": ctx.guild.id, "member": member.id, "reason": reason if reason else "Нет причины", "warn_id": warn_id})
        else:
            if ctx.author.top_role.position <= member.top_role.position:
                raise CustomError("Ваша роль равна или меньше роли упомянутого участника.")
            else:
                raise commands.MissingPermissions(missing_permissions=['ban_members'])

        await ctx.send(embed=embed)

    @commands.slash_command(
        description="Просмотр всех предупреждений участника"
    )
    async def warns(self, ctx, member: disnake.Member = commands.Param(lambda ctx: ctx.author)):
        if member.bot:
            raise CustomError("Невозможно просмотреть предупреждения **бота**")
        else:
            if await self.bot.config.DB.moderation.count_documents({"guild": ctx.guild.id, "member": member.id}) == 0:
                raise CustomError("У вас/участника отсутствуют предупреждения.")
            else:
                warn_description = "\n".join([f"{i['reason']} | {i['warn_id']}" async for i in self.bot.config.DB.moderation.find({"guild": ctx.guild.id})])
    
                embed = await self.bot.embeds.simple(
                    title=f"Вилкой в глаз или... Предупреждения {member.name}", 
                    description=warn_description, 
                    thumbnail=member.display_avatar.url,
                    footer={
                        "text": "Предупреждения участника", 
                        "icon_url": self.bot.user.avatar.url
                    }
                )
            await ctx.send(embed=embed)

    @commands.slash_command(
        description="Удаление предупреждений участника"
    )
    async def unwarn(self, ctx, member: disnake.Member, warn_id: int):
        if self.checker(ctx, member):
            await self.bot.config.DB.moderation.delete_one({"guild": ctx.guild.id, "member": member.id, "warn_id": warn_id})
            await ctx.send(embed=await self.bot.embeds.simple(
                title=f"Снятие предупреждения с {member.name}", 
                description="Предупреждение участника было снято! :з", 
                footer={"text": f"Модератор: {member.name}", "icon_url": member.display_avatar.url}
            )
        )
        elif await self.bot.config.DB.moderation.count_documents({"guild": ctx.guild.id, "member": member.id}) == 0:
            raise CustomError("У этого чудика нет предупреждений(")
        else:
            raise CustomError("Вы не можете снять предупреждение с себя.")

def setup(bot):
    bot.add_cog(Moderation(bot))
