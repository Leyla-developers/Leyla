import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Family(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='Заключить брак с пользователем')
    async def marry(self, inter, user: disnake.User):
        if user.bot:
            raise CustomError(f'Выне можете вступить в брак с ботом. {user.name} - бот, Ты - человек. Понимаешь? Вы разные!')
        elif user == inter.author:
            raise CustomError('Вы не можете вступить в брак с самим собой.')
        else:
            if self.bot.config.DB.marrys.count_documents({''}):
                ...

    @commands.slash_comand(description='Расторгнуть брак в котором вы состоите')
    async def divorce(self, inter):
        ...

    @commands.slash_comand(description='Усыновить/Удочерить пользователя')
    async def adopt(self, inter):
        ...


def setup(bot):
    bot.add_cog(Family(bot))
