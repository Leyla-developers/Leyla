import random
import json
from typing import Literal

import disnake
import genshin
from disnake.ext import commands
from Tools.exceptions import CustomError


class Genshin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.data_not_public_info = "Информация не публична. Если вы владелец этого аккаунта, то можете зайти на [hoyolab](https://www.hoyolab.com/home), зайти в свой профиль, зайти в настройки профиля, и в категории боевых заслуг нажать на 'Показывать Боевые заслуги в личном кабинете'"
        self.not_logged_in_info = "**Примечание:** Если вы с телефона, то это сделать невозможно, но вы можете попросить друзей или кого-либо ещё, у кого есть компьютер/ноутбук, чтобы вам всё сделали.\nАвторизация не прошла успешно. Если вы владелец этого аккаунта, то можете зайти на [hoyolab](https://www.hoyolab.com/home), далее зайти в свой профиль. Далее нажимаете F12, application, cookies, и ищите в таблице строки `ltuid` и `ltoken`, и копируете оттуда данные, далее вставляете в команду вновь."

    async def get_cookie(self):
        return await self.bot.config.DB.genshin_cookie.find_one({"_id": 598387707311554570})

    @commands.slash_command(name="genshin", description="Информация про что-либо из игры Genshin Impact!")
    async def genshin_impact(self, inter):
        ...

    @genshin_impact.sub_command(name='player', description="Информация о игроке")
    async def genshin_player(self, inter, uid):
        my_cookie = await self.get_cookie()
        cookie = dict(ltuid=my_cookie['ltuid'], ltoken=my_cookie['ltoken'])
        client = genshin.Client(cookie)
        user = await client.get_genshin_user(uid)

        fields = [{
            "name": "Достижения",
            "value": user.stats.achievements,
        },
        {
            "name": "Дней активности",
            "value": user.stats.days_active
        },
        {
            "name": "Персонажей",
            "value": user.stats.characters,
        },
        {
            "name": "Витая бездна",
            "value": user.stats.spiral_abyss
        },
        {
            "name": "Окулусы",
            "value": f'Анемокулов: **{user.stats.anemoculi}** | Геокулы: **{user.stats.geoculi}** | Электрокулы: **{user.stats.electroculi}**'
        },
        {
            "name": "Сундуки",
            "value": f'Обычных сундуков: **{user.stats.common_chests}**\nДорогих сундуков: **{user.stats.exquisite_chests}**\nДрагоценных сундуков: **{user.stats.precious_chests}**\nРоскошных сундуков: **{user.stats.luxurious_chests}**'
        },
        {
            "name": "Точки",
            "value": f'Разблокировано точек телепортации: **{user.stats.unlocked_waypoints}**\nРазблокировани подземелий: **{user.stats.unlocked_domains}**'
        }]
    
        embed = await self.bot.embeds.simple(
            title=f"Информация об игроке {uid}",
            description=' | '.join([f'{i.name} - **{str(i.raw_explored).removesuffix(str(i.raw_explored)[-1])}%**' for i in user.explorations]))

        for i in fields:
            embed.add_field(name=i.get('name'), value=i.get('value'), inline=True)

        await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(Genshin(bot))
