import disnake
from disnake.ext import commands
from Tools.exceptions import CustomError


class Logs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, member):
        if member.bot: return

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
                    title="Удалённое сообщение.",
                    description=message.content, 
                    footer={"text": f"Канал: {self.bot.get_channel(await self.get_channel(message.guild)).name}", "icon_url": message.guild.icon.url if message.guild.icon.url else None},
                    fields=[{"name": "Автор сообщения", "value": f"{message.author.mention} [{message.author.name}]"}],
                    url=message.channel.jump_url,
                    thumbnail=message.author.display_avatar.url,
                    color=disnake.Colour.red()
                )
            )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not self.get_channel(after.guild): raise CustomError("Канал логирования не был настроен.")
        elif after.content == before.content: return
        elif len(after.content) > 4096 or len(before.content) > 4096: return 
        else:
            await self.bot.get_channel(await self.get_channel(after.guild)).send(embed=await self.bot.embeds.simple(
                    title="Изменённое сообщение.",
                    description=f'До: {before.content}\nПосле: {after.content}',
                    footer={"text": f"Канал: {self.bot.get_channel(await self.get_channel(after.guild)).name}", "icon_url": after.guild.icon.url if after.guild.icon.url else None},
                    fields=[{"name": "Автор сообщения", "value": f"{after.author.mention} [{str(after.author)}]"}],
                    url=after.jump_url,
                    thumbnail=after.author.display_avatar.url,
                    color=disnake.Colour.dark_orange()
                )
            )

def setup(bot):
    bot.add_cog(Logs(bot))
