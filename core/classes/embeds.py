from typing import Union

from disnake import Embed, Integration
from disnake.ext.commands import Context


class Embeds(Embed):

    def __init__(self, default_color) -> None:
        self.default_color = default_color

    async def simple(self, ctx: Union[Context, Integration]=None, image: str=None, thumbnail: str=None, **kwargs):
        embed = self.from_dict(**kwargs)

        if isinstance(embed.color, self.Empty):
            embed.color = self.default_color if ctx is None else ctx.config.get_guild_data(ctx.guild.id, key='color')

        if ctx is not None:
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        if image is not None:
            embed.set_image(url=image)

        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)

        return embed
