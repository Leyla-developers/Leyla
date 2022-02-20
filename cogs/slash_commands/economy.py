import random

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def where_money(self, inter):
        if await self.bot.config.DB.economic.count_documents({"guild": inter.guild.id, "member": inter.author.id}) == 0:
            return False
        else:
            if dict(await self.bot.config.DB.economic.find_one({"guild": inter.guild.id, "member": inter.author.id}))['balance'] <= 0:
                return False
            else:
                return True

    @commands.slash_command(description="Я тоже своего рода бизнесвумен")
    async def economic(self, inter):
        ...

    @economic.sub_command(description="Если хочешь, могу отплатить тебе uwu. Шансы здесь выиграть - 50/50.")
    async def casino(self, inter, bet: int):
        if not await self.where_money(inter):
            raise CustomError("Дофига богатый шоль? У тебя бабла нет, хату проигрывать собрался(-ась)?")
        else:
            user_balance = dict(await self.bot.config.DB.economic.find_one({"guild": inter.guild.id}))['balance']

            if bet > user_balance:
                raise CustomError("Зачем ты делаешь ставку, которая больше твоего баланса? Я не собираюсь снова отдавать за тебя долги, Сенпай!(")
            else:
                win_or_lose = random.randint(1, 2)
                embed = await self.bot.embeds.simple(title='Казино | Ставки')

                if win_or_lose == 1:
                    await self.bot.config.DB.economic.update_one({"guild": inter.guild.id, "member": inter.author.id}, {"$set": {"balance": user_balance + bet}})
                    embed.description = f"Поздравляю!! Ты выиграл(-а) **{bet}** монеток!"
                else:
                    await self.bot.config.DB.economic.update_one({"guild": inter.guild.id, "member": inter.author.id}, {"$set": {"balance": user_balance - bet}})
                    embed.description = "Ты проиграл(-а)(. Но может быть в следующий раз повезёт!"

                await inter.send(embed=embed)
    
    @economic.sub_command(description="Просмотреть баланс участника")
    async def balance(self, inter, member: disnake.Member = commands.Param(lambda inter: inter.author)):
        data = dict(await self.bot.config.DB.economic.find_one({"guild": inter.guild.id, "member": member.id}))
        await inter.send(embed=await self.bot.embeds.simple(description=f"Баланс {member.name} :о\nПо нашим данным, у него(-её) **{data['balance']}** монет"))


def setup(bot):
    bot.add_cog(Economy(bot))
