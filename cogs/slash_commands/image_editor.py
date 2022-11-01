from PIL import Image
from io import BytesIO
from typing import Union, Literal

import disnake
import easy_pil as pil 
from disnake.ext import commands
from Tools.exceptions import CustomError


class ImageEditor(commands.Cog, name="картинки", description="Работа с изображениями"):

    COG_EMOJI = "<:comen:875434518746644531>"

    @commands.slash_command(name='images', description="Всячески можно изменять картинки")
    async def image_editor(self, inter):
        ...

    @image_editor.sub_command(name='resize', description="Изменение вашего изображения")
    async def image_resize(self, inter, x: int, y: int, image_link: str = None):
        image = inter.author.display_avatar.url if not image_link else image_link

        if (x+y) > (2048+1080):
            raise CustomError('Можно максимум 2К (2048 x 1080)')
        else:
            async with inter.bot.session.get(image) as response:
                data = await response.read()

            img = Image.open(BytesIO(data)).resize((x, y))
            img.save('resized_image.png')
            await inter.send('Ваше изображение ->', file=disnake.File(BytesIO(open('resized_image.png', 'rb').read()), 'resized_image.png'))

    @image_editor.sub_command(name='rotate', description='Вертела я эти ваши картинки...')
    async def rotate_image(self, inter, degree: float, expand: Literal['Изменять размер', 'Не изменять размер'], image: str):
        image = pil.Editor(pil.load_image(image))
        image.rotate(degree, True if expand == 'Изменять размер' else False)
        file = disnake.File(image.image_bytes, f'rotated_image.png')
        await inter.send('Люблю всё вертеть.', file=file)


def setup(bot):
    bot.add_cog(ImageEditor(bot))
