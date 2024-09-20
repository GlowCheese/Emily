import time
import sqlite3
import functools


DB_FILE = "words.db"

conn = sqlite3.connect(DB_FILE)
conn.row_factory = sqlite3.Row
conn.autocommit = True


class Word:
    def __init__(
        self,
        word: str,
        source: str,
        meanings: str,
        synonyms: str = None,
        time_added: int = None
    ):
        self.word = word
        self.source = source
        self.meanings = meanings.split(";")
        self.synonyms = synonyms.split(";") if synonyms else []
        self.time_added = time_added if time_added else int(time.time())


def create_table(username: str):
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS "{username}" (
            word         TEXT PRIMARY KEY,
            source       TEXT,
            meanings     TEXT,
            synonyms     TEXT,
            time_added   TEXT
        )
    """)


def make_sure_table_exist(fun):
    @functools.wraps(fun)
    def f(username: str, *args, **kwargs):
        create_table(username)
        return fun(username, *args, **kwargs)
    return f


@make_sure_table_exist
def add_word(username: str, word: Word):
    """
    Add a new word to database.

    Return `false` if the word already exists.
    """

    try:
        conn.execute(f"""
            INSERT INTO "{username}"
            VALUES (?, ?, ?, ?, ?)
        """, (
            word.word, word.source,
            word.meanings[0], None, word.time_added
        ))

        return True

    except sqlite3.IntegrityError as e:
        if e.sqlite_errorname == "SQLITE_CONSTRAINT_PRIMARYKEY":
            return False

        # Unexpected exception
        raise e


@make_sure_table_exist
def remove_word(username: str, word: str):
    """Remove a word from the database."""

    conn.execute(f"""
        DELETE FROM "{username}"
        WHERE word = ?
    """, (word,))


@make_sure_table_exist
def fetch_word(username: str, word: str):
    """Fetch source, meanings and synonyms of a word."""

    cursor = conn.execute(f"""
        SELECT * FROM "{username}"
        WHERE word = ?
    """, (word,))

    res = cursor.fetchone()
    if res is None: return None

    res = dict(res)

    return Word(
        word=word,
        source=res['source'],
        meanings=res['meanings'],
        synonyms=res['synonyms'],
        time_added=res['time_added']
    )


@make_sure_table_exist
def add_meaning(username: str, word: str, meaning: str):
    """Add another meaning for the word"""

    w = fetch_word(username, word)
    if not w: return False

    meanings = w.meanings
    meanings.append(meaning)
    meanings = ";".join(meanings)

    conn.execute(f"""
        UPDATE "{username}"
        SET meanings = ?
        WHERE word = ?
    """, (meanings, word))

    return True


@make_sure_table_exist
def add_synonym(username: str, word: str, synonym: str):
    """Add another synonym for the word"""

    w = fetch_word(username, word)
    if not w: return False

    synonyms = w.synonyms
    synonyms.append(synonym)
    synonyms = ";".join(synonyms)

    conn.execute(f"""
        UPDATE "{username}"
        SET synonyms = ?
        WHERE word = ?
    """, (synonyms, word))

    return True


@make_sure_table_exist
def list_words(username: str, source: str = None):
    if source is None:
        cursor = conn.execute(f"""
            SELECT * FROM "{username}"
            ORDER BY time_added DESC
        """)
    else:
        cursor = conn.execute(f"""
            SELECT * FROM "{username}"
            WHERE source = ?
            ORDER BY time_added DESC
        """, (source,))

    return [Word(
        word=res['word'],
        source=res['source'],
        meanings=res['meanings'],
        synonyms=res['synonyms'],
        time_added=res['time_added']
    ) for res in cursor.fetchall()]