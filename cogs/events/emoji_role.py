import disnake
from disnake.ext import commands
import emoji as emj


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
        member = await self.bot.get_guild(payload.guild_id).fetch_member(payload.user_id)

        if member.bot:
            return
        if await self.get_data_from_db(payload.message_id):
            data = dict(await self.get_data_from_db(payload.message_id))
            emoji_data = payload.emoji if payload.emoji in emj.UNICODE_EMOJI_ALIAS_ENGLISH else str(payload.emoji)

            if data['_id'] == payload.message_id:
                for i in data['emojis']:
                    if emoji_data in i.keys():
                        for j in i[emoji_data]:
                            await member.add_roles(self.bot.get_guild(payload.guild_id).get_role(int(j)))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: disnake.RawReactionActionEvent):
        member = await self.bot.get_guild(payload.guild_id).fetch_member(payload.user_id)

        if await self.get_data_from_db(payload.message_id):
            data = dict(await self.get_data_from_db(payload.message_id))
            emoji_data = payload.emoji if payload.emoji in emj.UNICODE_EMOJI_ALIAS_ENGLISH else str(payload.emoji)

            if data['_id'] == payload.message_id:
                for i in data['emojis']:
                    if emoji_data in i.keys():
                        for j in i[emoji_data]:
                            await member.remove_roles(self.bot.get_guild(payload.guild_id).get_role(int(j)))


def setup(bot):
    bot.add_cog(EmojiRole(bot))
