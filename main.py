from asyncio import run

import disnake
from core import Leyla
from config import Config as config


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

run(bot.start(config.TOKEN))
