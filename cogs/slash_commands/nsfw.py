import disnake
from disnake.ext import commands


class NSFW(commands.Cog, name="nsfw", description="NSFW команды, что-то ещё?"):
    COG_EMOJI = "🥵"
    NSFW_DESCRIPTIONS = {
        'Жопки :³ (ass)': 'ass',
        'БДСМ (Асуждаю) (bdsm)': 'bdsm',
        'Кам) (cum)': 'cum',
        'Девушки-доминаторы (femdom)': 'femdom', 
        'Хентай (hentai)': 'hentai',
        '×Агрессивные звуки осуждения... Наверное× (incest)': 'incest',
        'Др×чат девочки, др×чат мальчики (masturbation)': 'masturbation',
        'Ну типа... Напишите моему разработчику в лс, что это(((((( (ero)': 'ero', 
        'Оргия (orgy)': 'orgy', 
        'Девочка и девочка, и девочка... *Переполнение рекурсии* (yuri)': 'yuri', 
        'Что это (pantsu)': 'pantsu', 
        'Очко (очки) (glasses)': 'glasses', 
        'Работа ручками (handjob)': 'handjob',
        'Блоуджоб (blowjob)': 'blowjob', 
        'Работа грудью, что))) (boobjob)': 'boobjob',
        'Просто грудь (boobs)': 'boobs',
        'Ношшшшшшшшшки (footjob)': 'footjob', 
        'Ещё больше хентая (hentai gifs)': 'gif', 
        'Ахегао, что ещё говорить? (ahegao)': 'ahegao', 
        'Школьницы и не только... (uniform)': 'uniform', 
        'Щупальца (tentacles)': 'tentacles',
        'Бёдра (thighs)': 'thighs',
        'Кошко-девочки (nsfw neko)': 'nsfwNeko',
        'Юбочки (zettai ryouiki)': 'zettaiRyouiki',
    }

    @commands.slash_command(description='Ну... Это было неплохо.')
    @commands.is_nsfw()
    async def nsfw(
        self, 
        inter: disnake.ApplicationCommandInteraction, 
        choice: str = commands.Param(choices=[disnake.OptionChoice(x, x) for x in NSFW_DESCRIPTIONS.keys()])
    ):
        async with inter.bot.session.get(f'https://hmtai.hatsunia.cfd/nsfw/{self.NSFW_DESCRIPTIONS.get(choice)}') as response:
            data = await response.json()

        embed = await inter.bot.embeds.simple(
            image=data['url']
        )
        await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(NSFW(bot))
