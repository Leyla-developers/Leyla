from typing import Literal

import disnake
from disnake.ext import commands
from google.translator import GoogleTranslator
from Tools.exceptions import CustomError


class Genshin(commands.Cog):

    def __init__(self, bot):
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
        self.reverse_characters = {value:name for name, value in self.characters_dict}

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
        all_characters = [[i for i in self.characters_dict.values()], [i['name'] for i in data]]
        character_name = ''.join([self.characters_dict[character.capitalize()] if not character.capitalize() in [i for i in self.characters_dict.values()] else self.reverse_characters[character.capitalize()] for i in all_characters if character.capitalize() in i])


        if not character_name in [i for i in all_characters]:
            raise CustomError("Такого персонажа нет в игре!")
        else:
            embed.title = character.upper()
            embed.description = [await self.google.translate_async(f"{character_name} - {i['description']}", 'ru') for i in data]

        await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(Genshin(bot))
