import disnake
from disnake.ext import commands


class EmojiRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_data_from_db(self, message):
        if await self.bot.config.DB.emojirole.count_documents({"_id": message}) == 0:
            return False
        else:
            return await self.bot.config.DB.emojirole.find_one({"_id": message})

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: disnake.RawReactionActionEvent):
        if await self.get_data_from_db(payload.message_id):
            data = dict(await self.get_data_from_db(payload.message_id))

            if data['_id'] == payload.message_id:
                if payload.emoji in data['emoji'].keys():
                    for i in data['emoji']['roles']:
                        await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(int(i)))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: disnake.RawReactionActionEvent):
        if await self.get_data_from_db(payload.message_id):
            data = dict(await self.get_data_from_db(payload.message_id))

            if data['_id'] == payload.message_id:
                if payload.emoji in data['emoji'].keys():
                    for i in data['emoji']['roles']: # {"emoji": {"here_emoji": [roles]}}
                        await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(int(i)))


def setup(bot):
    bot.add_cog(EmojiRole(bot))
