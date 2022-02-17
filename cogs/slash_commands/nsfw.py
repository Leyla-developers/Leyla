import disnake
from disnake.ext import commands
from services import waifu_pics
import hmtai


NSFW_DESCRIPTIONS = {
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
                'choice', 'Выбор картинки', 
                type=disnake.OptionType.string,
                required=True, 
                choices=[disnake.OptionChoice(x, x) for x in NSFW_DESCRIPTIONS.keys()]
            ),
        ]
    )
    async def nsfw(self, inter: disnake.ApplicationCommandInteraction, choice: str = None):
        embed = await self.bot.embeds.simple(
            inter,
            image=hmtai.useHM("2_4", NSFW_DESCRIPTIONS.get(choice))
        )
        return await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(RolePlay(bot))
