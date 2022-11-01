import disnake
from disnake.ext import commands
import hmtai


class NSFW(commands.Cog, name="nsfw", description="NSFW команды, что-то ещё?"):
    COG_EMOJI = "🥵"
    NSFW_DESCRIPTIONS = {
        'Жопки :³ (ass)': 'ass',
        'БДСМ (Асуждаю) (bdsm)': 'bdsm',
        'Кам) (cum)': 'cum',
        'Крем). (creampie)': 'creampie', 
        'Девушки-доминаторы (femdom)': 'femdom', 
        'Хентай (hentai)': 'hentai',
        '×Агрессивные звуки осуждения... Наверное× (incest)': 'incest',
        'Др×чат девочки, др×чат мальчики (masturbation)': 'masturbation',
        'На публике (public)': 'public', 
        'Ну типа... Напишите моему разработчику в лс, что это(((((( (ero)': 'ero', 
        'Оргия (orgy)': 'orgy', 
        'Эльфики uwu (elves)': 'elves', 
        'Девочка и девочка, и девочка... *Переполнение рекурсии* (yuri)': 'yuri', 
        'Что это (pantsu)': 'pantsu', 
        'Очко (очки) (glasses)': 'glasses', 
        'Куколд (cuckold)': 'cuckold', 
        'Блоуджоб (blowjob)': 'blowjob', 
        'Работа грудью, что))) (boobjob)': 'boobjob', 
        'Ношшшшшшшшшки (foot)': 'foot', 
        # 'Ещё больше хентая (hentai gifs)': 'hnt_gifs', 
        # 'Дыротька, не моя, нет( (vagina)': 'vagina', 
        'Ахегао, что ещё говорить? (ahegao)': 'ahegao', 
        'Школьницы и не только... (uniform)': 'uniform', 
        'Щупальца (tentacles)': 'tentacles'
    }

    @commands.slash_command(description='Ну... Это было неплохо.')
    @commands.is_nsfw()
    async def nsfw(
        self, 
        inter: disnake.ApplicationCommandInteraction, 
        choice: str = commands.Param(choices=[disnake.OptionChoice(x, x) for x in NSFW_DESCRIPTIONS.keys()])
    ):
        embed = await inter.bot.embeds.simple(
            image=hmtai.useHM("29", self.NSFW_DESCRIPTIONS[choice])
        )
        await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(NSFW(bot))
