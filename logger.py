import asyncio
import logging

from disnake.ext import commands

from common import *


logging.basicConfig(
    format='\033[1;32m{asctime} \033[1;37m| '
           '\033[1;34m{levelname} \033[1;37m| '
           '\033[1;31m{name} \033[1;37m| '
           '\033[1;37m{message}',
    level=logging.INFO,
    style='{', datefmt='%d.%m %H:%M'
)
logger = logging.getLogger(__name__)


class Logging(commands.Cog, logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.queue = asyncio.Queue()

    @commands.Cog.listener()
    async def on_ready(self):
        print()
        logger.info('************************************************************')
        logger.info(f'***{f"Logged in as {bot.user}":^{60 - 6}}***')
        logger.info('************************************************************')
        print()

    def emit(self, record):
        self.queue.put_nowait(record)


def setup(bot: commands.AutoShardedInteractionBot):
    logging_cog = Logging()
    logging_cog.setLevel(logging.WARNING)
    logging_cog.setFormatter(
        logging.Formatter(
            fmt='{levelname} | {name} | {message}',
            style='{'))
    logging.getLogger().addHandler(logging_cog)

    bot.add_cog(logging_cog)
