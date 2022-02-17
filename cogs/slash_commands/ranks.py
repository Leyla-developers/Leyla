from asyncio import sleep

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Ranks(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    async def formula(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        data = dict(await self.bot.config.DB.levels.find_one({"guild": inter.guild.id, "member": member.id}))
        need_xp = int(((data['lvl'] * 23 / 100) / 0.5) * 1000)

        if data['xp'] >= need_xp:
            return True

        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if await self.bot.config.DB.levels.count_documents({"_id": message.guild.id}) == 0:
            await self.bot.config.DB.levels.insert_one({"_id": message.guild.id, "mode": False, "channel": None})

        if await self.bot.config.DB.levels.count_documents({"guild": message.guild.id, "member": message.author.id}) == 0:
            await self.bot.config.DB.levels.insert_one({"guild": message.guild.id, "member": message.author.id, "xp": 0, "lvl": 1})

        else:
            if dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['mode']:
                data = dict(await self.bot.config.DB.levels.find_one({"guild": message.guild.id, "member": message.author.id}))
                channel_id = dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['channel']
                message_format = {
                    "[xp]": data['xp'],
                    "[lvl]": data['lvl'],
                    "[member]": message.author.name,
                    "[memberMention]": message.author.mention,
                    "[channel]": message.channel.mention
                }

                if await self.formula(message, message.author):
                    lvl = dict(await self.bot.config.DB.levels.find_one({"guild": message.guild.id, "member": message.author.id}))['lvl']
                    await self.bot.config.DB.levels.update_one({"guild": message.guild.id, "member": message.author.id}, {"$set": {"xp": 0, "lvl": lvl + 1}})
                    await message.guild.get_channel(channel_id).send(message_format[dict(await self.bot.config.DB.levels.find_one({"guild": message.guild.id})['message'])])
                else:
                    await sleep(5)
                    await self.bot.config.DB.levels.update_one({"guild": message.guild.id, "member": message.author.id}, {"$set": {"xp": __import__('random').randint(2, 5)+data['xp']}})

    @commands.slash_command(description="Узнать свой (или пользователя) опыт/уровень")
    async def rank(self, inter, member: disnake.Member = commands.Param(lambda inter: inter.author)):
        if member.bot:
            raise CustomError("Боты не имеют этой привелегии :(")
        else:
            data = dict(await self.bot.config.DB.levels.find_one({"guild": inter.guild.id, "member": member.id}))
            await inter.send(embed=await self.bot.embeds.simple(title=f"Опыт и уровень {member.name}", description=f"Опыт: **{data['xp']}**\nУровень: **{data['lvl']}**"))

def setup(bot):
    bot.add_cog(Ranks(bot))
