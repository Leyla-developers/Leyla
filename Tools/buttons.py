from os import environ

import disnake
from disnake.ext import commands
from config import Config
import aiohttp


class SupportButton(disnake.ui.View):
    
    def __init__(self):
        super().__init__()

    @disnake.ui.button(
        label="Сервер поддержки", 
        style=disnake.ButtonStyle.blurple,
        emoji="✨"
    )
    async def support_server(self, button, inter):
        await inter.response.send_message("Сервер поддержки: https://discord.gg/43zapTjgvm", ephemeral=True)
