import disnake
from disnake.ext import commands
from Tools.buttons import SupportButton

DESCRIPTIONS = {
    commands.MissingPermissions: "У тебя недостаточно прав, милый \🥺",
    commands.BotMissingPermissions: "У меня нет прав на это(",
    commands.UserNotFound: "Этот человечек не найден, проверь ID/Тег/Никнейм на правильность :eyes:",
    commands.MemberNotFound: "Этот человечек не найден на этом сервере, проверь ID/Тег/Никнейм на правильность :eyes:",
}

PERMISSIONS = {
    "administrator": "Администратор",
    "ban_members": "Банить участников",
    "kick_members": "Выгонять участников",
    "manage_guild": "Управлять гильдией"
}

class OnErrors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:blurplecross:918571629997613096>"

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, cmd_error):
        embed = await self.bot.embeds.simple(
            title=f"{self.emoji} Произошла ошибка в команде **{ctx.command.qualified_name}**",
            color=disnake.Colour.red()
        )

        embed.description = DESCRIPTIONS.get(type(cmd_error), "Произошла неизвестная ошибка, пожалуйста, отправьте ошибку на [сервер технической поддержки](https://discord.gg/43zapTjgvm)")

        if isinstance(cmd_error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            embed.add_field(name="Недостающие права", value=", ".join([PERMISSIONS.get(i, i) for i in cmd_error.missing_permissions]))
        
        if not type(cmd_error) in DESCRIPTIONS.keys():
            embed.add_field(name="**Непрдвиденная** ошибка", value=cmd_error)
            view = SupportButton()

        await ctx.response.send_message(embed=embed, ephemeral=True, view=view or None)

def setup(bot):
    bot.add_cog(OnErrors(bot))
