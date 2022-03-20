from typing import Literal

import disnake
from disnake.ext import commands
from google.translator import GoogleTranslator
from Tools.exceptions import CustomError


class Genshin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.translator = GoogleTranslator()
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
    
        if not character.capitalize() in [i['name'] for i in data]:
            raise CustomError("Такого персонажа нет в игре!")
        else:
            embed.title = character.capitalize()
            embed.description = ''.join([await self.google.translate_async(f"{i['name']} - {i['name']['description']}", 'ru') for i in data if i['name'] == character.capitalize()])

        await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(Genshin(bot))
