import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Logs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_channel(self, guild):
        if await self.bot.config.DB.logs.count_documents({"guild": guild.id}) == 0:
            return False
        else:
            return dict(await self.bot.config.DB.logs.find_one({"guild": guild.id}))['channel']

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not self.get_channel(message.guild):
            raise CustomError("Канал логирования не был настроен.")
        else:
            await self.bot.get_channel(await self.get_channel(message.guild)).send(embed=await self.bot.embeds.simple(
                    description='Канал логирования был успешно включен!', 
                    footer={"text": f"Канал: {self.bot.get_channel(await self.get_channel(message.guild)).name}", "icon_url": message.guild.icon.url if message.guild.icon.url else None}
                )
            )

def setup(bot):
    bot.add_cog(Logs(bot))
