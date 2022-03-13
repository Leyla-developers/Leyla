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
        if not await self.get_channel(message.guild):
            raise CustomError("Канал логирования не был настроен.")
        elif message.author.bot: return
        else:
            await self.bot.get_channel(await self.get_channel(message.guild)).send(embed=await self.bot.embeds.simple(
                    title="Удалённое сообщение.",
                    description=message.content, 
                    footer={"text": f"Канал: {message.channel.name}", "icon_url": message.guild.icon.url if message.guild.icon.url else None},
                    fields=[{"name": "Автор сообщения", "value": f"{message.author.mention} [{message.author.name}]"}],
                    url=message.channel.jump_url,
                    thumbnail=message.author.display_avatar.url,
                    color=disnake.Colour.red()
                )
            )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not await self.get_channel(after.guild): raise CustomError("Канал логирования не был настроен.")
        elif after.content == before.content: return
        elif len(after.content) > 4096 or len(before.content) > 4096: return
        elif after.author.bot: return
        else:
            await self.bot.get_channel(await self.get_channel(after.guild)).send(embed=await self.bot.embeds.simple(
                    title="Изменённое сообщение.",
                    description=f'**До:** {before.content}\n**После:** {after.content}',
                    footer={"text": f"Канал: {after.channel.name}", "icon_url": after.guild.icon.url if after.guild.icon.url else None},
                    fields=[{"name": "Автор сообщения", "value": f"{after.author.mention} [{str(after.author)}]"}],
                    url=after.jump_url,
                    thumbnail=after.author.display_avatar.url,
                    color=disnake.Colour.dark_orange()
                )
            )

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not await self.get_channel(after.guild): raise CustomError("Канал логирования не был настроен.")
        elif before.name == after.name: return
        elif before.display_avatar == after.display_avatar: return
        elif before.banner == after.banner: return
        else:
            embed = await self.bot.embeds.simple(title=f'Изменение участника', url=f"https://discord.com/users/{after.id}")

            if before.banner != after.banner:
                embed.description = f"Баннер {after.name} был сменён.\n[Прошлый баннер]({before.banner.url if before.banner else None}) | [Новый баннер]({after.banner.url if after.banner else None})"
                embed.set_image(url=after.banner.url)
            elif before.display_avatar.url != after.display_avatar.url:
                embed.description = f"Аватар {after.display_avatar.url} был сменён."
                embed.set_image(url=after.display_avatar.url)
            elif before.name != after.name:
                embed.description = f"Никнейм {after.name} был сменён"

            await self.bot.get_channel(await self.get_channel(after.guild)).send(embed=embed)

def setup(bot):
    bot.add_cog(Logs(bot))
