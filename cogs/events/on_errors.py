import disnake
from disnake.ext import commands
from Tools.buttons import SupportButton
from Tools.exceptions import CustomError
from genshinstats.errors import DataNotPublic, NotLoggedIn

DESCRIPTIONS = {
    commands.MissingPermissions: "У тебя недостаточно прав, милый \🥺",
    commands.BotMissingPermissions: "У меня нет прав на это(",
    commands.UserNotFound: "Этот человечек не найден, проверь ID/Тег/Никнейм на правильность :eyes:",
    commands.MemberNotFound: "Этот человечек не найден на этом сервере, проверь ID/Тег/Никнейм на правильность :eyes:",
    CustomError: "Произошла какая-то ошибка, можешь прочитать ошибку ниже, Милое моё существо.",
    commands.NSFWChannelRequired: "В этом чате нельзя поразвлекаться(",
    NotLoggedIn: "Авторизация не прошла успешно",
    DataNotPublic: "Информация не публична"
}

PERMISSIONS = {
    "administrator": "Администратор",
    "ban_members": "Банить участников",
    "kick_members": "Выгонять участников",
    "manage_guild": "Управлять сервером"
}

class OnErrors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:blurplecross:918571629997613096>"

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

        if not type(cmd_error) in DESCRIPTIONS.keys():
            embed.add_field(name="Описание ошибки", value=cmd_error)

        if isinstance(cmd_error, commands.NSFWChannelRequired):
            channels = list(map(lambda n: n.mention, filter(lambda x: x.nsfw, ctx.guild.text_channels)))
            embed.add_field(
                name="Поэтому воспользуйтесь одним из NSFW-каналов", 
                value="\n".join(channels) if len(channels) != 0 else "На сервере нет NSFW каналов :("
            )

        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, cmd_error):
        embed = await self.bot.embeds.simple(
            title=f"{self.emoji} Произошла ошибка",
            color=disnake.Colour.red()
        )
        embed.description = DESCRIPTIONS.get(type(cmd_error), "Произошла неизвестная ошибка, пожалуйста, отправьте ошибку на [сервер технической поддержки](https://discord.gg/43zapTjgvm)")

        if isinstance(cmd_error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            embed.add_field(name="Недостающие права", value=", ".join([PERMISSIONS.get(i, i) for i in cmd_error.missing_permissions]))

        if isinstance(cmd_error, CustomError):
            embed.add_field(name="Описание ошибки", value=cmd_error)

        if not type(cmd_error) in DESCRIPTIONS.keys():
            embed.add_field(name="Описание ошибки", value=cmd_error)

        if isinstance(cmd_error, commands.NSFWChannelRequired):
            channels = list(map(lambda n: n.mention, filter(lambda x: x.nsfw, ctx.guild.text_channels)))
            embed.add_field(
                name="Поэтому воспользуйтесь одним из NSFW-каналов", 
                value="\n".join(channels) if len(channels) != 0 else "На сервере нет NSFW каналов :(")

        await ctx.response.send_message(embed=embed, ephemeral=True, view=SupportButton())

def setup(bot):
    bot.add_cog(OnErrors(bot))
