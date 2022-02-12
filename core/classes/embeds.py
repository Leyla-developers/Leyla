from typing import Union

import disnake
from disnake import Embed
from disnake.ext.commands import Context
from config import Config


class Embeds(Embed):

    def __init__(self, default_color) -> None:
        self.default_color = default_color

    async def simple(
        self, 
        interaction: Union[Context, disnake.ApplicationCommandInteraction] = None, 
        image: str = None, 
        thumbnail: str = None, 
        footer: dict = None,
        fields: list = None,
        **kwargs
    ):
        embed = Embed(**kwargs)

        embed.color = self.default_color if not interaction else await Config().get_guild_data(guild=interaction.guild.id, key='color')

        if interaction:
            embed.set_author(name=interaction.author.display_name, icon_url=interaction.author.display_avatar.url)

        if image:
            embed.set_image(url=image)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if footer:
            embed.set_footer(text=footer.get('text'), icon_url=footer.get('icon_url'))

        if fields:
            for field in fields:
                embed.add_field(name=field.get('name'), value=field.get('value'))

        return embed
