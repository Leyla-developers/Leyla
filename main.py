import asyncio
from os import environ

import disnake
from core import Leyla
from config import Config


config = Config()


async def init_and_run_bot(token: str) -> None:
    bot = Leyla(
        command_prefix=config.get_prefix(),
        allowed_mentions=disnake.AllowedMentions(
            everyone=False,
            replies=True,
            roles=False,
            users=False,
        ),
        strip_after_prefix=True,
        case_insensitive=True,
        status=disnake.Status.idle,
        intents=disnake.Intents.all()
    )
    bot.config = config
    await bot.start(token)

loop = asyncio.new_event_loop()
loop.run_until_complete(init_and_run_bot(environ['TOKEN']))
