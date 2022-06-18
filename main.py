import asyncio
from os import environ

import disnake
from core import Leyla
from Tools.help import LeylaHelp

from dotenv import load_dotenv

load_dotenv()

bot = Leyla(
    owner_ids=[598387707311554570],
    allowed_mentions=disnake.AllowedMentions(
        everyone=False,
        replied_user=True,
        roles=False,
        users=True,
    ),
    strip_after_prefix=True,
    case_insensitive=True,
    status=disnake.Status.online,
    intents=disnake.Intents.all(),
    sync_commands=True,
    enable_debug_events=True,
)
bot.help_command = LeylaHelp()

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.start(environ.get('TOKEN')))
