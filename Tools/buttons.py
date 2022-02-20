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

class Warns(disnake.ui.View):

    def __init__(self, member: disnake.Member):
        super().__init__()
        self.member = member

    @disnake.ui.button(
        label="Все предупреждения",
        style=disnake.ButtonStyle.blurple
    )
    async def warns(self, button, inter):
        warn_data = "\n".join([f"{i['reason']} | {i['warn_id']}" async for i in Config().DB.warns.find({"guild": inter.guild.id, "member": self.member.id})])
        
        async with aiohttp.ClientSession().post(
            'https://www.toptal.com/developers/hastebin/documents', 
            data=warn_data
        ) as response:
            pastebin_data = await response.json()

        await inter.response.send_message(f"Ваша ссылка: [нажмите, чтобы просмотреть все предупреждения](https://www.toptal.com/developers/hastebin/{pastebin_data['key']})", ephemeral=True)
