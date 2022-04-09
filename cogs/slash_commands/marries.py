from datetime import datetime

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class MarryButton(disnake.ui.Button):

    def __init__(self, partner: disnake.Member):
        super().__init__()
        self.partner = partner
        self.value = None
    
    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green)
    async def marry_button(self, button, inter):
        if inter.author.id == self.partner.id:
            await inter.response.send_message("Принять должен тот, кого вы попросили!")
        else:
            await inter.response.send_message(f'{inter.author.mention} Согласен(на) быть партнёром {self.partner.mention}')
            await self.bot.config.DB.marries.insert_one({"_id": inter.author.id, "mate": self.partner.id, 'time': datetime.now()})

        self.value = True
        self.stop()

    @disnake.ui.button(label="Отказать", style=disnake.ButtonStyle.red)
    async def marry_button(self, button, inter):
        if inter.author.id == self.partner.id:
            await inter.response.send_message("Нажать должен(на) тот, кого вы попросили!")
        else:
            await inter.response.send_message(f'{inter.author.mention} Не согласен(на) быть партнёром {self.partner.mention}')

        self.value = False
        self.stop()

class Marries(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='marry', description="Свадьбы")
    async def marry_cmd(self, inter):
        ...

    @marry_cmd.sub_command(name="invite")
    async def marry_invite(self, inter, member: disnake.Member):
        if await self.bot.config.DB.marries.count_documents({"_id": inter.author.id}) == 0 or \
                await self.bot.config.DB.marries.count_documents({"_id": member.id}) == 0:
            await inter.send(
                embed=await self.bot.embeds.simple(
                    title="Свадьба, получается", 
                    description=f"{inter.author.mention} и {member.mention} связали брачные узы"
                ), view=MarryButton(partner=inter.author)
            )
        else:
            raise CustomError(f"Эм) Вы и/или {member.mention} женаты. На что вы надеетесь?")

    @marry_cmd.sub_command(name='divorce', description="Развод с партнёром")
    async def marry_divorce(self, inter):
        ...