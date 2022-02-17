import disnake
from disnake.ext import commands
from services import waifu_pics
import hmtai


NSFW_DESCRIPTIONS = [
    'ass',
    'bdsm',
    'cum',
    'creampie',
    'femdom',
    'hentai',
    'incest',
    'masturbation',
    'public',
    'ero',
    'orgy',
    'elves',
    'yuri',
    'pantsu',
    'glasses',
    'cuckold',
    'blowjob',
    'boobjob',
    'foot',
    'thighs',
    'vagina',
    'ahegao',
    'uniform',
    'tentacles',
]


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
            image=hmtai.useHM("2_9", choice)
        )
        return await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(NSFW(bot))
