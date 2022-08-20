import random
import datetime
from typing import Literal

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError
from Tools.buttons import Warns


class Moderation(commands.Cog, name="модерация", description="Теперь можно давать не только в жопу, но и по ней!"):

    COG_EMOJI = "🔨"

    def __init__(self, bot):
        self.bot = bot

    async def warn_limit_action(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member, timeout_duration: int):
        if await self.bot.config.DB.warn_limit.count_documents({"_id": interaction.guild.id}) == 0:
            return
        else:
            user_data = await self.bot.config.DB.warns.count_documents({"guild": interaction.guild.id, "member": member.id})
            data = await self.bot.config.DB.warn_limit.find_one({"_id": interaction.guild.id})

            if data['limit'] <= user_data:
                match data['action']:
                    case 'mute':
                        if timeout_duration >= 0:
                            await member.timeout(reason=f'Лимит предупреждений (>={data["limit"]})', duration=timeout_duration)
                        else:
                            await member.timeout(reason=f'Лимит предупреждений (>={data["limit"]})', duration=43600)
                    case 'ban':
                        await member.ban(reason=f'Лимит предупреждений (>={data["limit"]})')
                    case 'kick':
                        await member.kick(reason=f'Лимит предупреждений (>={data["limit"]})')


    @commands.slash_command(
        description="Можете теперь спокойно выдавать предупреждения uwu."
    )
    @commands.has_permissions(ban_members=True)
    async def warn(self, inter, member: disnake.Member, *, reason: str = None):
        warn_id = random.randint(10000, 99999)
        embed = await self.bot.embeds.simple(title=f"(>-<)!!! {member.name} предупреждён!")
        embed.set_footer(text=f"ID: {warn_id} | {reason if reason else 'Нет причины'}")

        if inter.author == member:
            raise CustomError("Зачем вы пытаетесь себя предупредить?")
        elif inter.author.top_role <= member.top_role:
            raise CustomError("Ваша роль равна или меньше роли упомянутого участника.")
        else:
            warn_limits = {"timeout_duration": 42600}

            if await self.bot.config.DB.warn_limit.count_documents({"_id": inter.guild.id}) > 0:
                warn_limits = await self.bot.config.DB.warn_limit.find_one({"_id": inter.guild.id})

            embed.description = f"**{member.name}** было выдано предупреждение"
            await self.warn_limit_action(interaction=inter, member=member, timeout_duration=warn_limits['timeout_duration'])
            await self.bot.config.DB.warns.insert_one({"guild": inter.guild.id, "member": member.id, "reason": reason if reason else "Нет причины", "warn_id": warn_id})

        await inter.send(embed=embed)

    @commands.slash_command(
        description="Просмотр всех предупреждений участника"
    )
    @commands.has_permissions(ban_members=True)
    async def warns(self, inter, member: disnake.Member = commands.Param(lambda inter: inter.author)):
        if member.bot:
            raise CustomError("Невозможно просмотреть предупреждения **бота**")
        elif await self.bot.config.DB.warns.count_documents({"guild": inter.guild.id, "member": member.id}) == 0:
            raise CustomError("У вас/участника отсутствуют предупреждения.")
        else:
            warn_description = "Чтобы просмотреть все свои предупреждения, нажмите на кнопку ниже."

            embed = await self.bot.embeds.simple(
                title=f"Вилкой в глаз или... Предупреждения {member.name}",
                description=warn_description,
                thumbnail=member.display_avatar.url,
                footer={
                    "text": "Предупреждения участника", 
                    "icon_url": self.bot.user.avatar.url
                }
            )

        await inter.send(embed=embed, view=Warns(member))

    @commands.slash_command(description="Удаление предупреждений участника")
    @commands.has_permissions(ban_members=True)
    async def unwarn(self, inter, member: disnake.Member, warn_id: int):
        if inter.author == member:
            raise CustomError("Вы не можете снять предупреждение с себя.")
        elif await self.bot.config.DB.warns.count_documents({"guild": inter.guild.id, "member": member.id}) == 0:
            raise CustomError("У этого чудика нет предупреждений(")
        elif await self.bot.config.DB.warns.count_documents({"guild": inter.guild.id, "warn_id": warn_id}) == 0:
            raise CustomError("Такого warn-ID не существует.")
        else:
            await self.bot.config.DB.warns.delete_one({"guild": inter.guild.id, "member": member.id, "warn_id": warn_id})
            await inter.send(embed=await self.bot.embeds.simple(
                title=f"Снятие предупреждения с {member.name}", 
                description="Предупреждение участника было снято! :з", 
                footer={"text": f"Модератор: {inter.author.name}", "icon_url": inter.author.display_avatar.url}
            )
        )

    @commands.slash_command(description="Кто-то намусорил в чате? Помогу очистить :)")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, inter, messages_amount: int, member: disnake.Member = None):
        if messages_amount <= 0:
            raise CustomError("Как ты собрался очистить ноль или меньше сообщений?")
        else:
            if member:
                check = lambda m: m.author == member
            else:
                check = lambda m: m.author

            cleared_messages = await inter.channel.purge(limit=messages_amount, check=check)

        await inter.send(embed=await self.bot.embeds.simple(description=f"Я очистила **{len(cleared_messages)}** сообщений!"))

    @commands.slash_command(name="timeout", description="Надоел нарушитель? Теперь ему можно заклеить рот!")
    @commands.has_permissions(ban_members=True)
    async def discord_timeout(self,
                              inter,
                              member: disnake.Member,
                              duration: int,
                              unit: Literal['Секунды', 'Минуты', 'Часы', 'Дни', 'Недели'],
                              reason: str = None):
        units = {
            "Секунды": duration,
            "Минуты": duration * 60,
            "Часы": duration * 3600,
            "Дни": duration * 86400,
            "Недели": duration * 604800,
        }

        await member.timeout(duration=units[unit])
        await inter.send(
            embed=await self.bot.embeds.simple(
                title='Мут! (timeout)',
                description=f'Ротик {member.mention} был заклеен, и больше не сможет отработать!)',
                thumbnail=inter.author.display_avatar.url,
                footer={'text': f'А отрабатывал(-а) хорошо?', 'icon_url': member.display_avatar.url},
                fields=[{"name": "Время мута", "value": f'<t:{round(datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(seconds=units[unit])))}:R>', 'inline': True}, {"name": "Причина", "value": reason if reason else "Ещё и безпричинно...", 'inline': True}]
            )
        )

    @commands.slash_command(description="Перепутали участника? Могу убрать с него закляпку :)")
    @commands.has_permissions(ban_members=True)
    async def unmute(self, inter, member: disnake.Member):
        await member.timeout(duration=0)
        await inter.send(embed=await self.bot.embeds.simple(title='Мут снят!', description="Кляп с участника был снят, пусть пока радуется жизни, пока может..)"))

    @commands.slash_command(description="Помогу поставить любой медленный режим на канал")
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, inter, channel: disnake.TextChannel, time: int, unit: Literal['Секунды', 'Минуты', 'Часы']):
        units = {
            "Секунды": time,
            "Минуты": time * 60,
            "Часы": time * 3600,
        }

        if (unit == "Часы" and time > 6) or (unit == "Минуты" and time > 360) or (unit == "Секунды" and time > 3600):
            raise CustomError("Больше 6-ти часов быть не может")
        else:
            await channel.edit(slowmode_delay=units[unit])
        
        await inter.send(
            embed=await self.bot.embeds.simple(
                title='Ненавижу всё медленное!', 
                description=f"Зачем вы так ограничиваете людей?(" if time > 0 else "Медленный режим был успешно убран!", 
                fields=[{"name": "Время", "value": "Нолик :3, Вы убрали медленный режим" if time == 0 else f'{units[unit]} секунд'}]
            )
        )


def setup(bot):
    bot.add_cog(Moderation(bot))
