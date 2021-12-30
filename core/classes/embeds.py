from typing import Union

import disnake
from disnake import Embed, Integration
from disnake.ext.commands import Context
from config import Config as config


class Embeds(Embed):

    def __init__(self, default_color) -> None:
        self.default_color = default_color

    async def simple(self, ctx: Union[Context, disnake.ApplicationCommandInteraction]=None, image: str=None, thumbnail: str=None, **kwargs):
        embed = Embed(**kwargs)

        if isinstance(embed.color, type(self.Empty)):
            embed.color = self.default_color if not ctx else config.get_guild_data(guild=ctx.guild.id, key='color')

        if ctx:
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        if image:
            embed.set_image(url=image)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        return embed
