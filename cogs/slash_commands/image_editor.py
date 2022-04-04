from PIL import Image
from io import BytesIO
from typing import Union

import disnake
import easy_pil as pil 
from disnake.ext import commands
from Tools.exceptions import CustomError


class ImageEditor(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='images')
    async def image_editor(self, inter):
        ...

    @image_editor.sub_command(name='resize', description="Изменение вашего изображения")
    async def image_resize(self, inter, image_link: str, x: int, y: int):
        if (x+y) > (2048+1080):
            raise CustomError('Можно максимум 2К (2048 x 1080)')
        else:
            async with self.bot.session.get(image_link) as response:
                data = await response.read()

            img = Image.open(BytesIO(data)).resize((x, y))
            img.save('resized_image.png')
            await inter.send('Ваше изображение ->', file=disnake.File(BytesIO(open('resized_image.png', 'rb').read()), 'resized_image.png'))

    @image_editor.sub_command(name='rotate', description='Вертела я эти ваши картинки...')
    async def rotate_image(self, inter, degree: float, expand: commands.Param(default=True, choices=['Изменять размер', 'Не изменять размер']), image: Union[disnake.User, str]):
        image = pil.Editor(pil.load_image(image.display_avatar.url))
        image.rotate(degree, expand)
        file = disnake.File(image.image_bytes, f'{image.name}.png')
        await inter.send('Люблю всё вертеть.', file=file)