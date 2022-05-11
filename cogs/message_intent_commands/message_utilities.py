import sys
import platform
from datetime import datetime

import psutil
import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class MessageUtilities(commands.Cog, name='утилиты', description="Всякие ненужные, а может быть, и, вспомогательные команды"):

    def __init__(self, bot):
        self.bot = bot

    COG_EMOJI = '🔧'

    @commands.command(name="afk", description="Встали в афк? Ну ладно, подождём.")
    async def message_utilities_afk_command(self, inter, reason: str = None):
        if await self.bot.config.DB.afk.count_documents({"guild": inter.guild.id, "member": inter.author.id}) == 0:
            await self.bot.config.DB.afk.insert_one({"guild": inter.guild.id, "member": inter.author.id,
                                                     "reason": reason if reason else "Без причины",
                                                     "time": datetime.now()})

        await inter.send(
            embed=await self.bot.embeds.simple(
                description=f"Я поставила вас в список AFK, ждём вашего возвращения :relaxed:\nПричина: {reason if reason else 'Без причины'}"
            )
        )

    @commands.command(name="stats", description="Статистика бота")
    async def message_utilities_stats(self, ctx):
        shard_names = {
            '0': 'Стелла',
            '1': 'Кристина',
            '2': 'Виктория',
            '3': 'Клэр'
        }
        guilds_info = (
            f"Количество серверов: **{len(self.bot.guilds)}**",
            f"Количество пользователей: **{len(self.bot.users)}**",
            f"Количество стикеров: **{len(self.bot.stickers)}**",
            f"Количество эмодзи: **{len(self.bot.emojis)}**",
        )
        about_me_info = (
            f"Я создана: **13 июля, 2021 года.**",
            f"[Мой сервер поддержки](https://discord.gg/43zapTjgvm)",
            f"Операционная система: **{platform.platform()}**",
            f"Язык программирования: **Python {sys.version}**"
        )
        other_info = (
            f"Мой ID: **{ctx.me.id}**",
            f"Количество слэш команд: **{len(self.bot.global_slash_commands)}**",
            f"Количество обычных команд: **{len([i for i in self.bot.commands if not i.name == 'jishaku'])}**",
            f"Задержка: **{round(self.bot.latency*1000, 2)}ms**",
            f"RAM: **{psutil.virtual_memory().percent}%**",
            f"CPU: **{psutil.Process().cpu_percent()}%**",
            f"Кластеров: **{len(self.bot.shards)}**",
        )
        embed = await self.bot.embeds.simple(
            title=f"Моя статистика и информация обо мне | Кластер сервера: {shard_names[str(ctx.guild.shard_id)]}",
            description=f"Время, сколько я работаю - <t:{round(self.bot.uptime.timestamp())}:R> - ||спасите... ***моргнула 3 раза***||",
            url="https://leylabot.ml/",
            fields=[
                {"name": "Информация о серверах", "value": '\n'.join(guilds_info), "inline": True},
                {"name": "Информация про меня", "value": '\n'.join(about_me_info), "inline": True},
                {"name": "Всё прочее", "value": '\n'.join(other_info), "inline": True}
            ],
            footer={"text": f"Мои создатели: {', '.join([str(self.bot.get_user(i)) for i in self.bot.owner_ids])}", "icon_url": ctx.me.avatar.url}
        )

        await ctx.reply(embed=embed)
        

    @commands.group(name="profile", description="Информация о вас во мне, как бы странно это не звучало", invoke_without_command=True)
    async def message_utilities_profile(self, ctx, user: disnake.User):
        if await self.bot.config.DB.badges.count_documents({"_id": user.id}) > 0:
            badge_data = dict(await self.bot.config.DB.badges.find_one({"_id": user.id}))['badges']
        else:
            badge_data = 'Значков нет'

        fields = [
            {'name': 'Значки', 'value': badge_data},
        ]
        embed = await self.bot.emebds.simple(
            title=f'Профиль пользователя {user.id}',
            description=f"Статус **{user.name}** в боте: {'Просто пользователь' if not user.id in self.bot.owner_ids else 'Разработчик'}"
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MessageUtilities(bot))
