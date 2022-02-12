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

    @settings.sub_command_group()
    async def levels(self, inter):
        ...

    @automoderation.sub_command(description="Настройка наказания для любителей покричать (Caps Lock)")
    async def capslock(self, inter, action: Literal['ban', 'timeout', 'kick', 'warn'], percent: int = 50, message: str = None):
        if await self.bot.config.DB.automod.count_documents({"_id": inter.guild.id}) == 0:
            await self.bot.config.DB.automod.insert_one({"_id": inter.guild.id, "action": action, "percent": percent, "message": message})
        else:
            if action == "timeout": 
                data = {
                    "timeout": {
                        "duration": 43200
                    }
                }
                await self.bot.config.DB.automod.update_one({"_id": inter.guild.id}, {"$set": {"action": data, "message": message}})
            else:
                await self.bot.config.DB.automod.update_one({"_id": inter.guild.id}, {"$set": {"action": action, "message": message}})

        await inter.send(
            embed=await self.bot.embeds.simple(
                title='Leyla settings **(automoderation)**', 
                description=f"Установлено наказание в случае превышения капса",
                footer={"text": f"Наказание: {action}", "icon_url": inter.guild.icon.url if inter.guild.icon.url else None}
            )
        )


    @levels.sub_command(description="Настройка системы уровней")
    async def mode(self, inter, _mode: Literal['Включить', 'Выключить']):
        mode = {
            "Включить": True,
            "Выключить": False
        }

        if not await self.bot.config.DB.levels.find_one({"_id": inter.guild.id}):
            await self.bot.config.DB.levels.insert_one({"_id": inter.guild.id, "mode": mode[_mode]})

        if mode[_mode] == dict(await self.bot.config.DB.levels.find_one({"_id": inter.guild.id}))['mode']:
            raise CustomError(f"На данный момент система уровней стоит такая же, как вы указали.")

        else:
            await self.bot.config.DB.levels.update_one({"_id": inter.guild.id}, {"$set": {"mode": mode[_mode]}})
        
        await inter.send(embed=await self.bot.embeds.simple(title="Leyla settings **(ranks)**", description="Режим уровней успешно изменён."))

    @levels.sub_command(description="Настройка сообщения при повышении уровня")
    async def message(self, inter, message):
        if await self.bot.config.DB.levels.count_documents({"_id": inter.guild.id}) == 0:
            await self.bot.config.DB.levels.insert_one({"_id": inter.guild.id, "message": message})
        else:
            await self.bot.config.DB.levels.update_one({"_id": inter.guild.id}, {"$set": {"message": message}})

        await inter.send(embed=await self.bot.embeds.simple(
                title='Leyla settings **(ranks)**', 
                description="Установлено новое сообщение о повышении уровня\n**Сообщение:**\n{message}"
            )
        )

    @levels.sub_command(
        description="Выбор канала в который будут приходить оповещения о повышении уровня",
        options=[
            disnake.Option(
                'channel', 'Выбор канала',
                type=disnake.OptionType.channel,
                required=True,
            )
        ]
    )
    async def channel(self, inter, channel: disnake.TextChannel):
        if await self.bot.config.DB.levels.count_documents({"_id": inter.guild.id}) == 0:
            await self.bot.config.DB.levels.insert_one({"_id": inter.guild.id, "channel": channel.id})
        if await self.bot.config.DB.levels.count_documents({"_id": inter.guild.id, "channel": channel.id}) != 0:
            raise CustomError("Сейчас и так выбран этот канал")
        else:
            await self.bot.config.DB.levels.update_one({"_id": inter.guild.id}, {"$set": {"channel": channel.id}})

        await inter.send(embed=await self.bot.embeds.simple(
                title="Leyla settings **(ranks)**", 
                description="Вы успешно установили канал, в котором будет говориться и о повышении уровня участников",
                fields=[{"name": "Канал", "value": channel.mention}]
            )
        )

    
def setup(bot):
    bot.add_cog(Settings(bot))
