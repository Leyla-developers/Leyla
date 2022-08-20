import asyncio
from threading import Thread

import disnake
from disnake.ext import commands


class CoreEvents(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        alt_ctx = await self.bot.get_context(after)

        if after.content.lower() == before.content.lower() or not alt_ctx.command or after.author.bot:
            return

        emoji = '↩️'
        await after.add_reaction(emoji)

        try:
            await self.bot.wait_for('raw_reaction_add', check=lambda user: user.user_id == after.author.id and user.message_id == after.id, timeout=5)
            await self.bot.process_commands(after)
            await after.clear_reactions()
        except asyncio.TimeoutError:
            await after.clear_reactions()

    @commands.Cog.listener()
    async def on_connect(self):
        print('Я подключилась к этой хуйне.')

        if not self.bot.checks.nsfw.is_running():
            self.bot.checks.nsfw.start()
            
        self.bot.load_extension('cogs.message_intent_commands.music')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == self.bot.user.mention:
            await message.reply('Да, да, что такое? Я здесь, Старшина Сенпай!\nКоманды ты можешь посмотреть, введя `/` и найди мою аватарку в списке ботов. Там будут все команды, которые я могу тебе дать\n\n— Ссылка на сервер: <https://discord.gg/43zapTjgvm>\n— Сайт бота: <https://leylabot.ml/>\n— Пригласи меня и на другие сервера, тыкнув на кнопочку в профиле \🥺')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        channel = self.bot.get_channel(864408447029215232)
        await channel.send(
            embed=await self.bot.embeds.simple(
                title=f'Меня добавили на {guild.name}',
                description=f"Теперь у меня **{len(self.bot.guilds)}** серверов",
                fields=[
                    {"name": "Участников", "value": len(guild.members)},
                    {"name": "Ботов", "value": len([i.id for i in guild.members if i.bot])}
                ],
                image=guild.icon.url if guild.icon else guild.owner.display_avatar.url,
                color=disnake.Color.green()
            )
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(864408447029215232)
        await channel.send(
            embed=await self.bot.embeds.simple(
                title=f'Меня убрали с {guild.name}',
                description=f"Теперь у меня **{len(self.bot.guilds)}** серверов",
                fields=[
                    {"name": "Участников", "value": len(guild.members), "inline": True},
                    {"name": "Ботов", "value": len([i.id for i in guild.members if i.bot]), "inline": True}
                ],
                color=disnake.Color.red()
            )
        )


def setup(bot):
    bot.add_cog(CoreEvents(bot))
