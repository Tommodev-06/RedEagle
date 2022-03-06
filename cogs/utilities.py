import discord
from discord.ext import commands
from discord.commands import slash_command, Option

embed_color = 0xF00C0C
success = "<a:success:865522277729566741>"
fail = "<a:fail:866017479696318534>"

class Utilities(commands.Cog, description="Utilities commands"):
    def __init__(self, client):
        self.client = client

    @slash_command(description="Perform a mathematical operation.")
    async def calculate(
            self,
            ctx,
            num_1: Option(float, "First number of the operation."),
            operation: Option(
                str,
                "Mathematical operation",
                choices=[
                    "Addition (+)",
                    "Subtraction (-)",
                    "Multiplication (×)",
                    "Division (÷)"
                ]
            ),
            num_2: Option(float, "Second number of the operation.")
    ):
        o = operation

        if o == "Addition (+)":
            return await ctx.respond(str(num_1 + num_2))
        if o == "Subtraction (-)":
            return await ctx.respond(str(num_1 - num_2))
        if o == "Multiplication (×)":
            return await ctx.respond(str(num_1 * num_2))
        if o == "Division (÷)":
            try:
                return await ctx.respond(str(num_1 / num_2))
            except ZeroDivisionError:
                await ctx.respond(f"How the fuck do you pretend to divide {num_1} by zero?!", ephemeral=True)

    @slash_command(description="Get the raw text of a message.")
    async def raw(
            self,
            ctx,
            message_id: Option(str, "The ID of the message.")
    ):
        try:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if message is None:
                await ctx.respond(
                    "This message could not be fetched, or it might not have text content.", ephemeral=True
                )
                return
        except (discord.NotFound, AttributeError):
            try:
                message = await ctx.fetch_message(message_id)
            except:
                return await ctx.respond(
                    "The message you provided was not found in this channel!", ephemeral=True
                )

        if not message.content:
            await ctx.respond("This message has no content.", ephemeral=True)
            return

        await ctx.respond(f"```{message.content}```")

def setup(client):
    client.add_cog(Utilities(client))
