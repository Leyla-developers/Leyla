import disnake


class Paginator(disnake.ui.View):

    def __init__(self, embeds: list):
        super().__init__()
        self.embeds = embeds
        self.count = 0
        self.first = True
        self.back = True

    @disnake.ui.button(emoji="⏪", style=disnake.ButtonStyle.blurple)
    async def first(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.count = 0
        embed = self.embeds[self.count]
        embed.set_footer(text=f"Page 1 of {len(self.embeds)}")
        self.first = True
        self.back = True
        self.next_page = False
        self.last_page = False

        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.secondary)
    async def back(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.count -= 1
        embed = self.embeds[self.count]
        self.next_page = False
        self.last_page = False
        
        if self.count == 0:
            self.first = True
            self.back = True

        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.red)
    async def remove(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.delete_original_message()

    @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.secondary)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.count += 1
        embed = self.embeds[self.count]
        self.first = False
        self.back = False

        if self.count == (len(self.embeds) - 1):
            self.next_page = True
            self.last_page = True

        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="⏩", style=disnake.ButtonStyle.blurple)
    async def last_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.count = len(self.embeds) - 1
        embed = self.embeds[self.count]
        self.first = False
        self.back = False
        self.next_page = True
        self.last_page = True

        await interaction.response.edit_message(embed=embed, view=self)
