from PIL import Image, ImageDraw

import disnake
from disnake.ext import commands


class Memes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command()
    async def demotivator(self, inter, top_text: str, bottom_text: str, font_size: int, image: str = None):
        ...
