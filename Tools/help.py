import disnake
from disnake.ext import commands
from disnake.ext.commands import HelpCommand
from disnake import SelectOption

from Tools.exceptions import CustomError


class DropDown(disnake.ui.Select):

    def __init__(self, author, options, bot):
        self.options = options
        self.bot = bot
        self.author = author
        super().__init__(
            placeholder="Выберите категорию",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="help_dropdown"
        )

    async def callback(self, inter):
        cog = self.bot.get_cog(self.values[0].lower())
        prefix_data = await self.bot.config.DB.prefix.find_one({"_id": inter.guild.id})
        prefix = prefix_data if prefix_data else {'prefix': 'l.'}
        commands = [f'**{prefix["prefix"]}{i.name}** - {i.description}' for i in cog.get_commands()] if len(cog.get_commands()) > 0 else [f'**/{i.name}** - {i.description}' for i in cog.get_slash_commands()]

        if self.author != inter.author.id:
            await inter.send(
                embed=await self.bot.embeds.simple(
                    title=f"{cog.COG_EMOJI} | {cog.qualified_name.capitalize()}",
                    description=cog.description,
                    fields=[{"name": "Команды этого модуля", "value": '\n'.join(commands)}]
                ), ephemeral=True, view=Views(inter.author, self.options, self.bot)
            )
        else:
            await inter.send('Не вы вызывали справочник!', ephemeral=True)


class Views(disnake.ui.View):

    def __init__(self, author, options, bot):
        super().__init__()
        self.add_item(DropDown(author, options, bot))


class LeylaHelp(HelpCommand):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def generate_options(self, cogs) -> list:
        return [SelectOption(label=cog.qualified_name.capitalize(), description=cog.description, emoji=getattr(cog, 'COG_EMOJI', None)) for cog in cogs]


    def help_message_intent_cog_check(self, cog) -> bool:
        return len(cog.get_commands()) > 0 and not hasattr(cog, 'hidden')


    def help_slash_cog_check(self, cog) -> bool:
        return not hasattr(cog, 'hidden') and len(cog.get_slash_commands()) > 0 and cog.qualified_name
    

    async def command_not_found(self, string) -> str:
        raise CustomError(f"Я не нашла такой команды, как **{string}**! Проверьте правильность написания команды.")


    def get_all_cogs(self) -> list:
        cogs = list(filter(self.help_message_intent_cog_check, [self.context.bot.get_cog(cog) for cog in self.context.bot.cogs]))
        slash_cogs = list(filter(self.help_slash_cog_check, [self.context.bot.get_cog(cog) for cog in self.context.bot.cogs]))
        return (cogs + slash_cogs)

    
    async def send_command_help(self, command) -> str:
        embed = await self.context.bot.embeds.simple(
            title=f'Справка по заклинанию {command.qualified_name}',
            description=command.description,
        )

        if command.usage:
            embed.add_field(name='Правильное использование', value=self.context.clean_prefix + command.usage)

        return await self.context.reply(embed=embed, view=Views(self.context.author, self.generate_options(self.get_all_cogs()), self.context.bot))


    async def send_bot_help(self, mapping):
        embed = await self.context.bot.embeds.simple(
            title=f'Книжка заклинаний, ууу... [**{len(self.context.bot.commands) + len(self.context.bot.global_slash_commands)}** (не считая подкоманд)]',
            url="https://discord.gg/43zapTjgvm",
            description=f"**Небольшое примечание!** — в основном, я на слэш-командах. Поэтому, прошу, чтобы увидеть полный список моих заклинаний (то бишь, команд), вам нужно ввести `/` и найти в списке мою аватарку\n",
        )

        for cog in self.get_all_cogs():
            cog_name = cog.qualified_name.capitalize() if not cog.qualified_name == 'nsfw' else cog.qualified_name.upper()
            embed.description = embed.description + ' ' + f'`{cog_name}`'
        
        await self.context.reply(embed=embed, view=Views(self.context.author, self.generate_options(self.get_all_cogs()), self.context.bot))
