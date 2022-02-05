from random import randint

import disnake
from disnake.ext import commands

from Tools.exceptions import CustomError
from services import waifu_pics


OVERLAY_DESCRIPTIONS = {
    'jail': '{user} За шо сидим?',
}


class FunSlashCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        options=[
            disnake.Option(name='a', type=disnake.OptionType.integer, description='Число от:'),
            disnake.Option(name='b', type=disnake.OptionType.integer, description='Число до:')
        ],
        description='Случайное число в заданном диапазоне'
    )
    async def number(self, inter: disnake.ApplicationCommandInteraction, a: int, b: int):
        if b < a or a == b:
            raise CustomError('Второе число не должно быть равно первому либо быть меньше чем оно') # Я мастер объянсять
        embed = await self.bot.embeds.simple(inter, title=f'Случайное число от `{a}` до `{b}`', thumbnail=inter.author.avatar.url)
        embed.add_field(name='Ваше число...', value=randint(a, b))
        return await inter.send(embed=embed)

    @commands.slash_command(
        options=[
            disnake.Option(
                'overlay', 'выберите наложение', 
                type=disnake.OptionType.string,
                required=True, 
                choices=['wasted', 'jail', 'comrade', 'gay', 'glass', 'passed', 'triggered']
            ),
            disnake.Option('user', 'Выберите пользователя', type=disnake.OptionType.user, required=False)
        ],
        name='avatar-overlay',
        description="Накладывает разные эффекты на аватар."
    )
    async def jail_image(self, inter: disnake.ApplicationCommandInteraction, overlay: str, user: disnake.User = commands.Param(lambda inter: inter.author)):
        embed = await self.bot.embeds.simple(inter, title=OVERLAY_DESCRIPTIONS.get(overlay, f'`{user}`'), image=f'https://some-random-api.ml/canvas/{overlay}?avatar={str(user.avatar)}')
        return await inter.send(embed=embed)

    @commands.slash_command(
        options=[
            disnake.Option(
                'choice', 'Выберите тянку OwO', 
                type=disnake.OptionType.string,
                required=True, 
                choices=['megumin', 'shinobu', 'awoo']
            )
        ],
        name='anime-girl',
        description="Аниме девочки о"
    )
    async def anime_girl(self, inter: disnake.ApplicationCommandInteraction, choice: str):
        embed = await self.bot.embeds.simple(inter, title=f'{choice.title()} OwO', image=await waifu_pics.get_image('sfw', choice.lower()))
        return await inter.send(embed=embed)


def setup(bot):
    bot.add_cog(FunSlashCommands(bot))
