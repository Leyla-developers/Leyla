import disnake
from disnake.ext import commands
import hmtai


NSFW_DESCRIPTIONS = {
    'Зопки :³ (ass)': 'ass',
    'БДСМ (Асуждаю) (bdsm)': 'bdsm',
    'КониТИВАААА (Слишком много йогуртика) (cum)': 'cum',
    'Да. (creampie)': 'creampie', 
    'Девушки тоже умеют... (femdom)': 'femdom', 
    'Просто хентай (hentai)': 'hentai',
    '×Агрессивные звуки осуждения× (incest)': 'incest',
    'Мальчики не одни любят др×чить( (masturbation)': 'masturbation',
    'Эээ.. Ладно. (public)': 'public', 
    'ПаЛюБуЙтЕсЬ (ero)': 'ero', 
    'Оргия (orgy)': 'orgy', 
    'Эльфики uwu (elves)': 'elves', 
    'Девочка и девочка, хмм... (yuri)': 'yuri', 
    '(Мы, если честно, сами не знаем, что это.) (pantsu)': 'pantsu', 
    'В очках тоже неплохо) (glasses)': 'glasses', 
    'Куколд (cuckold)': 'cuckold', 
    'Блоуджоб (blowjob)': 'blowjob', 
    'Работа грудью, что))) (boobjob)': 'boobjob', 
    'Ношшшшшшшшшки (foor)': 'foot', 
    'Ещё больше хентая (hentai gifs)': 'hnt_gifs', 
    'Дыротька, не моя, нет( (vagina)': 'vagina', 
    'Ахегао, что ещё говорить? (ahegao)': 'ahegao', 
    'Школьницы и не только.. ой. (uniform)': 'uniform', 
    'Щупальца (tentacles)': 'tentacles'
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
