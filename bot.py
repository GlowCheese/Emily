import random
import asyncio
import constants

from common import *


bot.load_extension("logger")
bot.load_extension("slashes")


activity = disnake.Activity(type=disnake.ActivityType.playing)

@bot.event
async def on_ready():
    if activity.name is not None: return

    while True:
        activity.name = random.choice([
            "Candy Crush Saga",
            "Angry Birds",
            "Stardew Valley",
            "with your heart"
        ])
        await bot.change_presence(activity=activity)

        await asyncio.sleep(600)


if constants.BOT_TOKEN is None:
    print("Token required")
    exit(0)

bot.run(constants.BOT_TOKEN)
