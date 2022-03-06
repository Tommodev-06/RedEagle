import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import requests
import random

fail = "<a:fail:866017479696318534>"

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(description="MoCk TeXt (alternating upper and lower case).")
    async def mock(
            self,
            ctx,
            text: Option(str, "Text to be mocked.")
    ):
        mock_text = "".join(
            [char.upper() if i % 2 else char.lower() for i, char in enumerate(text)]
        )

        await ctx.respond(mock_text)

    @slash_command(description="Reversed text.")
    async def reverse(
            self,
            ctx,
            text: Option(str, "Text to be reversed.")
    ):
        await ctx.respond(text[::-1])

    @slash_command(description="Suggests you something to do if you're bored.")
    async def bored(self, ctx):
        await ctx.defer()

        r = requests.get("https://www.boredapi.com/api/activity?participants=1&price=0")

        if r.status_code != 200:
            await ctx.respond(
                f"{fail} The API has returned an error. Please try again later.", ephemeral=True
            )
            return

        json = r.json()
        await ctx.respond(f'{json["activity"]}.')

    @slash_command(description="Get a random meme from Reddit.")
    async def meme(
            self,
            ctx,
            subreddit: Option(str, "Subreddit of the meme.", required=False, default=None)
    ):
        await ctx.defer()

        if subreddit:
            json = requests.get(
                f"https://meme-api.herokuapp.com/gimme/{subreddit}"
            ).json()
        else:
            json = requests.get(f"https://meme-api.herokuapp.com/gimme").json()

        try:
            if json["code"]:
                await ctx.respond(
                    json["message"]
                )
                return
        except KeyError:
            if not json["nsfw"]:
                title = (
                    json["title"][:253] + "..."
                    if len(json["title"]) > 256
                    else json["title"]
                )
                meme_embed = discord.Embed(
                    title=title,
                    description=f"r/{json['subreddit']}",
                    color=0x76D7C4,
                    url=json["postLink"]
                )
                meme_embed.set_image(url=json["url"])

                await ctx.respond(embed=meme_embed)

        if json["nsfw"]:
            await ctx.respond(f"❗ Warning: NSFW post!\n\n<{json['postLink']}>")

    @slash_command(name="8ball", description="Ask the magic 8-ball a question.")
    async def ball(
            self,
            ctx,
            question: Option(str, "The question to ask to the 8-ball.")
    ):
        responses = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes, definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
        ]

        await ctx.respond(f'The magic ball says... "{random.choice(responses)}"')

    @slash_command(description="Flip a coin.")
    async def flip(self, ctx):
        if random.randint(1, 100) <= 50:
            await ctx.respond("You flipped... **heads**!")
        else:
            await ctx.respond("You flipped... **tails**!")

    @slash_command(description="Roll a dice.")
    async def roll(self, ctx):
        await ctx.respond(f"You rolled a **{random.randint(1, 6)}**!")

def setup(client):
    client.add_cog(Fun(client))
