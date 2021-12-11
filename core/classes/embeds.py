import disnake
from disnake import Embed
from disnake.ext import commands


class Embeds(Embed):

    def __init__(self, context: commands.Context=None):
        ...
