import disnake
from disnake.ext import commands


class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if await self.bot.config.DB.afk.count_documents({"guild": message.guild.id}) == 0:
            return

        if message.author.bot:
            return

        guild_afk_members = [i['member'] async for i in self.bot.config.DB.afk.find({"guild": message.guild.id})]

        if message.author.id in guild_afk_members:
            data = await self.bot.config.DB.afk.find_one({"guild": message.guild.id, "member": message.author.id})
            await self.bot.config.DB.afk.delete_one({"guild": message.guild.id, "member": message.author.id})
            await message.channel.send(
                f"Смотрите, кто пришёл! {message.author.mention}, не устал(а) быть в AFK? | Вы пробыли в AFK <t:{round(data['time'].timestamp())}:R> | Причина: {data['reason']}")
        else:
            members = []

            for i in message.mentions:
                if i.id in guild_afk_members:
                    members.append(i.name)
                    return await message.channel.send(
                        f'Ну, вообще-то, эт{"а" if len(members) == 1 else "и"} {"милашка" if len(members) == 1 else "милашки"} в AFK. Не думаю, что {"его(её)" if len(members) == 1 else "их"} стоит тревожить. ({"".join(members)})')


def setup(bot):
    bot.add_cog(Afk(bot))
