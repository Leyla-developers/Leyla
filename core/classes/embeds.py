from typing import Union

import disnake
from disnake import Embed, Integration
from disnake.ext.commands import Context
from config import Config


class Embeds(Embed):

    def __init__(self, default_color) -> None:
        self.default_color = default_color

    async def simple(self, ctx: Union[Context, disnake.ApplicationCommandInteraction]=None, image: str=None, thumbnail: str=None, footer: dict=None, **kwargs):
        embed = Embed(**kwargs)

        embed.color = self.default_color if not ctx else await Config().get_guild_data(guild=ctx.guild.id, key='color')

        if ctx:
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        if image:
            embed.set_image(url=image)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if footer:
            embed.set_footer(text=footer.get('text'), icon_url=footer.get('icon_url'))

        return embed
