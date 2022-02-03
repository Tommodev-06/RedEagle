import diskord
from diskord.ext import commands
from diskord.utils import remove_markdown
from contextlib import suppress

fail = "<a:fail:866017479696318534>"

class ServerButton(diskord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(diskord.ui.Button(label="Official Server", url="https://discord.gg/tTTuNRwRYJ"))

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        with suppress(AttributeError):
            if ctx.command.has_error_handler():
                return

        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply(
                f"{fail} I don't have enough permissions to complete this command!\n"
                "Missing permissions: "
                f"`{', '.join([e.capitalize().replace('_', ' ') for e in error.missing_permissions])}`\n\n"
                "Please add these permissions to my role ('RedEagle') in your server settings."
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(
                f"{fail} You don't have enough permissions to execute this command!\n"
                + "Missing permissions: "
                + f"`{', '.join([err.capitalize().replace('_', ' ') for err in error.missing_permissions])}`"
            )
        elif isinstance(error, commands.NotOwner):
            await ctx.reply(f"{fail} Only the owner of the bot can use this command!")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = diskord.Embed(
                title=f"{str(ctx.command.qualified_name).capitalize()} command",
                description=f"Missing required argument. Usage of the {ctx.command.qualified_name} command:\n"
                            f"```{ctx.prefix}{ctx.command.name} {ctx.command.signature}```",
                color=0xF00C0C
            )
            embed.add_field(name="Description", value=ctx.command.help, inline=False)
            embed.set_footer(text="< > Required | [ ] Optional")
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.TooManyArguments):
            await ctx.reply(
                f"{fail} You've passed extra options to the command!\n"
                "Check the help command to know what options to provide."
            )
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.reply(
                f'{fail} I couldn\'t find the channel "{remove_markdown(error.argument)}".'
            )
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(
                f'{fail} I couldn\'t find the member "{remove_markdown(error.argument)}".'
            )
        elif isinstance(error, commands.UserNotFound):
            await ctx.reply(
                f'{fail} I couldn\'t find the user "{remove_markdown(error.argument)}".'
            )
        elif isinstance(error, commands.RoleNotFound):
            await ctx.reply(
                f'{fail} I couldn\'t find the role "{remove_markdown(error.argument)}". You need to type '
                "the exact name of the role or ping it."
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(
                f"{fail} This command is on cooldown, try again in {round(error.retry_after, 2)} seconds."
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(
                f"{fail} You haven't provided the correct types of options, please check the help command."
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(f"{fail} This command can't be used in DMs.")
        elif "Forbidden" in str(error):
            await ctx.reply(
                f"{fail} Missing Access error. Possible reasons:\n\n"
                + "1. If I was supposed to perform an action on a *server member*, my roles are too low in the "
                  "hierarchy. I cannot run this command until you move any of my roles higher than the member's "
                  "top-most role.\n"
                + "2. If I was supposed to perform an action on a *channel*, I don't have access to that channel "
                  "because it is private."
            )
        elif isinstance(error, commands.ExpectedClosingQuoteError):
            await ctx.reply(f"{fail} You opened a quote but didn't close it!")
        elif isinstance(
                error, commands.UnexpectedQuoteError
        ) or "Expected space after closing quotation" in str(error):
            await ctx.reply(f"{fail} You didn't use quotes correctly.")
        else:
            error_channel = await self.client.fetch_channel(919158043776782367)

            embed = diskord.Embed(
                description=f"Error while invoking command `{ctx.message.content}`",
                colour=0xFF0000
            )
            embed.add_field(name="Error", value=f"```{error}```")
            embed.set_footer(text=f"User ID: {ctx.author.id}")

            await error_channel.send("<@&906675040005812255>", embed=embed)
            await ctx.reply(
                "That command returned an error. It has been reported to the developer.\nMeanwhile, "
                "don't run the same command! Join our server to track this error.", view=ServerButton()
            )

def setup(client):
    client.add_cog(Errors(client))
