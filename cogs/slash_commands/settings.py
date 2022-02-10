from typing import Literal

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.slash_command(description="Настрой-ка меня, Сен-пай u-u.")
    @commands.has_permissions(administrator=True)
    async def settings(self, inter):
        ...

    @settings.sub_command_group()
    async def automoderation(self, inter):
        ...

    @automoderation.sub_command(description="Настройка наказания для любителей покричать (Caps Lock)")
    async def capslock(self, inter, action: Literal['ban', 'timeout', 'kick', 'warn'], percent: int = 50):
        if await self.bot.config.DB.automod.count_documents({"_id": inter.guild.id}) == 0:
            await self.bot.config.DB.automod.insert_one({"_id": inter.guild.id, "action": action, "percent": percent})
        else:
            if dict(await self.bot.config.DB.automod.find_one({"_id": inter.guild.id}))['action'] == action:
                raise CustomError("Сейчас и так стоит это наказание >~<")
            elif action == "timeout": 
                data = {
                    "timeout": {
                        "duration": 43200
                    }
                }
                await self.bot.config.DB.automod.update_one({"_id": inter.guild.id}, {"$set": {"action": data}})
            else:
                await self.bot.config.DB.automod.update_one({"_id": inter.guild.id}, {"$set": {"action": action}})

        await inter.send(
            embed=await self.bot.embeds.simple(
                title='Leyla settings (automoderation)', 
                description=f"Установлено наказание в случае превышения капса",
                footer={"text": f"Наказание: {action}", "icon_url": inter.guild.icon.url if inter.guild.icon.url else None}
            )
        )


    
def setup(bot):
    bot.add_cog(Settings(bot))
