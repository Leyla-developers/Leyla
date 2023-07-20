from io import BytesIO
from asyncio import sleep
from typing import NewType
from dataclasses import dataclass
from abc import ABC, abstractmethod
from contextlib import suppress

import disnake
import pymongo
from disnake.ext import commands

from Tools.exceptions import CustomError
from Tools.images import user_rank_card
from Tools.custom_string import level_string
from Tools.paginator import Paginator



Level = NewType('Level', int)
LeylaMemberID = NewType('LeylaMemberID', int)
LeylaRoleID = NewType('LeylaRoleID', int)
LeylaGuildID = NewType('LeylaGuildID', int)


@dataclass
class RankData:
    level: Level
    member: LeylaMemberID
    role: LeylaRoleID
    guild_id: LeylaGuildID


class RanksRepository(ABC):
    @abstractmethod
    async def get_role_by_member_data(self, member: LeylaMemberID, lvl: Level, role: LeylaRoleID) -> RankData: ...


class Ranks(RanksRepository):
    def __init__(self, bot):
        self.bot = bot

    async def get_role_by_member_data(self, guild_id: LeylaGuildID, member_id: LeylaMemberID, lvl: Level, role_id: LeylaRoleID) -> RankData:
        db = await self.bot.config.DB.levels.find_one({"guild": guild_id, 'member': member_id})
        if db['lvl'] >= lvl:
            guild_object = self.bot.get_guild(guild_id)
            member_object = guild_object.get_member(member_id)
            role_object = guild_object.get_role(role_id)
            return await member_object.add_roles(role_object)


class RanksCog(commands.Cog, name="уровни", description="Ну, уровни, да"):
    
    COG_EMOJI = "<:flying_hearts:875710807206416455>"

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, inter):
        return dict(await self.bot.config.DB.levels.find_one({"_id": inter.guild.id}))['mode']

    async def add_level_role(self, guild, member, lvl):
        ranks_class = Ranks(self.bot)
        db = await self.bot.config.DB.levels.find_one({"_id": guild})
        row_data = [{j:k for k, j in i.items()} for i in db['roles']]
        roles = [int(i[0]) for i in list(filter(None, [[k for j, k in i.items() if int(j) <= lvl] for i in row_data]))] # Не делайте так, вы матерям ещё нужны

        for role_id in roles:
            await ranks_class.get_role_by_member_data(guild, member, lvl, role_id)

    async def formula(self, member: disnake.Member):
        data = dict(await self.bot.config.DB.levels.find_one({"guild": member.guild.id, "member": member.id}))
        need_xp = 5*(data['lvl']**2)+50*data['lvl']+100

        return data['xp'] >= need_xp

    async def get_level_up_message(self, message):
        if dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['message']:
            channel_id = dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['channel'] if dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['channel'] else message.channel.id
            data = await level_string(self.bot, message.author)
            return await message.guild.get_channel(channel_id).send(data)

    def get_guild_member_for_leaderboard(self, guild_id: int, member_id: int = None) -> str:
        cached_guild = self.bot.get_guild(guild_id)
        cached_member = cached_guild.get_member(member_id)
        if cached_member is not None:
            return cached_member.mention

        return "Неизвестен"

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        ignore_data = await self.bot.config.DB.levels.find_one({"_id": message.guild.id})

        if await self.bot.config.DB.levels.count_documents({"_id": message.guild.id}) == 0:
            await self.bot.config.DB.levels.insert_one({"_id": message.guild.id, "mode": False, "channel": None, "roles": None, "message": None, "users": [], "category": [], "channels": []})

        if await self.bot.config.DB.levels.count_documents({"guild": message.guild.id, "member": message.author.id}) == 0:
            await self.bot.config.DB.levels.insert_one({"guild": message.guild.id, "member": message.author.id, "xp": 0, "lvl": 1})

        if message.author.bot: 
            return
        
        with suppress(Exception):
            if message.channel.id in ignore_data['channels']:
                return

        with suppress(Exception):
            if message.channel.id in [[i.id for i in self.bot.get_channel(i).channels] for i in ignore_data['category']][0]:
                return

        if message.author.id in ignore_data['users']:
            return

        else:
            data = await self.bot.config.DB.levels.find_one({"guild": message.guild.id, "member": message.author.id})

            if dict(await self.bot.config.DB.levels.find_one({"_id": message.guild.id}))['mode']:
                if await self.formula(message.author):
                    await self.bot.config.DB.levels.update_one({"guild": message.guild.id, "member": message.author.id}, {"$set": {"xp": 0, "lvl": data['lvl'] + 1}})
                    await self.get_level_up_message(message)
                    kostil_ebani = await self.bot.config.DB.levels.find_one({"guild": message.guild.id, "member": message.author.id})
                    await self.add_level_role(message.author.guild.id, message.author.id, kostil_ebani['lvl'])
                else:
                    await sleep(60)
                    kostil_ebani = await self.bot.config.DB.levels.find_one({"guild": message.guild.id, "member": message.author.id})
                    await self.bot.config.DB.levels.update_one({"guild": message.guild.id, "member": message.author.id}, {"$set": {"xp": kostil_ebani['xp']+__import__('random').randint(15, 25)}})

    @commands.slash_command(description="Узнать свой (или пользователя) опыт/уровень")
    async def rank(self, inter, member: disnake.Member = commands.Param(lambda inter: inter.author)):
        if member.bot:
            raise CustomError("Боты не имеют этой привелегии :(")
        elif not await self.bot.config.DB.levels.find_one({"guild": inter.guild.id, "member": member.id}):
            raise CustomError("Этот человечек ещё не общался тут(")
        elif not await self.cog_check(inter):
            raise CustomError("Система уровней не включена здесь!")
        else:
            data = dict(await self.bot.config.DB.levels.find_one({"guild": inter.guild.id, "member": member.id}))
            user_rank_card(
                member, 
                data['lvl'], 
                data['xp'], 
                5*(data['lvl']**2)+50*data['lvl']+100, 
                (data['xp'] / (5*(data['lvl']**2)+50*data['lvl']+100)) * 100
            ).save('user_card.png')
            await inter.send(file=disnake.File(BytesIO(open('user_card.png', 'rb').read()), 'user_card.png'), ephemeral=True)

    @commands.slash_command(description="Список лидеров по уровню.")
    async def leaderboard(self, inter: disnake.ApplicationCommandInteraction):
        embeds = []
        iterable_data = [i async for i in (
            self.bot.config.DB.levels.find({"guild": inter.guild_id})
            .limit(100)
            .sort([("lvl", pymongo.DESCENDING), ("xp", pymongo.DESCENDING)])
        )]
        level_data = [
            f"{position + 1} | {self.get_guild_member_for_leaderboard(inter.guild_id, member_data.get('member'))} - "
            f"{member_data.get('lvl')} | {member_data.get('xp')}" 
            for position, member_data in enumerate(iterable_data)
        ]

        for index, _ in enumerate(level_data):
            if not index % 10 == 0:
                continue

            embed = await self.bot.embeds.simple(title="Лидеры по уровню", description="\n".join(level_data[index:index + 10]))
            embeds.append(embed)

        view = Paginator(pages=embeds, author=inter.author)
        await inter.send(embed=embeds[0], view=view)


def setup(bot):
    bot.add_cog(RanksCog(bot))
