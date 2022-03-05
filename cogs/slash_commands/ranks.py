from asyncio import sleep

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Ranks(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, inter):
        if dict(await self.bot.config.DB.levels.find_one({"_id": inter.guild.id}))['mode']:
            return True
        else:
            return False

    async def formula(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        data = dict(await self.bot.config.DB.levels.find_one({"guild": inter.guild.id, "member": member.id}))
        need_xp = 5*(data['lvl']**2)+50*data['lvl']+100

        if data['xp'] >= need_xp:
            return True

        else:
            return False

    async def get_level_up_message(self, message):
        if dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['message']:
            user_data = dict(await self.bot.config.DB.levels.find_one({"guild": message.guild.id, "member": message.author.id}))
            channel_id = dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['channel'] if dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['channel'] else message.channel.id
            data = dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['message']

            data = data.replace("[xp]", str(5*(user_data['lvl']**2)+50*user_data['lvl']+100))
            data = data.replace("[lvl]", str(user_data['lvl']))
            data = data.replace("[member]", message.author.name)
            data = data.replace("[memberMention]", message.author.mention)
            data = data.replace("[channel]", message.channel.mention)

            return await message.guild.get_channel(channel_id).send(data)
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if await self.bot.config.DB.levels.count_documents({"_id": message.guild.id}) == 0:
            await self.bot.config.DB.levels.insert_one({"_id": message.guild.id, "mode": False, "channel": None, "roles": None, "message": None})

        if await self.bot.config.DB.levels.count_documents({"guild": message.guild.id, "member": message.author.id}) == 0:
            await self.bot.config.DB.levels.insert_one({"guild": message.guild.id, "member": message.author.id, "xp": 0, "lvl": 1})

        if message.author.bot: 
            return

        else:
            data = dict(await self.bot.config.DB.levels.find_one({"guild": message.guild.id, "member": message.author.id}))
            lvl = dict(await self.bot.config.DB.levels.find_one({"guild": message.guild.id, "member": message.author.id}))['lvl']

            if dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['mode']:
                if await self.formula(message, message.author):
                    if dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['roles']:
                        for level_role_data in dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['roles']:
                            ...
                        reverse_levels = {value: key for key, value in level_role_data.items()}
                        await message.author.add_roles(message.guild.get_role(int(reverse_levels[[i for i in level_role_data.values() if lvl >= int(i)][0]])))

                    await self.bot.config.DB.levels.update_one({"guild": message.guild.id, "member": message.author.id}, {"$set": {"xp": 0, "lvl": lvl + 1}})
                    await self.get_level_up_message(message)
                else:
                    await sleep(60)
                    await self.bot.config.DB.levels.update_one({"guild": message.guild.id, "member": message.author.id}, {"$set": {"xp": __import__('random').randint(1, 3)+data['xp']}})

    @commands.slash_command(description="Узнать свой (или пользователя) опыт/уровень")
    async def rank(self, inter, member: disnake.Member = commands.Param(lambda inter: inter.author)):
        if member.bot:
            raise CustomError("Боты не имеют этой привелегии :(")
        elif await self.bot.config.DB.levels.find_one({"guild": inter.guild.id, "member": member.id}) is None:
            raise CustomError("Этот человечек ещё не общался тут(")
        elif not await self.cog_check(inter):
            raise CustomError("Система уровней не включена здесь!")
        else:
            data = dict(await self.bot.config.DB.levels.find_one({"guild": inter.guild.id, "member": member.id}))
            await inter.send(embed=await self.bot.embeds.simple(
                    title=f"Опыт и уровень {member.name}", 
                    description=f"Опыт: **{data['xp']}**\nУровень: **{data['lvl']}**",
                    thumbnail=member.display_avatar.url,
                    footer={"text": "Я люблю ананасы", "icon_url": self.bot.user.avatar.url}
                )
            )

def setup(bot):
    bot.add_cog(Ranks(bot))
