import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class LeylaHelp(commands.HelpCommand):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def command_not_found(self, string):
        raise CustomError(f"Команда **{string}** не найдена! Проверьте правильность написания. Вдруг, вы ошиблись.")
    
    async def send_bot_help(self, mapping):
        embed = await self.bot.embeds.simple(
            title='Книжка заклинаний, ууу...',
            description=f"**Небольшое примечание!** — в основном, я на слэш-командах. Поэтому, прошу, чтобы увидеть полный список моих заклинаний (то бишь, команд), вам нужно ввести `/` и найти в списке мой аватарку",
            fields=[i for i in self.bot.cogs]
        )