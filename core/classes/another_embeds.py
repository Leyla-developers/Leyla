from typing import NewType, Optional, List
from dataclasses import dataclass
from contextlib import suppress

from disnake import Embed

@dataclass
class Field:
    name: str
    value: str
    inline: Optional[str] = None

@dataclass
class Footer:
    text: Optional[str] = None
    icon_url: Optional[str] = None

@dataclass
class Author:
    name: Optional[str] = None
    icon_url: Optional[str] = None

Thumbnail = NewType('Thumbnail', str)
Image = NewType('Image', str)
Title = NewType('Title', str)
Description = NewType('Description', str)
Url = NewType('Url', str)


class LeylaEmbed:

    def __init__(
        self, 
        title: Optional[Title] = None,
        description: Optional[Description] = None,
        thumbnail: Optional[Thumbnail] = None,
        image: Optional[Image] = None,
        footer: Optional[Footer] = None,
        url: Optional[Url] = None,
        **kwargs
    ) -> None:
        self.title = title
        self.description = description
        self.thumbnail = thumbnail
        self.image = image
        self.footer = footer
        self.url = url

    def start(
        self,
        author: Author = None,
        fields: List[Field] = None
    ):
        embed = Embed()
        embed.color = 0xa8a6f0

        if self.title:
            embed.title = self.title
        if self.description:
            embed.description = self.description
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        if self.image:
            embed.set_image(url=self.image)
        if self.footer:
            embed.set_footer(text=self.footer.text, icon_url=self.footer.icon_url)
        if self.url:
            embed.url = self.url
        if fields:
            with suppress(Exception):
                for i in fields:
                    embed.add_field(name=i.name, value=i.value, inline=i.inline)

        if author:
            embed.set_author(name=author.name, icon_url=author.icon_url)

        return embed
