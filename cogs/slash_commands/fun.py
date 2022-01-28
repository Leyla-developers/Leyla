from random import randint

import disnake
from disnake.ext import commands

from services import waifu_pics


class FunSlashCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=[885541278908043304],
        options=[
            disnake.Option(name='a', type=disnake.OptionType.integer, description='Число от:'),
            disnake.Option(name='b', type=disnake.OptionType.integer, description='Число до:')
        ],
        description='Случайное число в заданном диапазоне'
    )
    async def number(self, inter: disnake.ApplicationCommandInteraction, a: int, b: int):
        embed = self.bot.embeds.simple(title=f'Случайное число от `{a}` до `{b}`', thumbnail=inter.author.avatar.url)
        embed.add_field(name='Ваше число...', value=randint(a, b))
        return await inter.send(embed=embed)

    @commands.slash_command(
        guild_ids=[885541278908043304],
        options=[
            disnake.Option(
                'choice', 'выберите наложение', 
                type=disnake.OptionType.string,
                required=True, 
                choices=['wasted', 'jail', 'comrade', 'gay', 'glass', 'passed', 'triggered']
            ),
            disnake.Option('user', 'Выберите пользователя', type=disnake.OptionType.user, required=False)
        ],
        name='avatar-overlay'
    )
    async def jail_image(self, inter: disnake.ApplicationCommandInteraction, overlay: str, user: disnake.User = commands.Param(lambda inter: inter.author)):
        embed = self.bot.embeds.simple(title=f'`{user}` За шо сидит?', image=f'https://some-random-api.ml/canvas/{overlay}?avatar={str(user.avatar)}')
        return await inter.send(embed=embed)

    @commands.slash_command(
        guild_ids=[885541278908043304],
        options=[
            disnake.Option(
                'choice', 'Выберите тянку OwO', 
                type=disnake.OptionType.string,
                required=True, 
                choices=['megumin', 'shinobu', 'awoo']
            )
        ],
        name='anime-girl'
    )
    async def anime_girl(self, inter: disnake.ApplicationCommandInteraction, choice: str):
        embed = self.bot.embeds.simple(title=f'{choice.title()} OwO', image=await waifu_pics.get_image('sfw', choice.lower()))
        return await inter.send(embed=embed)


def setup(bot):
    bot.add_cog(FunSlashCommands(bot))
