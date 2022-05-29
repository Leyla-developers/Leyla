import asyncio
from os import environ

import disnake
from core import Leyla
from config import Config
from Tools.help import LeylaHelp

from dotenv import load_dotenv

load_dotenv()

config = Config()

bot = Leyla(
    owner_ids=[598387707311554570],
    command_prefix=Leyla().get_prefix,
    allowed_mentions=disnake.AllowedMentions(
        everyone=False,
        replied_user=True,
        roles=False,
        users=False,
    ),
    strip_after_prefix=True,
    case_insensitive=True,
    status=disnake.Status.dnd,
    intents=disnake.Intents.all(),
    sync_commands=True,
    enable_debug_events=True,
)
bot.help_command = LeylaHelp()
bot.config = config

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.start(environ.get('TOKEN')))
