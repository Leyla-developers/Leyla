from datetime import datetime

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Owner(commands.Cog, description="Люблю ебаться в задницу"):

    COG_EMOJI = "👑"

    hidden = True

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[864367089102749726])
    @commands.has_role(918557563241500674)
    async def owner(self, inter):
        ...

    @owner.sub_command(name='give-badge')
    async def owner_give_badge(self, inter, user: disnake.User, badge):
        if await self.bot.config.DB.badges.count_documents({"_id": user.id}) == 0:
            await self.bot.config.DB.badges.insert_one({"_id": user.id, "badges": [str(badge)]})
        else:
            await self.bot.config.DB.badges.update_one({"_id": user.id}, {"$push": {"badges": str(badge)}})

        await inter.send(f'Значок {badge} был выдан **{user.name}**! Интересно, за что?')

    @owner.sub_command(name='link')
    async def link(self, ctx, link: str = None):
        try:
            await self.bot.config.OLD_DB.links.insert_one({"id": "bad", "link": link})
        except:
            raise CustomError('Ссылка уже есть в базе.')

        await ctx.send('Ссылка была добавлена.')

    @owner.sub_command(name='unlink')
    async def unlink(self, ctx, link: str = None):
        await self.bot.config.OLD_DB.links.delete_one({"id": "bad", "link": link})
        await ctx.send('Ссылка была удалена.')

    @owner.sub_command(name="jail")
    async def jail(self, inter, user: disnake.User):
        if await self.bot.config.OLD_DB.jail.count_documents({"_id": user.id}) == 0:
            await self.bot.config.OLD_DB.jail.insert_one({"_id": user.id})
            await inter.send(f'Эта бяка занесена в чёрный список! (**{await self.bot.config.OLD_DB.jail.count_documents({})}**)')
        else:
            await inter.send('Эта бяка и так в чёрном списке! (>~<)')

    @owner.sub_command(name="unjail")
    async def unjail(self, inter, user: disnake.User):
        if await self.bot.config.OLD_DB.jail.count_documents({"_id": user.id}) != 0:
            await self.bot.config.OLD_DB.jail.delete_one({"_id": user.id})
            await inter.send(f'Эта пуфыстя больше не в чёрном списке! (^-^) (**{await self.bot.config.OLD_DB.jail.count_documents({})}**)')
        else:
            await inter.send(f'Эта бяка не в чёрном списке!')

    @owner.sub_command(name="forced-divorce")
    async def force_divorce(self, inter, user: disnake.User):
        marry_data = await self.bot.config.DB.marry.find_one({'$or': [{'_id': user.id}, {'mate': user.id}]})
        user = await self.bot.fetch_user(marry_data['_id'] if marry_data['_id'] != inter.author.id else marry_data['mate'])

        if not await self.bot.config.DB.marry.count_documents({'$or': [{'_id': user.id}, {'mate': user.id}]}):
            raise CustomError('Эти пользователи не женаты.')

        await self.bot.config.DB.marry.delete_one(marry_data)
        await inter.send('Брак принудительно расторгнут.')
    
    @owner.sub_command(name="forced-marry")
    async def force_marry(self, inter, first_user: disnake.User, second_user: disnake.User):
        await self.bot.config.DB.marries.insert_one({"_id": first_user.id, "mate": second_user.id, "time": datetime.now()})
        await inter.send('Пользователь принудительно пожени.. на.. бл*ть, как это писать')


def setup(bot):
    bot.add_cog(Owner(bot))
