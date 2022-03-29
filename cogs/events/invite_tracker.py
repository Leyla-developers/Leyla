import disnake
from disnake.ext import commands


class InviteTracker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.list_invites = {}

    async def get_channel(self, guild):
        if await self.bot.config.DB.invite_tracker.count_documents({"_id": guild.id}) == 0:
            return False
        else:
            return dict(await self.bot.config.DB.invite_tracker.find_one({"_id": guild.id}))['channel']

    def get_invite(self, invites: list, code: str):
        for i in invites:
            if i.code == code:
                return i

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.get_channel(member.guild): return
        else:
            channel = await self.get_channel(member.guild)
            invites = [i for i in await member.guild.invites()][0]
            embed = await self.bot.embeds.simple()

            for i in invites:
                if i.uses < self.get_invite(invites, i.code).uses:
                    embed.title = f"Присоединение по приглашению {self.get_invite(invites, i.code)}"
                    embed.fields = [
                        {"name": "Количество использований", "value": self.get_invite(invites, i.code).uses},
                        {"name": "Приглашённый", "value": str(member)},
                        {"name": "Инвайтер", "value": str(self.get_invite(invites, i.code).inviter)},
                    ]
            await channel.send(embed=embed)