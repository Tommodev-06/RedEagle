import diskord
from diskord.ext import commands

embed_color = 0xF00C0C

class HelpDropdown(diskord.ui.Select):
    def __init__(self, ctx):

        options = [
            diskord.SelectOption(label="Miscellaneous", description="See all the miscellaneous commands.",
                                 emoji="<:miscellaneous:918838334292389908>"),
            diskord.SelectOption(label="Moderation", description="See al the moderation commands.",
                                 emoji="<:moderation:918837967957663765>"),
            diskord.SelectOption(label="Suggestions", description="See all the suggestion commands.",
                                 emoji="<:suggestion:930119666045706260>"),
            diskord.SelectOption(label="Utilities", description="See all the utilities commands.",
                                 emoji="<:utilities:924694038177792010>")
        ]

        super().__init__(placeholder="Select a category...", min_values=1, max_values=1, options=options)
        self.ctx = ctx
        self.prefix = ctx.prefix

    async def callback(self, interaction: diskord.Interaction):
        msg = interaction.message

        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "This is not your help command.", ephemeral=True
            )
            return

        if self.values[0] == "Miscellaneous":
            embed = diskord.Embed(
                description=f"""

`{self.prefix}ping` ➜ get the bot's latency.
`{self.prefix}userinfo [user]` ➜ get information about a user (aliases: `ui`).
`{self.prefix}serverinfo` ➜ get information about this server (aliases: `si`).
`{self.prefix}avatar [user]` ➜ get the profile picture of a user (aliases: `av`, `pfp`).
`{self.prefix}say <text>` ➜ make the bot say something.
`{self.prefix}embedsay <title> // <description>` ➜ create an embed with your text.
`{self.prefix}sponsor` ➜ see our partnership with GalaxyNodes.
`{self.prefix}stats` ➜ get information about RedEagle (aliases: `info`).
`{self.prefix}submit <suggestion>` ➜ submit a suggestion for the bot.
`{self.prefix}changelog` ➜ see what's new in the latest version of RedEagle. 
`{self.prefix}invite` ➜ get the invite link of RedEagle.
`{self.prefix}support` ➜ get the support server's link.
`{self.prefix}vote` ➜ vote RedEagle.

            """,
                color=embed_color
            )

            await msg.edit(content="<:miscellaneous:918838334292389908> **Miscellaneous commands**", embed=embed)

        elif self.values[0] == "Moderation":
            embed = diskord.Embed(
                description=f"""

`{self.prefix}lock <#channel>` ➜ lock a text channel.
`{self.prefix}unlock <#channel>` ➜ unlock a text channel.
`{self.prefix}kick <user> [reason]` ➜ kick a user.
`{self.prefix}ban <user> [reason]` ➜ ban a user.
`{self.prefix}mute <user> [reason]` ➜ mute a user.
`{self.prefix}tempmute <user> <duration> [reason]` ➜ tempmute a user (aliases: `tmute`).
`{self.prefix}unmute <user>` ➜ unmute a user.
`{self.prefix}clear <amount>` ➜ clear the specified amount of messages.
`{self.prefix}slowmode <seconds>` ➜ set the slowmode to the specified seconds.

            """,
                color=embed_color
            )

            await msg.edit(content="<:moderation:918837967957663765> **Moderation commands**", embed=embed)

        elif self.values[0] == "Suggestions":
            embed = diskord.Embed(
                description=f"""

`{self.prefix}suggest channel <#channel>` ➜ set the channel for suggestions.
`{self.prefix}suggest send <suggestion>` ➜ submit a suggestion for the server.

                """,
                color=embed_color
            )

            await msg.edit(content="<:suggestion:930119666045706260> **Suggestion commands**", embed=embed)

        elif self.values[0] == "Utilities":
            embed = diskord.Embed(
                description=f"""

`{self.prefix}calc <num_1> <operation> <num_2>` ➜ perform a mathematical operation.
`{self.prefix}raw [message_id]` ➜ get raw text of a message (you can reply to a message).
`{self.prefix}poll <question> <options>` ➜ create a poll with a maximum of 10 options.
Example: `{self.prefix}poll "Do you like the bot?" Yes, a lot! // Yeah // No`
`{self.prefix}addrole <user> <role>` ➜ add a role to a user (aliases: `ar`).
`{self.prefix}removerole <user> <role>` ➜ remove a role from a user (aliases: `rr`).

            """,
                color=embed_color
            )

            await msg.edit(content="<:utilities:924694038177792010> **Utilities commands**", embed=embed)

class HelpDropdownView(diskord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

        self.add_item(HelpDropdown(ctx))

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        await ctx.send(
            "Select the category to show commands for.\nIf an argument is in <angle brackets>, "
            "it's required. If it is in [squared brackets], it's optional.", view=HelpDropdownView(ctx)
        )

def setup(client):
    client.add_cog(Help(client))
