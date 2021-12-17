import diskord
from diskord.ext import commands
from diskord.utils import remove_markdown
from contextlib import suppress

fail = "<a:fail:866017479696318534>"

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        with suppress(AttributeError):
            if ctx.command.has_error_handler():
                return

        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                f"{fail} I don't have enough permissions to complete this command!\n"
                + "Missing permissions: "
                + f"`{', '.join([e.capitalize().replace('_', ' ') for e in error.missing_permissions])}`\n\n"
                + "Please add these permissions to my role ('RedEagle') in your server settings.",
                components=[self.client.error_btns],
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"{fail} You don't have enough permissions to execute this command!\n"
                + "Missing permissions: "
                + f"`{', '.join([err.capitalize().replace('_', ' ') for err in error.missing_permissions])}`"
            )
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"{fail} Only the owner of the bot can use this command!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"{fail} You haven't provided enough options.\n"
                f"Missing option: `{error.param.name}`."
            )
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(
                f"{fail} You've passed extra options to the command!\n"
                + "Check the help command to know what options to provide."
            )
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send(
                f'{fail} I couldn\'t find the channel "{remove_markdown(error.argument)}".'
            )
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(
                f'{fail} I couldn\'t find the member "{remove_markdown(error.argument)}".'
            )
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(
                f'{fail} I couldn\'t find the user "{remove_markdown(error.argument)}".'
            )
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(
                f'{fail} I couldn\'t find the role "{remove_markdown(error.argument)}". You need to type '
                'the exact name of the role or ping it.'
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"{fail} Whoa, slow down. This command is on cooldown, try again in {round(error.retry_after, 2)} seconds."
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f"{fail} You haven't provided the correct types of options, please check the help command."
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f"{fail} This command can't be used in DMs.")
        elif "Forbidden" in str(error):
            await ctx.send(
                f"{fail} Missing Access error. Possible reasons:\n\n"
                + "1. If I was supposed to perform an action on a *server member*, my roles are too low in the "
                  "hierarchy. I cannot run this command until you move any of my roles higher than the member's "
                  "top-most role.\n "
                + "2. If I was supposed to perform an action on a *channel*, I don't have access to that channel "
                  "because it is private. "
            )
        elif isinstance(error, commands.ExpectedClosingQuoteError):
            await ctx.send(f"{fail} You opened a quote but didn't close it!")
        elif isinstance(
            error, commands.UnexpectedQuoteError
        ) or "Expected space after closing quotation" in str(error):
            await ctx.send(f"{fail} You didn't use quotes correctly.")
        else:
            error_embed = diskord.Embed(
                title="❌ Unhandled error",
                description="Oops, looks like that command returned an unknown error. The error has been "
                            "automatically reported to the developers in our server and will be fixed soon.\n "
                + "Meanwhile, **please do not repeatedly run the same command**.",
                colour=0xFF0000,
            )
            error_embed.add_field(
                name="Join our server to track this error",
                value="If you would like to see more about this error, join [our server](https://discord.gg/tTTuNRwRYJ).",
            )

            embed = diskord.Embed(
                title="Error",
                colour=0xFF0000,
                description=f"Error while invoking command:\n`{ctx.message.content}`",
            ).add_field(name="Error:", value=error)
            embed.set_footer(text=f"User ID: {ctx.author.id}")

            error_channel = self.client.get_channel(919158043776782367)

            await error_channel.send("<@&906675040005812255>", embed=embed)
            await ctx.send(embed=error_embed)

def setup(client):
    client.add_cog(Errors(client))
