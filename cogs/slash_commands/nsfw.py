import disnake
from disnake.ext import commands
from services import waifu_pics
import hmtai


NSFW_DESCRIPTIONS = {
    'ass': 'Зопки :³',
    'bdsm': 'БДСМ (Асуждаю)',
    'cum': 'КониТИВАААА (Слишком много йогуртика)',
    'creampie': 'Да.',
    'femdom': 'Девушки тоже умеют...',
    'hentai': 'Просто хентай',
    'incest': '×Агрессивные звуки осуждения×',
    'masturbation': 'Мальчики не одни любят др×чить(',
    'public': 'Эээ.. Ладно.',
    'ero': 'ПаЛюБуЙтЕсЬ',
    'orgy': 'Оргия',
    'elves': 'Эльфики uwu',
    'yuri': 'Девочка и девочка, хмм...',
    'pantsu': "(Мы, если честно, сами не знаем, что это.)",
    'glasses': 'В очках тоже неплохо)',
    'cuckold': 'Куколд',
    'blowjob': 'Блоуджоб',
    'boobjob': 'Работа грудью, что)))',
    'foot': 'Ношшшшшшшшшки',
    'hnt_gifs': 'Ещё больше хентая',
    'vagina': 'Дыротька, не моя, нет(',
    'ahegao': 'Ахегао, что ещё говорить?',
    'uniform': 'Школьницы и не только.. ой.',
    'tentacles': 'Щупальца',
}

class NSFW(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        description='Взаимодействовать с пользователем',
        options=[
            disnake.Option(
                'choice', 'Выбор картинки', 
                type=disnake.OptionType.string,
                required=True, 
                choices=[disnake.OptionChoice(x, x) for x in NSFW_DESCRIPTIONS]
            ),
        ]
    )
    @commands.is_nsfw()
    async def nsfw(self, inter: disnake.ApplicationCommandInteraction, choice: str = None):
        embed = await self.bot.embeds.simple(
            inter,
            image=hmtai.useHM("29", choice)
        )
        return await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(NSFW(bot))
