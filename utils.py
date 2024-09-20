import random
import requests

import database
from common import *
from constants import *


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

    if w.thumbnail is not None:
        embed.set_thumbnail(w.thumbnail)

    return embed


def get_google_images(query: str, num: int = 5):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,  # Search query
        "cx": SEARCH_ENGINE_ID,  # Search engine ID
        "key": GOOGLE_API_KEY,  # Google API key
        "searchType": "image",  # Specify image search
        "num": num,  # Get only the first result
        "imgSize": "MEDIUM",
        "imgType": "clipart"
    }
    response = requests.get(url, params=params).json()

    return [x['link'] for x in response['items']]