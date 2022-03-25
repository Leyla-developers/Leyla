import disnake
from disnake.ext import commands


class Voices(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if await self.bot.config.DB.voice.count_documents({"_id": member.guild.id}) == 0:
            ...
        else:
            data = await self.bot.config.DB.voice.find_one({"_id": member.guild.id})
            permissions = {member: disnake.PermissionOverwrite(connect=True, mute_members=True, move_members=True, manage_channels=True)}

            if 'lobby' in data.keys():
                category = self.bot.get_channel(data['lobby'])
            else:
                channel = self.bot.get_channel(data['channel'])

            if category:
                if member in after.channel.members:
                    voice_channel = await category.create_voice_channel(name=f"Комната {member.name}", overwrites=permissions)
                    return
            else:
                if bool(channel.category):
                    voice_channel = await channel.category.create_voice_channel(name=f"Комната {member.name}", overwrites=permissions)
                else:
                    voice_channel = await member.guild.create_voice_channel(name=f"Комната {member.name}", overwrites=permissions)
                return

            await member.move_to(voice_channel)
            await self.bot.wait_for('voice_state_update', check=lambda x, y, z: len(voice_channel.members) == 0)
            await voice_channel.delete()

def setup(bot):
    bot.add_cog(Voices(bot))
