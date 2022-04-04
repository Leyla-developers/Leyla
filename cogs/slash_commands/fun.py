from io import BytesIO
from PIL import Image
from random import randint, choice

import disnake
from disnake.ext import commands

from Tools.exceptions import CustomError
from Tools.images import ship_image
from services import waifu_pics


OVERLAY_DESCRIPTIONS = {
    'jail': '{user} За шо сидим?',
    'wasted': 'R.I.P. {user} погиб(-ла) смретью храбрых :D',
    'gay': '🤭',
    'triggered': 'ВЫАЫВОАЫАОЫВАЫВАРЫРАВЫРАЛО'
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
    async def random(self, inter: disnake.ApplicationCommandInteraction, a: int, b: int):
        if b < a or a == b:
            raise CustomError('Второе число не должно быть равно первому либо быть меньше чем оно owo') # Я мастер объянсять
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
        async with self.bot.session.get(f'https://some-random-api.ml/canvas/{overlay}?avatar={user.display_avatar.url}') as response:
            image_bytes = BytesIO(await response.read())
            image_filename = f'overlay.{"png" if overlay != "triggered" else "gif"}'
            embed = await self.bot.embeds.simple(inter, title=OVERLAY_DESCRIPTIONS.get(overlay, f'`{user}`'), image=f'attachment://{image_filename}')
            await inter.send(embed=embed, file=disnake.File(image_bytes, filename=image_filename))
            return await response.close()

    @commands.slash_command(
        options=[
            disnake.Option(
                'choice', 'Выберите девАтЬку owo', 
                type=disnake.OptionType.string,
                required=True, 
                choices=['megumin', 'shinobu', 'awoo', 'neko', 'poke']
            )
        ],
        name='anime-girl',
        description="Аниме тянки"
    )
    async def anime_girl(self, inter: disnake.ApplicationCommandInteraction, choice: str):
        embed = await self.bot.embeds.simple(inter, title=f'{choice.title()} OwO', image=await waifu_pics.get_image('sfw', choice.lower()))
        return await inter.send(embed=embed)

    @commands.slash_command(name="ship", description="Создание шип-картинки")
    async def ship_not_ship(
        self, 
        inter, 
        user_one: disnake.User = commands.Param(
            default=lambda inter: inter.author,
            description="Первый пользователь"
        ),
        second_user: disnake.User = commands.Param(
            default=lambda inter: choice(inter.guild.members),
            description="Второй пользователь"
        )
    ):
        percentage = randint(1, 100)
        get_image = ship_image(percentage, user_one, second_user)

        await inter.send(
            embed=await self.bot.embeds.simple(
                title=f'*Толкнула {user_one.name} на {second_user.name}* <:awww:878155710796550145>' if percentage > 30 else 'Хрусь 💔',
                image='attachment://ship_img.png'
            )
        )

def setup(bot):
    bot.add_cog(FunSlashCommands(bot))
