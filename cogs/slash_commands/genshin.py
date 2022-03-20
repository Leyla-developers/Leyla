import statistics
from typing import Literal

import disnake
import genshinstats as genshin
from genshinstats import NotLoggedIn
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
    async def player(self, inter, uid, ltuid, ltoken):
        self.gs.set_cookie(ltuid=ltuid, ltoken=ltoken)

        try:
            data = self.gs.get_user_stats(uid)

            if await self.bot.config.DB.genshin_cookie.count_documents({"_id": inter.author.id}) == 0:
                await self.bot.config.DB.genshin_cookie.insert_one({"_id": inter.author.id})
            else:
                await self.bot.config.DB.genshin_cookie.update_one({"_id": inter.author.id}, {"$set": {"ltuid": ltuid, "ltoken": ltoken}})
        except:
            raise NotLoggedIn


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
                "value": f"Анемокулы: {statistics['anemoculi']} | Геокулы: {statistics['geoculi']} | Электрокулы: {statistics['electroculi']}",
                "inline": True,
            },
            {
                "name": "Собрано сундуков",
                "value": f"Обычных сундуков: {statistics['common_chests']} | Богатых сундуков: {statistics['exquisite_chests']}\nДрагоценных сундуков: {statistics['precious_chests']} | Роскошных сундуков: {statistics['luxurious_chests']}",
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
            }
        ]
        embed = await self.bot.embeds.simple(title=f'Информация о {uid}')
        embed.description = 'Персонажи игрока (из профиля): ' + ', '.join(data['characters'])

        for i in fields:
            embed.add_field(name=i.get('name'), value=i.get('value'), inline=i.get('inline') if i.get('inline') else None)

        await inter.send(embed=embed)


def setup(bot):
    bot.add_cog(Genshin(bot))
