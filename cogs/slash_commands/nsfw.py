import disnake
from disnake.ext import commands

from services import waifu_pics


RP_DESCRIPTIONS = {
    'hentai': 'pwp',
    'pussy': '(///////)',
    'boobs': 'o-o',
    'ass': 'p-q',
    'anal': 'qwp',
}


class RolePlay(commands.Cog):

    COG_EMOJI = '<:blurple_lock:918571630358319145>'

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        description='Взаимодействовать с пользователем',
        options=[
            disnake.Option(
                'choice', 'Выбор действия', 
                type=disnake.OptionType.string,
                required=True, 
                choices=[disnake.OptionChoice(x, x) for x in RP_DESCRIPTIONS.keys()]
            ),
            disnake.Option('user', 'Пользователь', type=disnake.OptionType.user)
        ]
    )
    async def nsfw(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = commands.Param(lambda inter: inter.author), choice: str = None):
        embed = await self.bot.embeds.simple(
            inter,
            description=f'***{RP_DESCRIPTIONS[choice].format(user=user)}***',
            image=await waifu_pics.get_image('nsfw', choice)
        )
        return await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(RolePlay(bot))
