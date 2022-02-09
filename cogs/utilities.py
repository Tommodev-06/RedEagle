import diskord
from diskord.ext import commands

embed_color = 0xF00C0C
success = "<a:success:865522277729566741>"
fail = "<a:fail:866017479696318534>"

class Utilities(commands.Cog, description="Utilities commands"):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Perform a mathematical operation.")
    async def calc(self, ctx, num_1: float, operation: str, num_2: float):
        o = operation.lower()

        if o == "+" or o == "plus":
            return await ctx.send(str(num_1 + num_2))
        if o == "-" or o == "minus":
            return await ctx.send(str(num_1 - num_2))
        if o == "*" or o == "times" or o == "x":
            return await ctx.send(str(num_1 * num_2))
        if o == "/" or o == "by":
            try:
                return await ctx.send(str(num_1 / num_2))
            except ZeroDivisionError:
                await ctx.send(f"How the fuck do you pretend to divide {num_1} by zero?!")
        else:
            await ctx.send(
                "Invalid operation. Use one of these for the operation: `+`, `plus`, `-`, `minus`, `*`, `x`, `/`."
            )

    @commands.command(help="Get raw text of a message")
    async def raw(self, ctx, message_id: str = None):
        message = None

        try:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if message is None:
                return await ctx.send(
                    "This message could not be fetched, or it might not have text content."
                )
        except (diskord.NotFound, AttributeError):
            if not message_id:
                await ctx.send(
                    "You need to either reply to a message with this command or provide a message ID!"
                )
                return
            else:
                try:
                    message = await ctx.fetch_message(message_id)
                except:
                    return await ctx.send(
                        "The message you provided was not found in this channel!"
                    )

        if not message.content:
            await ctx.send("This message has no content.")
            return

        await ctx.send(f"```{message.content}```",allowed_mentions=diskord.AllowedMentions.none())

    @commands.command(help="Create a poll")
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, question: str, *, options: str):
        numbers = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟")
        option_list = options.split("//")

        await ctx.message.delete()

        if len(option_list) > 10:
            await ctx.send(f"{fail} You can't have more than 10 choices!")
            return
        elif len(option_list) < 2:
            await ctx.send(f"{fail} You need to provide multiple options!")
            return

        emb = diskord.Embed(
            title=str(question.capitalize()),
            description="\n\n".join(
                [
                    f"{numbers[i]} {option_list[i]}"
                    for i in range(len(option_list))
                ]
            ),
            color=embed_color
        )
        emb.set_footer(text=f"Poll created by {ctx.message.author}")

        poll_msg = await ctx.send(embed=emb)

        for emoji in numbers[: len(option_list)]:
            await poll_msg.add_reaction(emoji)

    @commands.command(help="Add a role to a user", aliases=["ar"], pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, user: commands.MemberConverter = None, *, role: commands.RoleConverter):
        if role in user.roles:
            await ctx.send(f"{fail} This user has this role yet!")
            return

        try:
            await user.add_roles(role)
            await ctx.send(f"{success} Successfully added to {user} the role `{role.name}`.")
        except diskord.Forbidden:
            pass
            await ctx.send(
                f"{fail} An error occured! You can fix it with moving my role over the role you want to add."
            )

    @commands.command(help="Remove a role from a user", aliases=["rr"], pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, user: commands.MemberConverter = None, *, role: commands.RoleConverter):
        if not role in user.roles:
            await ctx.send(f"{fail} This user doesn't have this role!")
            return

        try:
            await user.remove_roles(role)
            await ctx.send(
                f"{success} Successfully removed to {user} the role `{role.name}`."
            )
        except diskord.Forbidden:
            pass
            await ctx.send(
                f"{fail} An error occured! You can fix it with moving my role over the role you want to remove."
            )

def setup(client):
    client.add_cog(Utilities(client))
