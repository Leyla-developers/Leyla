from os import environ

import disnake
from disnake.ext import commands


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

    def __init__(self):
        super().__init__()

    @disnake.ui.button(
        label="Предупреждения",
        style=disnake.ButtonStyle.red
    )
    async def warns(self, button, inter):
        warn_data = "\n".join([f"{i['reason']} | {i['warn_id']}" async for i in self.bot.config.DB.warns.find({"guild": inter.guild.id})])
        
        async with self.bot.session.post(
            'https://pastebin.com/api/api_post.php', 
            data={"api_dev_key": environ["PASTEBIN"], "api_paste_code": "hi", "api_paste_private": "0", "api_option": "paste"}
        ) as response:
            pastebin_data = await response.read()

        await inter.response.send_message(f"Ваша ссылка: {pastebin_data}", ephemeral=True)