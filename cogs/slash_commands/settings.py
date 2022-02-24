from typing import Literal

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, inter):
        if not inter.author.guild_permissions.administrator:
            raise commands.MissingPermissions(['administrator'])
        else:
            return True
    
    @commands.slash_command(description="Настрой-ка меня, Сен-пай u-u.")
    @commands.has_permissions(administrator=True)
    async def settings(self, inter):
        ...

    @settings.sub_command_group(description="Автомодерация")
    async def automoderation(self, inter):
        ...

    @settings.sub_command_group(description="Уровни")
    async def level(self, inter):
        ...

    @settings.sub_command_group(description="Автороли")
    async def autoroles(self, inter):
        ...

    @settings.sub_command()
    @commands.is_nsfw()
    async def nsfw(self, inter, channel: disnake.TextChannel):
        if await self.bot.config.DB.nsfw.count_documents({"_id": inter.guild.id}) == 0:
            await self.bot.config.DB.nsfw.insert_one({"_id": inter.guild.id, "channel": channel.id})
        else:
            await self.bot.config.DB.nsfw.update_one({"_id": inter.guild.id}, {"$set": {"channel": channel.id}})

        await inter.send(embed=await self.bot.embeds.simple(title='Leyla settings **(posting)**', description="Канал автопостинга NSFW был установлен, картинка отсылается каждые 30 секунд."))


    @autoroles.sub_command(name="add-role", description="Настройка авторолей")
    async def add_roles(self, inter, role: disnake.Role):
        if await self.bot.config.DB.autoroles.count_documents({"guild": inter.guild.id}) == 0:
            await self.bot.config.DB.autoroles.insert_one({"guild": inter.guild.id, "roles": [role.id]})
        else:
            if role.id in dict(await self.bot.config.DB.autoroles.find_one({"guild": inter.guild.id}))['roles']:
                raise CustomError("Роль уже установлена")
            else:
                await self.bot.config.DB.autoroles.update_one({"guild": inter.guild.id}, {"$push": {"roles": role.id}})

        await inter.send(embed=await self.bot.embeds.simple(
                title='Leyla settings **(autoroles)**', 
                description="Роль при входе на сервер установлена", 
                footer={'text': f'Роль: {role.name}', 'icon_url': inter.guild.icon.url if inter.guild.icon.url else None}
            )
        )

    # @autoroles.sub_command(name='remove-role', description='')
    
    @settings.sub_command(name="log-channel", description="Настройка кАнальчика для логов")
    async def logs_channel(self, inter, channel: disnake.TextChannel):
        if await self.bot.config.DB.logs.count_documents({"guild": inter.guild.id}) == 0:
            await self.bot.config.DB.logs.insert_one({"guild": inter.guild.id, "channel": channel.id})
        else:
            await self.bot.config.DB.logs.update_one({"guild": inter.guild.id}, {"$set": {"channel": channel.id}})
        
        await inter.send(embed=await self.bot.embeds.simple(title="Leyla settings **(logs)**", description="Канал логов был установлен", fields=[{"name": "Канал", "value": channel.mention}]))

    @automoderation.sub_command(description="Настройка наказания для любителей покричать (Caps Lock)")
    async def capslock(self, inter, action: Literal['ban', 'timeout', 'kick', 'warn'], percent: int = 50, message: str = None, administrator_ignore: Literal["Игнорировать", "Не игнорировать"] = "Игнорировать"):
        admin_ignore = {
            "Игнорировать": True,
            "Не игнорировать": False, 
        }

        if await self.bot.config.DB.automod.count_documents({"_id": inter.guild.id}) == 0:
            await self.bot.config.DB.automod.insert_one({"_id": inter.guild.id, "action": action, "percent": percent, "message": message, "admin_ignore": admin_ignore[administrator_ignore]})
        else:
            if action == "timeout": 
                data = {
                    "timeout": {
                        "duration": 43200
                    }
                }
                await self.bot.config.DB.automod.update_one({"_id": inter.guild.id}, {"$set": {"action": data, "message": message, "admin_ignore": admin_ignore[administrator_ignore]}})
            else:
                await self.bot.config.DB.automod.update_one({"_id": inter.guild.id}, {"$set": {"action": action, "message": message, "admin_ignore": admin_ignore[administrator_ignore]}})

        await inter.send(
            embed=await self.bot.embeds.simple(
                title='Leyla settings **(automoderation)**', 
                description=f"Настройки были успешно сохранены и применены",
                footer={"text": f"Наказание: {action}", "icon_url": inter.guild.icon.url if inter.guild.icon.url else None}
            )
        )

    @level.sub_command(description="Настройка системы уровней")
    async def mode(self, inter, system_mode: Literal['Включить', 'Выключить']):
        mode = {
            "Включить": True,
            "Выключить": False,
        }

        if not dict(await self.bot.config.DB.levels.find_one({"_id": inter.guild.id}))['mode']:
            await self.bot.config.DB.levels.update_one({"_id": inter.guild.id}, {"$set": {"mode": mode[system_mode]}})

        elif mode[system_mode] == dict(await self.bot.config.DB.levels.find_one({"_id": inter.guild.id}))['mode']:
            raise CustomError(f"На данный момент система уровней стоит такая же, как вы указали.")

        else:
            await self.bot.config.DB.levels.update_one({"_id": inter.guild.id}, {"$set": {"mode": mode[system_mode]}})
        
        await inter.send(embed=await self.bot.embeds.simple(title="Leyla settings **(ranks)**", description="Режим уровней успешно изменён."))

    @level.sub_command(description="Настройка сообщения при повышении уровня")
    async def message(self, inter, message):
        if await self.bot.config.DB.levels.count_documents({"_id": inter.guild.id}) == 0:
            await self.bot.config.DB.levels.insert_one({"_id": inter.guild.id, "message": message})
        else:
            await self.bot.config.DB.levels.update_one({"_id": inter.guild.id}, {"$set": {"message": message}})

        await inter.send(embed=await self.bot.embeds.simple(
                title='Leyla settings **(ranks)**', 
                description=f"Установлено новое сообщение о повышении уровня\n**Сообщение:**\n{message}"
            )
        )

    @level.sub_command(description="Выбор канала в который будут приходить оповещения о повышении уровня")
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
