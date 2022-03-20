import statistics
from typing import Literal

import disnake
import genshinstats as genshin
from genshinstats import NotLoggedIn, DataNotPublic, AccountNotFound
from disnake.ext import commands
from Tools.exceptions import CustomError


class Genshin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.gs = genshin

    @commands.slash_command(name="genshin-impact", description="Информация про что-либо из игры Genshin Impact!")
    async def genshin_impact(self, inter):
        ...

    @genshin_impact.sub_command(description="Информация о игроке")
    async def player(self, inter, uid, ltuid=None, ltoken=None):
        if await self.bot.config.DB.genshin_cookie.count_documents({"_id": inter.author.id}) == 0:
            await self.bot.config.DB.genshin_cookie.insert_one({"_id": inter.author.id})
        else:
            cookie_data = dict(await self.bot.config.DB.genshin_cookie.find_one({"_id": inter.author.id}))
            if None in (ltuid, ltoken):
                pass
            else:
                await self.bot.config.DB.genshin_cookie.update_one({"_id": inter.author.id}, {"$set": {"ltuid": ltuid, "ltoken": ltoken}})

            self.gs.set_cookie(ltuid=cookie_data['ltuid'], ltoken=cookie_data['ltoken'])

        try:
            data = self.gs.get_user_stats(uid)
            statistics = self.gs.get_user_stats(uid)['stats']
            fields = [
                {
                    "name": "Количество персонажей",
                    "value": statistics["characters"],
                    "inline": True
                },
                {
                    "name": "Количество достижений",
                    "value": statistics['achievements'],
                    "inline": True
                },
                {
                    "name": "Дней активности",
                    "value": statistics['active_days'],
                    "inline": True
                },
                {
                    "name": "Витая бездна",
                    "value": statistics['spiral_abyss'],
                    "inline": True
                },
                {
                    "name": "Окулы",
                    "value": f"Анемокулы: **{statistics['anemoculi']}** \n Геокулы: **{statistics['geoculi']}** \n Электрокулы: **{statistics['electroculi']}**",
                    "inline": True,
                },
                {
                    "name": "Собрано сундуков",
                    "value": f"Обычных сундуков: **{statistics['common_chests']}** \n Богатых сундуков: **{statistics['exquisite_chests']}**\nДрагоценных сундуков: **{statistics['precious_chests']}** \n Роскошных сундуков: **{statistics['luxurious_chests']}**",
                    "inline": True,
                },
                {
                    "name": "Разблокировано точек телепортации",
                    "value": statistics['unlocked_waypoints'],
                    "inline": True
                },
                {
                    "name": "Разблокировано подземелий",
                    "value": statistics['unlocked_domains'],
                    "inline": True
                },
                #{
                #    "name": "Изучение мира",
                #    "value": f"Мондштадт: "
                #}
            ]
            embed = await self.bot.embeds.simple(title=f'Информация о {uid}')
            embed.description = f'Персонажи игрока (из профиля) [{len(data["characters"])}]: ' + ', '.join([i['name'] for i in data['characters']])

            for i in fields:
                embed.add_field(name=i.get('name'), value=i.get('value'), inline=i.get('inline') if i.get('inline') else None)

            await inter.send(embed=embed)

        except DataNotPublic:
            raise CustomError("Информация не публична. Если вы владелец этого аккаунта, то можете зайти на [hoyolab](https://www.hoyolab.com/home), зайти в свой профиль, зайти в настройки профиля, и в категории боевых заслуг нажать на 'Показывать Боевые заслуги в личном кабинете'")

        except NotLoggedIn:
            raise CustomError("**Примечание:** Если вы с телефона, то это сделать невозможно, но вы можете попросить друзей или кого-либо ещё, у кого есть компьютер/ноутбук, чтобы вам всё сделали.\nАвторизация не прошла успешно. Если вы владелец этого аккаунта, то можете зайти на [hoyolab](https://www.hoyolab.com/home), далее зайти в свой профиль. Далее нажимаете F12, application, cookies, и ищите в таблице строки `ltuid` и `ltoken`, и копируете оттуда данные, далее вставляете в команду вновь.")

        except AccountNotFound:
            raise CustomError("Такого аккаунта не существует.")

    @genshin_impact.sub_command(name="abyss", description="Информация по витой бездне")
    async def spiral_abyss(self, inter, uid, ltuid=None, ltoken=None):
        if await self.bot.config.DB.genshin_cookie.count_documents({"_id": inter.author.id}) == 0:
            await self.bot.config.DB.genshin_cookie.insert_one({"_id": inter.author.id, "ltuid": ltuid, "ltoken": ltoken})
        else:
            cookie_data = dict(await self.bot.config.DB.genshin_cookie.find_one({"_id": inter.author.id}))
            if None in (ltuid, ltoken):
                pass
            else:
                await self.bot.config.DB.genshin_cookie.update_one({"_id": inter.author.id}, {"$set": {"ltuid": ltuid, "ltoken": ltoken}})

            self.gs.set_cookie(ltuid=cookie_data['ltuid'], ltoken=cookie_data['ltoken'])

        try:
            spiral_abyss = self.gs.get_spiral_abyss(uid, previous=True)
            stats = spiral_abyss['stats']
            embed = await self.bot.embeds.simple(title=f"Информация по витой бездне у {uid}")

            for field, value in stats.items():
                embed.add_field(name=''.join(field.capitalize().replace('_', ' ')), value=value)

            await inter.send(embed=embed)

        except DataNotPublic:
            raise CustomError("Информация не публична. Если вы владелец этого аккаунта, то можете зайти на [hoyolab](https://www.hoyolab.com/home), зайти в свой профиль, зайти в настройки профиля, и в категории боевых заслуг нажать на 'Показывать Боевые заслуги в личном кабинете'")

        except NotLoggedIn:
            raise CustomError("**Примечание:** Если вы с телефона, то это сделать невозможно, но вы можете попросить друзей или кого-либо ещё, у кого есть компьютер/ноутбук, чтобы вам всё сделали.\nАвторизация не прошла успешно. Если вы владелец этого аккаунта, то можете зайти на [hoyolab](https://www.hoyolab.com/home), далее зайти в свой профиль. Далее нажимаете F12, application, cookies, и ищите в таблице строки `ltuid` и `ltoken`, и копируете оттуда данные, далее вставляете в команду вновь.")

        except AccountNotFound:
            raise CustomError("Такого аккаунта не существует.")

def setup(bot):
    bot.add_cog(Genshin(bot))
