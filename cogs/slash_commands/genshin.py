import random
import json
from typing import Literal

import disnake
import genshin
from disnake.ext import commands
from Tools.exceptions import CustomError


class Genshin(commands.Cog, name="гейщит", description="Команды, для того, чтобы получить информацию о каком-либо игроке."):

    COG_EMOJI = "<:WAAAAAAAAA:918940472674758706>"

    async def get_cookie(self, bot):
        return await bot.config.DB.genshin_cookie.find_one({"_id": 598387707311554570}) # до этого было по-другому, но потом мне стало лень всё менять, поэтому оставил, как есть

    async def genshin_client(self, uid, bot):
        my_cookie = await self.get_cookie()
        cookie = dict(ltuid=my_cookie['ltuid'], ltoken=my_cookie['ltoken'])
        client = genshin.Client(cookie, bot)
        return await client.get_genshin_user(uid)

    @commands.slash_command(name="genshin", description="Информация про что-либо из игры Genshin Impact!")
    async def genshin_impact(self, inter):
        ...

    @genshin_impact.sub_command(name='player', description="Информация о игроке")
    async def genshin_player(self, inter, uid: int):
        try:
            user = await self.genshin_client(uid, inter.bot)
            fields = [
                {"name": "Достижения", "value": user.stats.achievements},
                {"name": "Дней активности", "value": user.stats.days_active},
                {"name": "Персонажей", "value": user.stats.characters},
                {"name": "Витая бездна", "value": user.stats.spiral_abyss},
                {"name": "Окулусы", "value": f'Анемокулов: **{user.stats.anemoculi}** | Геокулы: **{user.stats.geoculi}** | Электрокулы: **{user.stats.electroculi}**'},
                {"name": "Сундуки", "value": f'Обычных сундуков: **{user.stats.common_chests}**\nДорогих сундуков: **{user.stats.exquisite_chests}**\nДрагоценных сундуков: **{user.stats.precious_chests}**\nРоскошных сундуков: **{user.stats.luxurious_chests}**'},
                {"name": "Точки", "value": f'Разблокировано точек телепортации: **{user.stats.unlocked_waypoints}**\nРазблокировани подземелий: **{user.stats.unlocked_domains}**'}
            ]

            embed = await inter.bot.embeds.simple(
                title=f"Информация об игроке {uid}",
                description=' | '.join([f'{i.name} - **{str(i.raw_explored).removesuffix(str(i.raw_explored)[-1])}%**' for i in user.explorations]))

            for i in fields:
                embed.add_field(name=i.get('name'), value=i.get('value'), inline=True)

            await inter.send(embed=embed)

        except genshin.errors.AccountNotFound:
            raise CustomError("Аккаунт не найден")
        except genshin.errors.DataNotPublic:
            raise CustomError("Информация игрока не опубликована на hoyolab")
        except genshin.errors.InvalidCookies:
            raise CustomError("Произошла ошибка при поиске. Попробуйте снова.")

    @genshin_impact.sub_command(name="teapot", description="Получение информации о чайнике безмятежности игрока")
    async def genshin_player_teapot(self, inter, uid: int):
        try:
            user = await self.genshin_client(uid)

            if user.teapot is not None:
                fields = [
                    {'name': 'Уровень чайника', 'value': user.teapot.level},
                    {'name': 'Высший уровень комфорта', 'value': f'{user.teapot.comfort_name} — **{user.teapot.comfort}**'},
                    {'name': 'Предметов декора', 'value': user.teapot.items}
                ]

                embed = await inter.bot.embeds.simple(
                    title=f'Информация о чайнике безмятежности {uid}',
                    description=', '.join(list(map(lambda x: x.name, user.teapot.realms)))
                )

                for i in fields:
                    embed.add_field(name=i.get('name'), value=i.get('value'), inline=True)

                await inter.send(embed=embed)
            else:
                raise CustomError("Чайника, пока что, нет.")

        except genshin.errors.AccountNotFound:
            raise CustomError("Аккаунт не найден")
        except genshin.errors.DataNotPublic:
            raise CustomError("Информация игрока не опубликована на hoyolab")
        except genshin.errors.InvalidCookies:
            raise CustomError("Произошла ошибка при поиске. Попробуйте снова.")


def setup(bot):
    bot.add_cog(Genshin(bot))
