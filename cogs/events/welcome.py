import random

from disnake.ext import commands
from Tools.custom_string import welcome_function


class Welcome(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.bot.config.DB.welcome.count_documents({"_id": member.guild.id}) == 0:
            return
            
        if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['welcome_channel']:
            if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['welcome_message']:
                data = dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))
                message = welcome_function(member, data['welcome_message'])
                
                if 'welcome_messages' in data.keys():
                    message = welcome_function(member, random.choice(data['welcome_messages']))

                await member.guild.get_channel(data['welcome_channel']).send(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if await self.bot.config.DB.welcome.count_documents({"_id": member.guild.id}) == 0:
            return

        if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['goodbye_channel']:
            if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['goodbye_message']:
                data = dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))
                message = welcome_function(member, data['goodbye_message'])

                if 'goodbye_messages' in data.keys():
                    message = welcome_function(member, random.choice(data['goodbye_messages']))

                await member.guild.get_channel(data['goodbye_channel']).send(message)

def setup(bot):
    bot.add_cog(Welcome(bot))
    