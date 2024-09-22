import time
import random
import requests
import functools

from typing import Any, Callable, Dict

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


class LazyData:
    def __init__(self, fetch: Callable[[], Any], lazy_time = 100):
        """
        Initialize LazyData object.

        :param fetch: A callable that fetches the data when needed.
        :param lazy_time: Time in seconds to wait before fetching new data.
        """
        self.fetch = fetch
        self.value = None
        self.lazy_time = lazy_time
        self.last_fetch = 0

    def get(self) -> Any:
        """
        Fetch the value lazily. If enough time has passed since the last fetch, it refetches the value.
        
        :return: The fetched value.
        """
        if self.last_fetch + self.lazy_time < int(time.time()):
            self.value = self.fetch()
            self.last_fetch = int(time.time())
        return self.value


class LazyDict:
    def __init__(self, fetch: Callable[[Any], Any], lazy_time = 100):
        """
        Initialize LazyDict object.

        :param fetch: A callable that fetches the data for a given key when needed.
        :param lazy_time: Time in seconds to wait before refetching the data for any key.
        """
        self.fetch = fetch
        self.value: Dict[Any, LazyData] = {}
        self.lazy_time = lazy_time

    def get(self, key: Any) -> Any:
        """
        Get the value associated with the given key, fetching it lazily if necessary.

        :param key: The key to look up.
        :return: The value associated with the key.
        """
        if key not in self.value:
            self.value[key] = LazyData(
                functools.partial(self.fetch, key),
                self.lazy_time
            )
        return self.value[key].get()