import disnake
from disnake.ext import commands

from services import waifu_pics


RP_DESCRIPTIONS = {
    'pat': 'Погладил(-а) {user}',
    'hug': 'Обнял(-а) {user}',
    'kiss': 'Поцеловал(-а) {user}',
    'lick': 'Облизнул(-а) {user}',
    'cuddle': 'Прижал(-а) к себе {user}',
    'handhold': 'Взял(-а) за руку {user}',
    'nom': 'Покормил(-а) {user}',
    'slap': 'Дал(-а) пощечину {user}',
    'bite': 'Сделал(-а) кусь {user}',
}


class RolePlay(commands.Cog):

    COG_EMOJI = '🎭'

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        description='Взаимодействовать с пользователем',
        options=[
            disnake.Option('user', 'пользователь', type=disnake.OptionType.user),
            disnake.Option('choice', 'выбор действия', type=disnake.OptionType.string,
                            required=True, choices=[disnake.OptionChoice(x, x) for x in RP_DESCRIPTIONS.keys()])
        ]
    )
    async def rp(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = commands.Param(lambda inter: inter.author), choice: str=None):
        embed = await self.bot.embeds.simple(
            inter, 
            description=f'***{RP_DESCRIPTIONS[choice].format(user=user)}',
            image=await waifu_pics.get_image('sfw', choice, self.bot.session)
        )
        return await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(RolePlay(bot))
