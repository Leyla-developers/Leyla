import re

import disnake
from disnake.ext import commands


class AntiInvite(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    DISCORD_INVITE = r'(?:https*:\/\/)?(?:discord\.)?(?:com\/invite|gg)\/[\w\/]+'

    @commands.Cog.listener()
    async def on_message(self, message):
        if len(re.findall(self.DISCORD_INVITE, message.content)) == 0:
            return

        if await self.bot.config.DB.invites.count_documents({"_id": message.guild.id}) == 0:
            return

        data = dict(await self.bot.config.DB.invites.find_one({"_id": message.guild.id}))

        if data['admin_ignore']:
            return
            
        if data['mode']:
            await message.channel.send(data['message']) if data['message'] else None

            if data['action']:
                action_data = data['action']

                match action_data:
                    case 'ban':
                        await message.author.ban(reason="Отправление приглашения [AUTOMOD]")
                    case 'timeout':
                        await message.author.timeout(duration=dict(await self.bot.config.DB.invites.find_one({"_id": message.guild.id}))['action']['duration'])
                    case 'kick':
                        await message.author.kick(reason="Отправление приглашения [AUTOMOD]")
                    case 'warn':
                        await self.bot.config.DB.warns.insert_one({"guild": message.guild.id, "member": message.author.id, "reason": "Не отправляй приглашения! | (Автомодерация)", "warn_id": __import__('random').randint(10000, 99999)})

            await message.delete()


def setup(bot):
    bot.add_cog(AntiInvite(bot))
