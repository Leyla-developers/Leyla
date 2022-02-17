import disnake
from disnake.ext import commands
from services import waifu_pics
import hmtai


NSFW_DESCRIPTIONS = {
    'Зопки :³': 'ass',
    'БДСМ (Асуждаю)': 'bdsm',
    'КониТИВАААА (Слишком много йогуртика)': 'cum',
    'Да.': 'creampie', 
    'Девушки тоже умеют...': 'femdom', 
    'Просто хентай': 'hentai',
    '×Агрессивные звуки осуждения×': 'incest',
    'Мальчики не одни любят др×чить(': 'masturbation',
    'Эээ.. Ладно.': 'public', 
    'ПаЛюБуЙтЕсЬ': 'ero', 
    'Оргия': 'orgy', 
    'Эльфики uwu': 'elves', 
    'Девочка и девочка, хмм...': 'yuri', 
    '(Мы, если честно, сами не знаем, что это.)': 'pantsu', 
    'В очках тоже неплохо)': 'glasses', 
    'Куколд': 'cuckold', 'Блоуджоб': 'blowjob', 
    'Работа грудью, что)))': 'boobjob', 
    'Ношшшшшшшшшки': 'foot', 'Ещё больше хентая': 
    'hnt_gifs', 'Дыротька, не моя, нет(': 'vagina', 
    'Ахегао, что ещё говорить?': 'ahegao', 
    'Школьницы и не только.. ой.': 'uniform', 
    'Щупальца': 'tentacles'
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
                choices=[disnake.OptionChoice(x, x) for x in NSFW_DESCRIPTIONS.keys()]
            ),
        ]
    )
    @commands.is_nsfw()
    async def nsfw(self, inter: disnake.ApplicationCommandInteraction, choice: str = None):
        embed = await self.bot.embeds.simple(
            inter,
            image=hmtai.useHM("29", NSFW_DESCRIPTIONS[choice])
        )
        return await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(NSFW(bot))
