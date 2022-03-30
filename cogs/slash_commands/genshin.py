import random
import json
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
        self.data_not_public_info = "Информация не публична. Если вы владелец этого аккаунта, то можете зайти на [hoyolab](https://www.hoyolab.com/home), зайти в свой профиль, зайти в настройки профиля, и в категории боевых заслуг нажать на 'Показывать Боевые заслуги в личном кабинете'"
        self.not_logged_in_info = "**Примечание:** Если вы с телефона, то это сделать невозможно, но вы можете попросить друзей или кого-либо ещё, у кого есть компьютер/ноутбук, чтобы вам всё сделали.\nАвторизация не прошла успешно. Если вы владелец этого аккаунта, то можете зайти на [hoyolab](https://www.hoyolab.com/home), далее зайти в свой профиль. Далее нажимаете F12, application, cookies, и ищите в таблице строки `ltuid` и `ltoken`, и копируете оттуда данные, далее вставляете в команду вновь."

    @commands.slash_command(name="genshin", description="Информация про что-либо из игры Genshin Impact!")
    async def genshin_impact(self, inter):
        ...

    @genshin_impact.sub_command(description="Информация о игроке")
    async def player(self, inter, uid, ltuid=None, ltoken=None):
        if await self.bot.config.DB.genshin_cookie.count_documents({"_id": inter.author.id}) == 0:
            await self.bot.config.DB.genshin_cookie.insert_one({"_id": inter.author.id})
        else:
            cookie_data = dict(await self.bot.config.DB.genshin_cookie.find_one({"_id": inter.author.id}))
            if None in (ltuid, ltoken, cookie_data.values()):
                cookie_data = random.choice([i async for i in self.bot.config.DB.genshin_cookie.find()])
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

            await inter.send(embed=embed, ephemeral=True)

        except DataNotPublic:
            raise CustomError(self.data_not_public_info)

        except NotLoggedIn:
            raise CustomError(self.not_logged_in_info)

        except AccountNotFound:
            raise CustomError("Такого аккаунта не существует.")

    @genshin_impact.sub_command(name="abyss", description="Информация по витой бездне")
    async def spiral_abyss(self, inter, uid, ltuid=None, ltoken=None):
        if await self.bot.config.DB.genshin_cookie.count_documents({"_id": inter.author.id}) == 0:
            await self.bot.config.DB.genshin_cookie.insert_one({"_id": inter.author.id, "ltuid": ltuid, "ltoken": ltoken})
        else:
            cookie_data = dict(await self.bot.config.DB.genshin_cookie.find_one({"_id": inter.author.id}))
            if None in (ltuid, ltoken, cookie_data.values()):
                cookie_data = random.choice([i async for i in self.bot.config.DB.genshin_cookie.find()])
            else:
                await self.bot.config.DB.genshin_cookie.update_one({"_id": inter.author.id}, {"$set": {"ltuid": ltuid, "ltoken": ltoken}})

            self.gs.set_cookie(ltuid=cookie_data['ltuid'], ltoken=cookie_data['ltoken'])

        try:
            spiral_abyss = self.gs.get_spiral_abyss(uid, previous=True)
            stats = spiral_abyss['stats']
            embed = await self.bot.embeds.simple(title=f"Информация по витой бездне у {uid}")

            for field, value in stats.items():
                embed.add_field(name=''.join(field.title().replace('_', ' ')), value=value)

            await inter.send(embed=embed, ephemeral=True)

        except DataNotPublic:
            raise CustomError(self.data_not_public_info)

        except NotLoggedIn:
            raise CustomError(self.not_logged_in_info)

        except AccountNotFound:
            raise CustomError("Такого аккаунта не существует.")

    @genshin_impact.sub_command(name='player-uid', description="Не можете найти профиль? Тогда можете получить его через HoYoLab!")
    async def get_player_uid_from_hoyolab(self, inter, hoyolab_uid: int):
        if dict(await self.bot.config.DB.genshin_cookie.find_one({"_id": inter.author.id})):
            cookie_data = dict(await self.bot.config.DB.genshin_cookie.find_one({"_id": inter.author.id}))
        else:
            cookie_data = random.choice([i async for i in self.bot.config.DB.genshin_cookie.find()])

        self.gs.set_cookie(ltuid=cookie_data['ltuid'], ltoken=cookie_data['ltoken'])

        if self.gs.is_game_uid(hoyolab_uid):
            raise CustomError("Это игровой UID! Вводите UID человека с HoYoLab!")
        else:
            await inter.send(embed=await self.bot.embeds.simple(description="Ниже можете посмотреть результат :)", fields=[{"name": "HoYoLab ID", "value": hoyolab_uid, "inline": True}, {"name": "Genshin Impact UID", "value": self.gs.get_uid_from_hoyolab_uid(hoyolab_uid), "inline": True}]))

    @genshin_impact.sub_command(name="player-character", description="Информация о персонаже игрока")
    async def get_player_characters(self, inter, uid, character: str, one_or_all: Literal['one', 'all'] = "one"):
        await inter.response.defer()

        if dict(await self.bot.config.DB.genshin_cookie.find_one({"_id": inter.author.id})):
            cookie_data = dict(await self.bot.config.DB.genshin_cookie.find_one({"_id": inter.author.id}))
        else:
            cookie_data = random.choice([i async for i in self.bot.config.DB.genshin_cookie.find()])

        self.gs.set_cookie(ltuid=cookie_data['ltuid'], ltoken=cookie_data['ltoken'])

        try:
            if one_or_all == "one":
                if character is None:
                    raise CustomError("Вы или забыли указать персонажа, или перепутали аргумент 'one' с 'all'")
                else:
                    character_data = lambda x: [str(i[x]) for i in self.gs.get_characters(uid, lang='ru-ru') if i['name'].lower() == character.lower()]
                    list_of_artifacts = [i['artifacts'] for i in self.gs.get_characters(uid, lang='ru-ru') if i['name'].lower() == character.lower()]

                    if character.lower() in [i.lower() for i in character_data('name')]:
                        fields = [
                            {
                                "name": "Раритетность",
                                "value": ''.join(character_data('rarity')),
                                "inline": True
                            },
                            {
                                "name": "Элемент",
                                "value": ''.join(character_data('element')),
                                "inline": True
                            },
                            {
                                "name": "Уровень дружбы",
                                "value": ''.join(character_data('friendship')),
                                "inline": True
                            },
                            {
                                "name": "Созвездий",
                                "value": ''.join(character_data('constellation')),
                                "inline": True
                            },
                            {
                                "name": "Оружие",
                                "value": f"Название: " + json.loads(''.join(character_data('weapon')).replace('"', "'").replace("'", '"'))['name'] + "\nРаритетность: " + str(json.loads(''.join(character_data('weapon')).replace('"', "'").replace("'", '"'))['rarity']),
                                "inline": True
                            },
                        ]
                        description = "```Артефакты:```\n" + ''.join(['\n'.join([f"Название: {j['name']} | Уровень: {j['level']} | Раритетность: {j['rarity']}" for j in i]) for i in list_of_artifacts])
                        await inter.edit_original_message(embed=await self.bot.embeds.simple(title=f'Информация о персонаже {character.title()} | {uid}', description=description, fields=fields, thumbnail=''.join(character_data('icon'))))
                    else:
                        raise CustomError("Этого персонажа нет у игрока!")
            else:
                elements = {
                    "Pyro": "Пиро",
                    "Hydro": "Гидро",
                    "Geo": "Гео",
                    "Dendro": "Дендро",
                    "Cryo": "Крио",
                    "Electro": "Электро",
                    "Anemo": "Анемо"
                }
                characters_data = "\n".join([f"Уровень **{i['level']}** | C{i['constellation']} | Элемент: **{elements[i['element']]}** | {i['name']} {i['rarity']}★ " for i in self.gs.get_characters(uid, lang='ru-ru')])
                await inter.edit_original_message(embed=await self.bot.embeds.simple(title=f'Информация о персонажах {uid}', description=characters_data))

        except DataNotPublic:
            raise CustomError(self.data_not_public_info)

        except AccountNotFound:
            raise CustomError("Такого аккаунта не существует.")

def setup(bot):
    bot.add_cog(Genshin(bot))
