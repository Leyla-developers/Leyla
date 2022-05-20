from datetime import datetime, timedelta
from random import choice, randint

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Economy(commands.Cog, name="экономика", description="Типа экономист, типа богатые. Все дела там, да)0 (Этот модуль в глубокой разработке)"):

    COG_EMOJI = "💰"
    hidden = True

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '💸'

    @commands.command(name="work", description="Работа застанет вас даже здесь!")
    async def economy_work(self, ctx):
        db = self.bot.config.DB.economic
        works = {
            'Грузчик': 1500,
            'Учитель': 500,
            'Разработчик': 2000,
            'Художник': 1750,
            'Дворник': 200,
            'Врач': 1800,
            'Строитель': 2100,
            'Мед. сестра': 500,
            'Лесник': 2000
        }
        work = choice(list(works))
        embed = await self.bot.embeds.simple(
            title='Работы (Экономика)',
            fields=[
                {'name': 'Профессия', 'value': work},
                {'name': 'Сколько заработали', 'value': str(works[work]) + self.emoji}
            ]
        )
        if await db.count_documents({'guild': ctx.guild.id, 'member': ctx.author.id}) == 0:
            await db.insert_one({"guild": ctx.guild.id, 'member': ctx.author.id, 'money': works[work], 'bank': 0, 'work_timeout': datetime.now()})
        else:
            data = await db.find_one({"guild": ctx.guild.id, "member": ctx.author.id})
            time_data = await db.find_one({"guild": ctx.guild.id, 'member': ctx.author.id, 'work_timeout': {'$gte': datetime.now() - timedelta(hours=10)}})
            
            if not time_data:
                await db.update_one({"guild": ctx.guild.id, 'member': ctx.author.id}, {"$set": {'money': data['money']+works[work], 'work_timeout': datetime.now()}})
            else:
                raise CustomError(f"Ээ... Время ещё не пришло! Приходите чуть позже, пожалуйста. Вам нужно ждать до <t:{round((data['work_timeout']+timedelta(hours=10)).timestamp())}:D>")

        await ctx.reply(embed=embed)

    @commands.command(name="daily", description="Просто так получить 1500 💸!")
    async def economy_daily(self, ctx):
        db = self.bot.config.DB.economic
        embed = await self.bot.embeds.simple(
            title='Работы (Экономика)',
            description="Ваши **1500** монет были выданы!"
        )

        if await db.count_documents({'guild': ctx.guild.id, 'member': ctx.author.id}) == 0:
            await db.insert_one({"guild": ctx.guild.id, 'member': ctx.author.id, 'money': 1500, 'bank': 0, 'daily': datetime.now()})
        else:
            data = await db.find_one({"guild": ctx.guild.id, "member": ctx.author.id})
            time_data = await db.find_one({"guild": ctx.guild.id, 'member': ctx.author.id, 'daily': {'$gte': datetime.now() - timedelta(hours=24)}})
            
            if not time_data:
                await db.update_one({"guild": ctx.guild.id, 'member': ctx.author.id}, {"$set": {'money': data['money']+1500, 'daily': datetime.now()}})
            else:
                raise CustomError(f"Ээ... Время ещё не пришло! Приходите чуть позже, пожалуйста. Вам нужно ждать до <t:{round((data['daily']+timedelta(hours=24)).timestamp())}:D>")

        await ctx.reply(embed=embed)

    @commands.command(name="balance", aliases=['bal'], description="Вывод баланса пользователя", usage="balance [Пользователь]")
    async def economy_balance(self, ctx, user: disnake.User = None):
        user = user if bool(user) else ctx.author 
        db = self.bot.config.DB.economic
        embed = await self.bot.embeds.simple(title=f'Баланс {user.name}')
        
        if await db.count_documents({"guild": ctx.guild.id, 'member': user.id}) == 0:
            raise CustomError("У него(-её) совсем пустой кошелёк(")
        else:
            data = await db.find_one({"guild": ctx.guild.id, 'member': user.id})
            embed.description = f'В кошельке: **{data["money"]}** {self.emoji}\nВ банке: **{data["bank"]}** {self.emoji}\nСуммарно: **{data["money"]+data["bank"]}** {self.emoji}'

        await ctx.reply(embed=embed)

    @commands.command(name="deposit", aliases=['dep'], description="Положить все деньги в банк", usage='deposit <Сумма>')
    async def economy_deposit(self, ctx, number: int = None):
        db = self.bot.config.DB.economic
        
        if await db.count_documents({"guild": ctx.guild.id, "member": ctx.author.id}) == 0:
            raise CustomError("У вас и так нет денег, что вы хотите положить в банк?)")
        else:
            data = await db.find_one({"guild": ctx.guild.id, "member": ctx.author.id})

            if data['money'] <= 0:
                raise CustomError("У тебя нет денег!")
            
            number = data['money'] if not bool(number) else number

            if data['money'] < number:
                raise CustomError("У тебя нет столько денег, милый.")
            else:
                await db.update_one({"guild": ctx.guild.id, "member": ctx.author.id}, {"$set": {"money": data['money']-number, "bank": data['bank']+data['money']}})
                await ctx.reply(f"Ваши деньги были положены в банк! Теперь они в целости и сохранности! uwu")

    @commands.command(name="withdraw", aliases=['wd'], description="Положить все деньги в банк", usage='withdraw <Сумма>')
    async def economy_withdraw(self, ctx, number: int = None):
        db = self.bot.config.DB.economic
        
        if await db.count_documents({"guild": ctx.guild.id, "member": ctx.author.id}) == 0:
            raise CustomError("У вас и так нет денег, что вы хотите положить в банк?)")
        else:
            data = await db.find_one({"guild": ctx.guild.id, "member": ctx.author.id})

            if data['bank'] <= 0:
                raise CustomError("У вас нулевой банковский счёт!")
            
            number = data['bank'] if not bool(number) else number

            if data['bank'] < number:
                raise CustomError("У тебя нет столько денег в банке, милый.")
            else:
                await db.update_one({"guild": ctx.guild.id, "member": ctx.author.id}, {"$set": {"money": data['money']+number, "bank": data['bank']-number}})
                await ctx.reply(f"Деньги были положены на Ваш личный счёт!")

    @commands.command(name="rob", description="Ограбить другого участника. Ай-ай-ай, нельзя так! Напишу в полицию! Наверное.")
    async def economy_rob(self, ctx, member: disnake.Member):
        db = self.bot.config.DB.economic

        if await db.count_documents({"guild": ctx.guild.id, "member": member.id}) == 0:
            raise CustomError("Да эта бедняжка и так на мели(")
        elif await db.count_documents({"guild": ctx.guild.id, "member": ctx.author.id}) == 0:
            await db.insert_one({"guild": ctx.guild.id, 'member': ctx.author.id, 'money': 0, 'bank': 0})
        else:
            data = await db.find_one({"guild": ctx.guild.id, "member": member.id})
            robber = await db.find_one({"guild": ctx.guild.id, "member": ctx.author.id})

            if data['money'] < 0:
                raise CustomError("У него(её) нет денег на личном счету, возможно всё в банке или пропил(а) всё")
            else:
                robbed = randint(1, data['money'])
                time_data = await db.find_one({"guild": ctx.guild.id, 'member': ctx.author.id, 'rob_time': {'$gte': datetime.now() - timedelta(hours=5)}})
                
                if not time_data:
                    if robbed > 999:
                        raise CustomError("Более чем 999 украсть нельзя. Возвращайтесь в следующий раз u-u.")
                    elif robbed > data['money']:
                        raise CustomError("Вы попытались выкрасть слишком много, так что, возвращайтесь в следующий раз)")
                    else:
                        await db.update_one({"guild": ctx.guild.id, 'member': member.id}, {"$set": {"money": data['money']-robbed}})
                        await db.update_one({"guild": ctx.guild.id, 'member': ctx.author.id}, {"$set": {"money": robbed + robber['money'], "rob_time": datetime.now()}})
                        await ctx.reply(f'Вы ограбили **{member.name}** на **{robbed}** 💰. Зачем?')
                else:
                    raise CustomError(f"Ээ... Время ещё не пришло! Приходите чуть позже, пожалуйста. Вам нужно ждать до <t:{round((robber['rob_time']+timedelta(hours=5)).timestamp())}:D>")


def setup(bot):
    bot.add_cog(Economy(bot))
