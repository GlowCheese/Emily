import random

import database
from common import *

def make_word_card(username: str, word: str):
    w = database.fetch_word(username, word)
    if w is None: return None

    meanings = ""
    for i, meaning in enumerate(w.meanings):
        meanings += f"{i+1}. {meaning}\n"

    embed = disnake.Embed(title=f"{word} ({w.source})")
    embed.color = random.choice(COLORS)
    if len(w.synonyms) > 0:
        synonyms = ", ".join(w.synonyms)
        embed.add_field("Synonyms", synonyms)
    embed.add_field("Meanings", meanings, inline=False)

    return embed
