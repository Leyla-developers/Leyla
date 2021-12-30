from os import environ

import jishaku
from disnake.ext import commands
from jishaku.cog import Jishaku
from jishaku.features.baseclass import Feature


class LeylaJishaku(Jishaku):

    COG_EMOJI = '👑'

def setup(bot: commands.Bot):
    jishaku.Flags.NO_UNDERSCORE = True
    jishaku.Flags.FORCE_PAGINATOR = True
    jishaku.Flags.NO_DM_TRACEBACK = True
    environ['JISHAKU_EMBEDDED_JSK'] = 'true'
    bot.add_cog(LeylaJishaku(bot=bot))
