from datetime import datetime
from this import d

import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class MarryButton(disnake.ui.View):

    def __init__(self, partner: disnake.Member):
        super().__init__()
        self.partner = partner
        self.value = None
    
    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green)
    async def marry_button_accept(self, button, inter):
        if inter.author.id == self.partner.id:
            await inter.response.send_message("Принять должен тот, кого вы попросили!")
        else:
            await inter.response.send_message(f'{inter.author.mention} Согласен(на) быть партнёром {self.partner.mention}')
            await self.bot.config.DB.marries.insert_one({"_id": inter.author.id, "mate": self.partner.id, 'time': datetime.now()})

        self.value = True
        self.stop()

    @disnake.ui.button(label="Отказать", style=disnake.ButtonStyle.red)
    async def marry_button_cancel(self, button, inter):
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

    @marry_cmd.sub_command(name="invite", description="Предложить сыграть свадьбу кому-либо")
    async def marry_invite(self, inter, member: disnake.Member):
        if await self.bot.config.DB.marries.count_documents({"_id": inter.author.id}) == 0 or \
                await self.bot.config.DB.marries.count_documents({"_id": member.id}) == 0:
            view = MarryButton(partner=inter.author)
            main_description = f"{inter.author.mention} предлагает {member.mention} сыграть свадьбу. Ммм...)"
            embed = await self.bot.embeds.simple(
                        title="Свадьба, получается <3", 
                        description=main_description,
                        footer={"text": "Только, давайте, без беременная в 16, хорошо?", 'icon_url': inter.author.display_avatar.url}
                    )
            message = await inter.send(embed=embed, view=view)

            if view.value:
                embed.description = f"Свадьбе быть! {inter.author.mention} связал(а) свои брачные узы с {member.mention} :3"
                await message.edit(embed=embed)
            else:
                embed.description = f"Свадьбе не быть(. {member.mention} отказал(а) {inter.author.mention}"
                await message.edit(embed=embed)
        else:
            raise CustomError(f"Эм) Вы и/или {member.mention} женаты. На что вы надеетесь?")

    @marry_cmd.sub_command(name='divorce', description="Развод с партнёром")
    async def marry_divorce(self, inter):
        ...

def setup(bot):
    bot.add_cog(Marries(bot))
