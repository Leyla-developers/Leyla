import disnake
from disnake.ext import commands


class CoreEvents(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == self.bot.user.mention:
            await message.reply('Да, да, что такое? Я здесь, Старшина Сенпай!\nКоманды ты можешь посмотреть, введя `/` и найди мою аватарку в списке ботов. Там будут все команды, которые я могу тебе дать')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(864408447029215232)
        await channel.send(
            embed=await self.bot.embeds.simple(
                title=f'Меня добавили на {guild.name}', 
                fields=[
                    {"name": "Участников", "value": len(guild.member)},
                    {"name": "Ботов", "value": len([i.id for i in guild.members if i.bot])}
                ]
            )
        )

def setup(bot):
    bot.add_cog(CoreEvents(bot))
