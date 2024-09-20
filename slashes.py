import time
from utils import *
from constants import *
from database import Word

class SlashesCommands(commands.Cog):
    @commands.slash_command()
    async def ping(self, inter: SlashInteraction):
        """Is Emily alive?"""
        start = time.perf_counter()
        await inter.send(':ping_pong: Pong!')
        end = time.perf_counter()
        duration = (end - start) * 1000
        await inter.edit_original_response(
            f'REST API latency: {int(duration)}ms\n'
            f'Gateway API latency: {int(bot.latency * 1000)}ms'
        )

    @commands.slash_command()
    async def kill(self, inter: SlashInteraction):
        """Shutdown Emily :("""
        await inter.response.defer()

        if await bot.is_owner(inter.author):
            desc = f"Boi boi, {inter.author.name}-sama~!"
            embed = disnake.Embed(
                description=desc,
                color=random.choice(COLORS)
            )
            embed.set_image(file=disnake.File(UMARU_SLEEPING))
            await inter.send(embed=embed)
            exit(0)

        else:
            desc = f"Eh? Only my master can do that, silly {inter.author.name}-kun~!"
            embed = disnake.Embed(
                description=desc,
                color=random.choice(COLORS)
            )
            embed.set_image(file=disnake.File(UMARU_HITTING))
            await inter.send(embed=embed)


    @commands.slash_command()
    async def add(self, inter: SlashInteraction):
        pass


    @commands.slash_command()
    async def remove(self, inter: SlashInteraction):
        pass


    @add.sub_command()
    async def word(self, inter: SlashInteraction, word: str, source: str, meaning: str):
        """
        Add a new word to dictionary

        Parameters
        ----------
        word: The given word (e.g. Mouse)
        source: The theme of the word (e.g. Animal)
        meaning: The meaning of the word (e.g. A very long-tailed hamster)
        """

        await inter.response.defer()

        username = inter.author.name
        w = Word(word, source, meaning, None)

        if database.add_word(username, w):
            desc = "✅ Successfully added `1` new word to dictionary!"
            embed = disnake.Embed(description=desc, color=SUCCESS)
            await inter.send(embeds=[embed, make_word_card(username, word)])
        else:
            desc = "⭕ This word has already been added to dictionary!"
            await inter.send(embed=disnake.Embed(description=desc, color=NEUTRAL))


    @remove.sub_command()
    async def word(self, inter: SlashInteraction, word: str):
        """
        Remove a word from the dictionary

        Parameters
        ----------
        word: The word you want to remove
        """

        await inter.response.defer()
        username = inter.author.name

        if database.fetch_word(username, word):
            database.remove_word(username, word)
            desc = f"✅ Removed word `{word}` from dictionary!"
            await inter.send(embed=disnake.Embed(description=desc, color=SUCCESS))
        else:
            desc = "⭕ This word doesn't exist in the dictionary!"
            await inter.send(embed=disnake.Embed(description=desc, color=NEUTRAL))


    @commands.slash_command()
    async def list(self, inter: SlashInteraction, source: str = None):
        """
        List recently added words

        Parameters
        ----------
        source: Filtering words with a theme.
        """

        await inter.response.defer()
        username = inter.author.name

        words = [w.word for w in database.list_words(username, source)]
        if len(words) == 0:
            desc = "⭕ You haven't added any word to dictionary!"
            await inter.send(embed=disnake.Embed(description=desc, color=NEUTRAL))
        else:
            words = words[:15]
            desc = f"✍ List of `{len(words)}` recently added words:"

            embed = disnake.Embed(description=desc, color=random.choice(COLORS))
            field1, field2, field3 = "", "", ""
            for i in range((len(words)+2)//3):
                field1 += f"{i+1}. {words[i]}"
            for i in range((len(words)+2)//3, len(words) - len(words)//3):
                field2 += f"{i+1}. {words[i]}"
            for i in range(len(words) - len(words)//3, len(words)):
                field3 += f"{i+1}. {words[i]}"

            embed.add_field(" ", field1)
            if field2 != "": embed.add_field(" ", field2)
            if field3 != "": embed.add_field(" ", field3)

            await inter.send(embed=embed)


    @add.sub_command()
    async def meaning(self, inter: SlashInteraction, word: str, meaning: str):
        """
        Add another meaning for the word.

        Parameters
        ----------
        word: The given word (e.g. Mouse)
        meaning: The other meaning of the word (e.g. Typically reside in your kitchen :))
        """

        await inter.response.defer()
        username = inter.author.name

        if database.add_meaning(username, word, meaning):
            desc = f"✅ Successfully added `1` new meaning for word `{word}`!"
            embed = disnake.Embed(description=desc, color=SUCCESS)
            await inter.send(embeds=[embed, make_word_card(username, word)])
        else:
            desc = "⭕ This word doesn't exist in the dictionary!"
            await inter.send(embed=disnake.Embed(description=desc, color=NEUTRAL))


    @add.sub_command()
    async def synonym(self, inter: SlashInteraction, word: str, synonym: str):
        """
        Add another synonym for the word.

        Parameters
        ----------
        word: The given word (e.g. overcome)
        synonym: A synonym of the word (e.g. get over)
        """

        await inter.response.defer()
        username = inter.author.name

        if database.add_synonym(username, word, synonym):
            desc = f"✅ Successfully added `1` new synonym for word `{word}`!"
            embed = disnake.Embed(description=desc, color=SUCCESS)
            await inter.send(embeds=[embed, make_word_card(username, word)])
        else:
            desc = "⭕ This word doesn't exist in the dictionary!"
            await inter.send(embed=disnake.Embed(description=desc, color=NEUTRAL))


    @commands.slash_command()
    async def show(self, inter: SlashInteraction, word: str):
        """
        Show synonyms and meanings of a word.

        Parameters
        ----------
        word: The given word (e.g. cheese)
        """

        await inter.response.defer()
        username = inter.author.name

        word_card = make_word_card(username, word)
        if word_card: await inter.send(embed=word_card)
        else:
            desc = "⭕ This word doesn't exist in the dictionary!"
            await inter.send(embed=disnake.Embed(description=desc, color=NEUTRAL))


    @commands.slash_command()
    async def study(self, inter: SlashInteraction, source: str = None):
        """
        Show synonyms and meanings of a word.

        Parameters
        ----------
        word: The given word (e.g. cheese)
        """

        await inter.response.defer()
        username = inter.author.name

        words = [w.word for w in database.list_words(username, source)]
        random.shuffle(words)
        total = len(words)

        await inter.send(embed=make_word_card(username, words[0]))
        if total == 1: return

        next_button = disnake.ui.Button(
            label=f"Next (1/{total})",
            style=disnake.ButtonStyle.green,
            emoji="➡️"
        )
        view = disnake.ui.View()

        current = 1
        async def button_callback(
            new_inter: disnake.MessageInteraction
        ):
            nonlocal current
            await new_inter.response.defer()

            current += 1
            next_button.label = f"Next ({current}/{total})"
            if current == total:
                next_button.disabled = True
                view.clear_items().add_item(next_button)

            await inter.edit_original_response(
                view=view,
                embed=await make_word_card(username, words[current])
            )
        
        async def on_timeout():
            next_button.disabled = True
            view.clear_items().add_item(next_button)
            try:
                await inter.edit_original_response(view=view)
            except disnake.errors.HTTPException:
                pass

        next_button.callback = button_callback
        view.on_timeout = on_timeout
        await inter.edit_original_response(
            view=view.add_item(next_button)
        )


def setup(bot: commands.InteractionBot):
    bot.add_cog(SlashesCommands())