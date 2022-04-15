import disnake
from disnake.ext import commands


class Afk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if await self.bot.config.DB.afk.count_documents({"_id": message.guild.id}) == 0:
            return
        
        data = await self.bot.config.DB.afk.find_one({"_id": message.guild.id})

        if message.author.id in data['afk_members']:
            await self.bot.config.DB.afk.update_one({"_id": message.guild.id}, {"$pull": {"afk_members": message.author.id}})
            await message.channel.send(f"Смотрите, кто пришёл! {message.author.mention}, не устал(а) быть в AFK?")
        else:
            members = [i.name for i in message.mentions if i.id in data['afk_members']]
            if not members:
                return
            else:
                return await message.channel.send(f'Ну, вообще-то, эт{"а" if len(members) == 1 else "и"} {"милашка" if len(members) == 1 else "милашки"} в AFK. Не думаю, что их надо тревожить. ({"".join(members)})')

def setup(bot):
    bot.add_cog(Afk(bot))
