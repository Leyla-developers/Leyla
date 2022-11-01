import disnake
from disnake.ext import commands


class Logs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_channel(self, guild):
        if not await self.bot.config.DB.logs.count_documents({"guild": guild.id}) == 0:
            try:
                return dict(await self.bot.config.DB.logs.find_one({"guild": guild.id}))['channel']
            except AttributeError:
                await self.bot.config.DB.logs.delete_one({"guild": guild.id})

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not await self.get_channel(member.guild): return
        else:
            await self.bot.get_channel(
                await self.get_channel(member.guild)).send(embed=await self.bot.embeds.simple(
                    title="Новый участник тут зашёл :3",
                    fields=[{"name": "Никнейм пользователя", "value": str(member), "inline": True}],
                    footer={"text": f"Дата регистрации: {member.created_at.strftime('%Y.%m.%d %H:%M:%S')}", "icon_url": member.guild.icon.url if member.guild.icon else self.bot.user.avatar.url},
                    thumbnail=member.display_avatar.url,
                    color=disnake.Colour.red()
                )
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not await self.get_channel(member.guild): return
        else:
            await self.bot.get_channel(await self.get_channel(member.guild)).send(embed=await self.bot.embeds.simple(
                    title="Кто-то ушёл отседова...(",
                    fields=[{"name": "Никнейм пользователя", "value": str(member), "inline": True}],
                    footer={"text": f"Дата регистрации: {member.created_at.strftime('%Y.%m.%d %H:%M:%S')}", "icon_url": member.guild.icon.url if member.guild.icon else self.bot.user.avatar.url},                    thumbnail=member.display_avatar.url,
                    color=disnake.Colour.red()
                )
            )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not await self.get_channel(message.guild): return
        elif message.author.bot: return
        else:
            embed = await self.bot.embeds.simple(
                title="Удалённое сообщение.",
                description=message.content, 
                footer={"text": f"Канал: {message.channel.name}", "icon_url": message.guild.icon.url if message.guild.icon else self.bot.user.avatar.url},
                fields=[{"name": "Автор сообщения", "value": f"{message.author.mention} [{message.author.name}]"}],
                url=message.channel.jump_url,
                thumbnail=message.author.display_avatar.url,
                color=disnake.Colour.red()
            )

            if message.attachments:
                embed.set_image(url=message.attachments[0].proxy_url)

            await self.bot.get_channel(await self.get_channel(message.guild)).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not await self.get_channel(after.guild): return
        elif after.content == before.content: return
        elif len(after.content) > 4096 or len(before.content) > 4096: return
        elif after.author.bot: return
        else:
            await self.bot.get_channel(await self.get_channel(after.guild)).send(embed=await self.bot.embeds.simple(
                    title="Изменённое сообщение.",
                    description=f'**До:** {before.content}\n**После:** {after.content}',
                    footer={"text": f"Канал: {after.channel.name}", "icon_url": after.guild.icon.url if after.guild.icon else self.bot.user.avatar.url},
                    fields=[{"name": "Автор сообщения", "value": f"{after.author.mention} [{str(after.author)}]"}],
                    url=after.jump_url,
                    thumbnail=after.author.display_avatar.url,
                    color=disnake.Colour.dark_orange(),
                    image=after.attachments[0].proxy_url if bool(after.attachments) else disnake.embeds.EmptyEmbed
                )
            )

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        embed = await self.bot.embeds.simple(title=f'Изменение профиля участника', url=f"https://discord.com/users/{after.id}")

        if not await self.get_channel(after.guild):
            return

        if not before.name == after.name:
            embed.description = f"Никнейм `{before.name}` был сменён на `{after.name}`"
        elif not before.display_name == after.display_name:
            embed.description = f"Никнейм `{before.display_name}` был сменён на `{after.display_name}`"
        elif not before.display_avatar.url == after.display_avatar.url:
            embed.description = f"Аватар {after.name} был сменён."
            embed.set_image(url=after.display_avatar.url)
        elif not before.banner == after.banner:
            embed.description = f"Баннер {after.name} был сменён.\n[Прошлый баннер]({before.banner.url if before.banner else self.bot.user.avatar.url}) | [Новый баннер]({after.banner.url if after.banner else None})"
            embed.set_image(url=after.banner.url)

        await self.bot.get_channel(await self.get_channel(after.guild)).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        if not await self.get_channel(guild):
            return
        if not await self.bot.config.DB.logs.count_documents({"_id": guild.id}) == 0:
            return

        channel = await self.get_channel(guild)
        embed = await self.bot.embeds.simple(
            title="Бан участника", 
            fields=[
                {"name": "Забаненный", "value": str(member)}
            ]
        )

        await self.bot.get_channel(channel(guild)).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        if not await self.get_channel(guild): return
        if not await self.bot.config.DB.logs.find_one({"_id": guild.id})['moderation']: return
        else:
            channel = await self.get_channel(guild)
            embed = await self.bot.embeds.simple(
                title="Разбан участника", 
                fields=[
                    {"name": "Разбаненный", "value": str(member)}
                ]
            )

            await self.bot.get_channel(channel(guild)).send(embed=embed)

    @commands.Cog.listener()
    async def on_thread_join(self, thread):
        if not await self.get_channel(thread.guild): return
        else:
            await self.bot.get_channel(await self.get_channel(thread.guild)).send(embed=await self.bot.embeds.simple(
                    title="Новая ветка :eyes:",
                    url=thread.jump_url,
                    description=f"Название ветки: **{thread.name}**",
                    footer={"text": f"Дата создания: {thread.created_at.strftime('%Y.%m.%d %H:%M:%S')}", "icon_url": thread.guild.icon.url if thread.guild.icon else self.bot.user.avatar.url},
                    thumbnail=thread.guild.icon.url if thread.guild.icon else self.bot.user.avatar.url,
                    color=disnake.Colour.red()
                )
            )

    @commands.Cog.listener()
    async def on_thread_remove(self, thread):
        if not await self.get_channel(thread.guild): return
        else:
            await self.bot.get_channel(await self.get_channel(thread.guild)).send(embed=await self.bot.embeds.simple(
                    title="Удаление ветки :eyes:",
                    description=f"Ветка называлась **{thread.name}**",
                    thumbnail=thread.guild.icon.url if thread.guild.icon else self.bot.user.avatar.url,
                    color=disnake.Colour.red()
                )
            )


def setup(bot):
    bot.add_cog(Logs(bot))
