from typing import Literal

import disnake
from disnake.ext import commands
from hikari import EmbedField
from google.translator import GoogleTranslator
from Tools.exceptions import CustomError


class Genshin(commands.Cog):

    def init(self, bot):
        self.bot = bot
        self.translator = GoogleTranslator()
        self.characters_dict = {
            'Diluc': 'Дилюк', 
            'Jean': 'Джинн', 
            'Keqing': 'Кэ Цин', 
            'Klee': 'Кли', 
            'Mona': 'Мона', 
            'Qiqi': 'Ци Ци', 
            'Venti': 'Венти', 
            'Xiao': 'Сяо', 
            'Tartaglia': 'Тарталья', 
            'Zhongli': 'Чжун Ли', 
            'Amber': 'Эмбер', 
            'Barbara': 'Барбара', 
            'Beidou': 'Бэй Доу', 
            'Bennett': 'Беннет', 
            'Chongyun': 'Чун Юнь', 
            'Fischl': 'Фишль', 
            'Kaeya': 'Кэйа', 
            'Lisa': 'Лиза', 
            'Ningguang': 'Нин Гуан', 
            'Noelle': 'Ноэлль', 
            'Razor': 'Рэйзор', 
            'Sucrose': 'Сахароза', 
            'Xiangling': 'Сян Лин', 
            'Xingqiu': 'Син Цю', 
            'Diona': 'Диона', 
            'Xinyan': 'Синь Янь'
        }
        self.google = GoogleTranslator()


    async def unofficial_api(self, endpoint):
        async with self.bot.session.get(f'https://genshinlist.com/api/{endpoint}') as response:
            return await response.json()

    @commands.slash_command(name="genshin-impact", description="Информация про что-либо из игры Genshin Impact!")
    async def genshin_impact(self, inter):
        ...

    @genshin_impact.sub_command(description="Информация о персонажах игры")
    async def characters(self, inter, character):
        data = await self.unofficial_api('characters')
        embed = await self.bot.embeds.simple()

        if not character in [i for i in self.characters_dict.values()] or character not in [i['name'] for i in data]:
            raise CustomError("Такого персонажа нет в игре!")
        else:
            embed.title = character.upper()
            embed.description = [await self.google.translate_async(f"{i['name']} - {i['description']}", 'ru') for i in data if i['name'] == character if character in self.characters_dict.items()]

        await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(Genshin(bot))