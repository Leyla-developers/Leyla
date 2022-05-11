import asyncio
from os import environ

import disnake
from core import Leyla
from config import Config
from Tools.help import LeylaHelp

from dotenv import load_dotenv

load_dotenv()

config = Config()
intents = disnake.Intents.default()
intents.members = True
intents.message_content = True


async def init_and_run_bot(token: str) -> None:
    bot = Leyla(
        owner_ids=[848593011038224405, 598387707311554570],
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
        intents=intents,
        sync_commands=True,
        enable_debug_events=True,
    )
    bot.config = config
    bot.help_command = LeylaHelp()
    await bot.start(token)

loop = asyncio.get_event_loop()
loop.run_until_complete(init_and_run_bot(environ.get('TOKEN')))
