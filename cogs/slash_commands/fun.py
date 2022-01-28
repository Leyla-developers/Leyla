from random import randint

import disnake
from disnake.ext import commands, slash_commands


class FunSlashCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Случайное число в заданном диапазоне', )
    async def number(self, inter: disnake.ApplicationCommandInteraction, a: int, b: int):
        return await inter.send(randint(a, b))