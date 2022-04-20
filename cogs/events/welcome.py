import random

from disnake.ext import commands


class Welcome(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.bot.config.DB.welcome.count_documents({"_id": member.guild.id}) == 0:
            return
        else:
            if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['welcome_channel']:
                if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['welcome_message']:
                    data = dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))
                    data['welcome_message'] = data['welcome_message'].replace('[memberMention]', member.mention)
                    data['welcome_message'] = data['welcome_message'].replace('[member]', member.name)
                    data['welcome_message'] = data['welcome_message'].replace('[guild]', member.guild.name)
                    data['welcome_message'] = data['welcome_message'].replace('[guildMembers]', str(len(member.guild.members)))
                    
                    if 'welcome_messages' in data.keys():
                        data['welcome_messages'] = [i.replace('[memberMention]', member.mention) for i in data['welcome_messages']]
                        data['welcome_messages'] = [i.replace('[member]', member.name) for i in data['welcome_messages']]
                        data['welcome_messages'] = [i.replace('[guild]', member.guild.name) for i in data['welcome_messages']]
                        data['welcome_messages'] = [i.replace('[guildMembers]', str(len(member.guild.members))) for i in data['welcome_messages']]

                    await member.guild.get_channel(
                        data['welcome_channel']).send(
                            data['welcome_message'] if random.randint(1, 2) == 1 else random.choice(
                                data['welcome_messages']
                        ) if 'welcome_messages' in data.keys() else data['welcome_message']
                    )
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if await self.bot.config.DB.welcome.count_documents({"_id": member.guild.id}) == 0:
            return
        else:
            if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['goodbye_channel']:
                if dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))['goodbye_message']:
                    data = dict(await self.bot.config.DB.welcome.find_one({"_id": member.guild.id}))
                    data['goodbye_message'] = data['goodbye_message'].replace('[memberMention]', member.mention)
                    data['goodbye_message'] = data['goodbye_message'].replace('[member]', member.name)
                    data['goodbye_message'] = data['goodbye_message'].replace('[guild]', member.guild.name)
                    data['goodbye_message'] = data['goodbye_message'].replace('[guildMembers]', str(len(member.guild.members)))
    
                    if 'goodbye_messages' in data.keys():
                        data['goodbye_messages'] = [i.replace('[memberMention]', member.mention) for i in data['goodbye_messages']]
                        data['goodbye_messages'] = [i.replace('[member]', member.name) for i in data['goodbye_messages']]
                        data['goodbye_messages'] = [i.replace('[guild]', member.guild.name) for i in data['goodbye_messages']]
                        data['goodbye_messages'] = [i.replace('[guildMembers]', str(len(member.guild.members))) for i in data['goodbye_messages']]

                    await member.guild.get_channel(
                        data['goodbye_channel']).send(
                            data['goodbye_message'] if random.randint(1, 2) == 1 else random.choice(
                                data['goodbye_messages']
                        ) if 'goodbye_messages' in data.keys() else data['goodbye_message']
                    )

def setup(bot):
    bot.add_cog(Welcome(bot))
