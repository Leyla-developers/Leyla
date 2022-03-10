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

class CurrencyButton(disnake.ui.View):

    def __init__(self):
        super().__init__()
    
    @disnake.ui.button(
        label="Остальные существующие валюты", 
        style=disnake.ButtonStyle.blurple,
    )
    async def currency(self, button, inter):
        cur_data = ['AUD - Австралийский доллар', 'AZN - Азербайджанский манат', 'GBP - Фунт стерлингов Соединенного королевства', 'AMD - Армянских драмов', 'BYN - Белорусский рубль', 'BGN - Болгарский лев', 'BRL - Бразильский реал', 'HUF - Венгерских форинтов', 'HKD - Гонконгский доллар', 'DKK - Датская крона', 'USD - Доллар США', 'EUR - Евро', 'INR - Индийских рупий', 'KZT - Казахстанских тенге', 'CAD - Канадский доллар', 'KGS - Киргизских сомов', 'CNY - Китайский юань', 'MDL - Молдавских леев', 'NOK - Норвежская крона', 'PLN - Польский злотый', 'RON - Румынский лей', 'XDR - СДР (специальные права заимствования)', 'SGD - Сингапурский доллар', 'TJS - Таджикских сомони', 'TRY - Турецких лир', 'TMT - Новый туркменский манат', 'UZS - Узбекских сумов', 'UAH - Украинских гривен', 'CZK - Чешских крон', 'SEK - Шведская крона', 'CHF - Швейцарский франк', 'ZAR - Южноафриканских рэндов', 'KRW - Вон Республики Корея', 'JPY - Японских иен']
        async with aiohttp.ClientSession().post(
            'https://www.toptal.com/developers/hastebin/documents', 
            data=cur_data
        ) as response:
            pastebin_data = await response.json()

        await inter.response.send_message(f"Ваша ссылка: [нажмите, чтобы просмотреть все валюты](https://www.toptal.com/developers/hastebin/{pastebin_data['key']})", ephemeral=True)
