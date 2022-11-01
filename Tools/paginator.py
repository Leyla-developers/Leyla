from typing import List

import disnake

from Tools.exceptions import CustomError


class Paginator(disnake.ui.View):
    def __init__(self, pages: List[disnake.Embed], author: disnake.Member) -> None:
        super().__init__()
        self.author = author
        self.pages = pages
        self.first_page.disabled = True
        self.last_page.disabled = False
        self.page_index = 0
        
    @disnake.ui.button(emoji="<:double_left_arrow:984444620010311692>")
    async def first_page(self, button, inter):
        if not inter.author.id == self.author.id:
            raise CustomError("Не вы вызывали команду!")

        embed = self.pages[0]
        self.first_page.disabled = True
        self.next_page.disabled = False
        self.previous_page.disabled = True
        self.last_page.disabled = False

        await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="<:left_arrow1:984444666797768755>")
    async def previous_page(self, button, inter):
        if not inter.author.id == self.author.id:
            raise CustomError("Не вы вызывали команду!")

        self.page_index -= 1
        embed = self.pages[self.page_index]

        self.next_page.disabled = False
        self.last_page.disabled = False

        if self.page_index == 0:
            self.first_page.disabled = True
            self.previous_page.disabled = True

        await inter.response.edit_message(embed=embed, view=self)
        
    @disnake.ui.button(emoji='❌')
    async def close_paginator(self, button, inter):
        if not inter.author.id == self.author.id:
            raise CustomError("Не вы вызывали команду!")

        await inter.response.defer()
        await inter.delete_original_message()
    
    @disnake.ui.button(emoji="<:right_arrow:984444669679255583>")
    async def next_page(self, button, inter):
        if not inter.author.id == self.author.id:
            raise CustomError("Не вы вызывали команду!")

        self.page_index += 1
        embed = self.pages[self.page_index]

        self.first_page.disabled = False
        self.previous_page.disabled = False

        if self.page_index == len(self.pages) - 1:
            self.next_page.disabled = True
            self.last_page.disabled = True

        await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="<:double_right_arrow:984444618840096798>")
    async def last_page(self, button, inter):
        if not inter.author.id == self.author.id:
            raise CustomError("Не вы вызывали команду!")

        embed = self.pages[-1]
        self.last_page.disabled = True
        self.next_page.disabled = True
        self.previous_page.disabled = False
        self.first_page.disabled = False

        await inter.response.edit_message(embed=embed, view=self)
