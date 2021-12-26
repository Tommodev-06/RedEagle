import diskord
from diskord.ext import commands

prefix = "re!"
embed_color = 0xF00C0C

class HelpDropdown(diskord.ui.Select):
    def __init__(self):

        options = [
            diskord.SelectOption(label="Miscellaneous", description="See all the miscellaneous commands.",
                                 emoji="<:miscellaneous:918838334292389908>"),
            diskord.SelectOption(label="Moderation", description="See al the moderation commands.",
                                 emoji="<:moderation:918837967957663765>"),
            diskord.SelectOption(label="Utilities", description="See all the utilities commands.",
                                 emoji="<:utilities:924694038177792010>")
        ]

        super().__init__(placeholder="Select a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: diskord.Interaction):
        msg = interaction.message

        if self.values[0] == "Miscellaneous":
            embed = diskord.Embed(
                description=f"""

`{prefix}ping` ➜ get the bot's latency.
`{prefix}userinfo [user]` ➜ get information about a user (aliases: `ui`).
`{prefix}serverinfo` ➜ get information about this server (aliases: `si`).
`{prefix}avatar [user]` ➜ get the profile picture of a user (aliases: `av`, `pfp`).
`{prefix}say <text>` ➜ make the bot say something.
`{prefix}embedsay <title> // <description>` ➜ create an embed with your text.
`{prefix}sponsor` ➜ see our partnership with GalaxyNodes.
`{prefix}stats` ➜ get information about RedEagle (aliases: `info`).
`{prefix}changelog` ➜ see what's new in the latest version of RedEagle. 
`{prefix}invite` ➜ get the invite link of RedEagle.
`{prefix}support` ➜ get the support server's link.
`{prefix}vote` ➜ vote RedEagle.

            """,
                color=embed_color
            )

            await msg.edit(content="<:miscellaneous:918838334292389908> **Miscellaneous commands**", embed=embed)

        elif self.values[0] == "Moderation":
            embed = diskord.Embed(
                description=f"""

`{prefix}lock <#channel>` ➜ lock a text channel.
`{prefix}unlock <#channel>` ➜ unlock a text channel.
`{prefix}kick <user> [reason]` ➜ kick a user.
`{prefix}ban <user> [reason]` ➜ ban a user.
`{prefix}mute <user> [reason]` ➜ mute a user.
`{prefix}tempmute <user> <duration> [reason]` ➜ tempmute a user (aliases: `tmute`).
`{prefix}unmute <user>` ➜ unmute a user.
`{prefix}clear <amount>` ➜ clear the specofied amount of messages.
`{prefix}slowmode <seconds>` ➜ set the slowmode to the specified seconds.

            """,
                color=embed_color
            )

            await msg.edit(content="<:moderation:918837967957663765> **Moderation commands**", embed=embed)

        elif self.values[0] == "Utilities":
            embed = diskord.Embed(
                description=f"""

`{prefix}calc <num_1> <operation> <num_2>` ➜ perform a mathematical operation.
`{prefix}raw [message_id]` ➜ get raw text of a message (you can reply to a message).
`{prefix}poll <question> <options>` ➜ create a poll with a maximum of 10 options.
Example: `{prefix}poll "Do you like the bot?" Yes, a lot! // Yeah // No`
`{prefix}addrole <user> <role>` ➜ add a role to a user (aliases: `ar`).
`{prefix}removerole <user> <role>` ➜ remove a role from a user (aliases: `rr`).

            """,
                color=embed_color
            )

            await msg.edit(content="<:utilities:924694038177792010> **Utilities commands**", embed=embed)

class HelpDropdownView(diskord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(HelpDropdown())

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        await ctx.send("Select the category to show commands for.\nIf an argument is in <angle brackets>, "
                       "it's required. If it is in [squared brackets], it's optional.", view=HelpDropdownView())

def setup(client):
    client.add_cog(Help(client))
