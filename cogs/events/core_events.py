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
    async def on_command(self, ctx):
        del self.bot[ctx.command.qualified_name]
        await ctx.reply(f'{ctx.author.name}-Сан! Более обычные команды, начинающиеся с `{ctx.prefix}`, больше работать не будут. Теперь используйте слэш-команды `/`\nНо сначала перепригласите меня, чтобы слэш-команды появились.')
    
def setup(bot):
    bot.add_cog(CoreEvents(bot))
