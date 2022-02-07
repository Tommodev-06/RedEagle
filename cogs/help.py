import discord
from discord.ext import commands
from discord.commands import slash_command, Option

embed_color = 0xF00C0C

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(description="See the available commands of RedEagle.")
    async def help(
            self,
            ctx,
            category: Option(str, "Category to show available commands.",
                             choices=[
                                 "Fun", "Miscellaneous", "Moderation", "Suggestion system", "Ticket system",
                                 "Utilities", "Welcome system"
                             ])
    ):
        global embed

        if category == "Fun":
            embed = discord.Embed(
                title="Fun commands",
                description="""
`/mock <text>` ➜ mOcK tExT (alternating upper and lower case).
`/reverse <text>` ➜ unlock a text channel.
`/bored` ➜ suggests you something to do if you're bored.
`/meme [subreddit]` ➜ get a random meme from Reddit.
`/8ball <question>` ➜ ask the magic 8-ball a question.
`/flip` ➜ flip a coin.
`/roll` ➜ roll a dice.             
                """,
                color=embed_color
            )
        elif category == "Miscellaneous":
            embed = discord.Embed(
                title="Miscellaneous commands",
                description="""
`/ping` ➜ see the bot's latency.
`/userinfo [user]` ➜ get information about a user.
`/serverinfo` ➜ get information about this server.
`/avatar [user]` ➜ get the profile picture of a user.
`/say <text>` ➜ make the bot say something.
`/embedsay <title> <description>` ➜ create an embed with your text.
`/sponsor` ➜ see our partnership with GalaxyNodes.
`/stats` ➜ get information about RedEagle.
`/advice <suggestion>` ➜ submit a suggestion for the bot.
`/changelog` ➜ see what's new in the latest version of RedEagle.
`/invite` ➜ get the invite link of RedEagle.
`/support` ➜ get the support server's link.
`/vote` ➜ vote RedEagle.             
                """,
                color=embed_color
            )
        elif category == "Moderation":
            embed = discord.Embed(
                title="Moderation commands",
                description="""
`/lock [channel] [reason]` ➜ lock a text channel.
`/unlock [channel] [reason]` ➜ unlock a text channel.
`/kick <user> [reason]` ➜ kick a user.
`/ban <user> [reason]` ➜ ban a user.
`/mute <user> [reason]` ➜ mute a user.
`/tempmute <user> <duration> [reason]` ➜ temporarily mute a user.
`/unmute <user>` ➜ unmute a user.
`/clear <amount>` ➜ clear the specified amount of messages.
`/slowmode <seconds>` ➜ set the slowmode to the specified seconds.            
                """,
                color=embed_color
            )
        elif category == "Suggestion system":
            embed = discord.Embed(
                title="Suggestion system",
                description="""
`/suggest channel <channel>` ➜ set the channel for suggestions.
`/suggest send <channel>` ➜ submit a suggestion for the server.            
                """,
                color=embed_color
            )
        elif category == "Ticket system":
            embed = discord.Embed(
                title="Ticket system",
                description="""
`/ticket help` ➜ see the usable commands for the ticket system.
`/ticket role <role>` ➜ set the role that will have access to tickets.
`/ticket logs <channel>` ➜ set the logs channel for ticket events.
`/ticket category <category>` ➜ set the category where tickets will be created.
`/ticket panel <channel> <title> <description>` ➜ send in a channel the panel for opening tickets.         
                """,
                color=embed_color
            )
        elif category == "Utilities":
            embed = discord.Embed(
                title="Utilities commands",
                description="""
`/calculate <num_1> <operation> <num_2>` ➜ perform a mathematical operation.
`/raw <message_id>` ➜ get the raw text of a message.       
                """,
                color=embed_color
            )
        elif category == "Welcome system":
            embed = discord.Embed(
                title="Welcome system",
                description="""
`/welcome help` ➜ see the usable commands for the welcome system.
`/welcome channel <channel>` ➜ set the channel for welcome messages.
`/welcome message <message>` ➜ set the welcome message.
`/welcome disable` ➜ disable the welcome system.  
                """,
                color=embed_color
            )

        embed.set_footer(text="< > Required | [ ] Optional")

        await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(Help(client))
