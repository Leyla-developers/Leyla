import disnake
from disnake.ext import commands

from Tools.buttons import SupportButton
from Tools.exceptions import CustomError

DESCRIPTIONS = {
    commands.MissingPermissions: "У тебя недостаточно прав, милый \🥺",
    commands.BotMissingPermissions: "У меня нет прав на это(",
    commands.UserNotFound: "Этот человечек не найден, проверь ID/Тег/Никнейм на правильность :eyes:",
    commands.MemberNotFound: "Этот человечек не найден на этом сервере, проверь ID/Тег/Никнейм на правильность :eyes:",
    CustomError: "Произошла какая-то ошибка, можешь прочитать ошибку ниже, Милое моё существо.",
    commands.NSFWChannelRequired: "В этом чате нельзя поразвлекаться(",
    commands.MissingRequiredArgument: "Вы пропустили какой-то аргумент \🤔",
    commands.NotOwner: "Вы не мой папочка, чтобы мне указывать uwu.",
    commands.RoleNotFound: "Я не нашла такой роли, попробуйте ещё раз!",
    commands.GuildNotFound: "Я не нашла такого сервера!\nПроверьте правильность написания названия/ID. [Ну или вы можете добавить меня туда!)](https://discord.com/oauth2/authorize?client_id=828934385112711188&scope=bot+applications.commands)",
    50013: "У меня нет прав на это("
}

PERMISSIONS = {
    "administrator": "Администратор",
    "ban_members": "Банить участников",
    "kick_members": "Выгонять участников",
    "manage_guild": "Управлять сервером",
    "send_messages": "Отправлять сообщения",
    "view_channel": "Просматривать канал",
    "manage_roles": "Управлять ролями"
}

class OnErrors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:leyla_middle_finger:975200963612803174>"

    @commands.Cog.listener()
    async def on_command_error(self, ctx, cmd_error):
        embed = await self.bot.embeds.simple(
            title=f"{self.emoji} Произошла ошибка",
            color=disnake.Colour.red()
        )
        embed.description = DESCRIPTIONS.get(type(cmd_error), "Произошла неизвестная ошибка, пожалуйста, отправьте ошибку на [сервер технической поддержки](https://discord.gg/43zapTjgvm)")

        if isinstance(cmd_error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            embed.add_field(name="Недостающие права", value=", ".join([PERMISSIONS.get(i, i) for i in cmd_error.missing_permissions]))

        if isinstance(cmd_error, CustomError):
            embed.add_field(name="Описание ошибки", value=cmd_error)
        
        if isinstance(cmd_error, commands.MissingRequiredArgument):
            embed.add_field(name="Использование", value=f"`{ctx.prefix}{ctx.command.usage}`")

        if not type(cmd_error) in DESCRIPTIONS.keys():
            if isinstance(cmd_error, commands.CommandNotFound):
                return

            embed.add_field(name="Описание ошибки", value=cmd_error)

        if isinstance(cmd_error, commands.NSFWChannelRequired):
            channels = list(map(lambda n: n.mention, filter(lambda x: x.nsfw, ctx.guild.text_channels)))
            embed.add_field(
                name="Поэтому воспользуйтесь одним из NSFW-каналов", 
                value="\n".join(channels) if len(channels) != 0 else "На сервере нет NSFW каналов :("
            )

        embed.description = DESCRIPTIONS.get(type(cmd_error), "Произошла неизвестная ошибка, пожалуйста, отправьте ошибку на [сервер технической поддержки](https://discord.gg/43zapTjgvm)")

        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, cmd_error):
        embed = await self.bot.embeds.simple(
            title=f"{self.emoji} Произошла ошибка",
            color=disnake.Colour.red()
        )
        embed.description = DESCRIPTIONS.get(type(cmd_error), "Произошла неизвестная ошибка, пожалуйста, отправьте ошибку на [сервер технической поддержки](https://discord.gg/43zapTjgvm)")

        if isinstance(cmd_error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            embed.add_field(name="Недостающие права", value=", ".join([PERMISSIONS.get(i, i) for i in cmd_error.missing_permissions]))

        if isinstance(cmd_error, CustomError):
            embed.add_field(name="Описание ошибки", value=cmd_error)

        if isinstance(cmd_error, commands.NSFWChannelRequired):
            channels = list(map(lambda n: n.mention, filter(lambda x: x.nsfw, inter.guild.text_channels)))
            embed.add_field(
                name="Поэтому воспользуйтесь одним из NSFW-каналов", 
                value="\n".join(channels) if len(channels) != 0 else "На сервере нет NSFW каналов :("
            )

        embed.description = DESCRIPTIONS.get(type(cmd_error) if not '50013' in str(cmd_error) else 50013, f"Произошла неизвестная ошибка, пожалуйста, отправьте ошибку на [сервер технической поддержки](https://discord.gg/43zapTjgvm)\n```py\n{str(cmd_error)}```")

        await inter.send(embed=embed, ephemeral=True, view=SupportButton())


def setup(bot):
    bot.add_cog(OnErrors(bot))
