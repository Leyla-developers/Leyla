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
    'highfive': 'Дал(-а) пять {user}',
    'kill': 'Убил(-а) {user}'
}

RP_DESCRIPTIONS_MYSELF = {
    'pat': 'Погладил(-а) себя',
    'hug': 'Обнял(-а) себя',
    'kiss': 'Поцеловал(-а) себя',
    'lick': 'Облизнул(-а) себя',
    'cuddle': 'Прижал(-а) себя к себе',
    'handhold': 'Взял(-а) себя за руку',
    'nom': 'Покормил(-а) себя',
    'slap': 'Дал(-а) себе пощёчину',
    'bite': 'Укусил(-а) себя',
    'highfive': 'Дал(-а) себе пять',
    'kill': 'Убил(-а) себя'
}

RP_DESCRIPTIONS_LEYLA = {
    'pat': 'Погладил(-а) {user}',
    'hug': 'Обнял(-а) {user}',
    'kiss': 'Поцеловал(-а) {user}',
    'lick': 'Облизнул(-а) {user}',
    'cuddle': 'Прижал(-а) к себе {user}',
    'handhold': 'Взял(-а) за руку {user}',
    'nom': 'Покормил(-а) {user}',
    'slap': 'Дал(-а) пощечину {user}',
    'bite': 'Ай... За шо? qwq',
    'highfive': '🖐️',
    'kill': 'Заказывает розовый гроб с Хеллоу Китти'
}

class RolePlay(commands.Cog):

    COG_EMOJI = '🎭'

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        description='Взаимодействовать с пользователем',
        options=[
            disnake.Option(
                'choice', 'выбор действия', 
                type=disnake.OptionType.string,
                required=True, 
                choices=[disnake.OptionChoice(x, x) for x in RP_DESCRIPTIONS.keys()]
            ),
            disnake.Option('user', 'пользователь', type=disnake.OptionType.user)
        ]
    )
    async def rp(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = commands.Param(lambda inter: inter.author), choice: str=None):
        descriptions = RP_DESCRIPTIONS if user != inter.author and user != self.bot.user else RP_DESCRIPTIONS_MYSELF if user == inter.author else RP_DESCRIPTIONS_LEYLA
        embed = await self.bot.embeds.simple(
            inter, 
            description=f'***{descriptions[choice].format(user=user)}***',
            image=await waifu_pics.get_image('sfw', choice)
        )
        return await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(RolePlay(bot))
