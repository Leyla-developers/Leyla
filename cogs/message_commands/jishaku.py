from os import environ

import jishaku
from disnake.ext import commands
from jishaku.cog import STANDARD_FEATURES, OPTIONAL_FEATURES, Jishaku
from jishaku.features.baseclass import Feature

from config import Config


config = Config()


class Jishaku(*OPTIONAL_FEATURES, *STANDARD_FEATURES):

    COG_EMOJI = '👑'

    @Feature.Command(parent='jsk', name='test')
    async def test(self, ctx):
        return await ctx.reply('Ok')


def setup(bot: commands.Bot):
    jishaku.Flags.NO_UNDERSCORE = True
    jishaku.Flags.FORCE_PAGINATOR = True
    jishaku.Flags.NO_DM_TRACEBACK = True
    environ['JISHAKU_EMBEDDED_JSK'] = 'true'
    environ['JISHAKU_EMBEDDED_JSK_COLOUR'] = str(config.DEFAULT_GUILD_DATA['color']).replace('0x', '#')
    bot.add_cog(Jishaku(bot))
