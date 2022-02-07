import discord
from discord.ext import commands
from contextlib import suppress
import traceback

fail = "<:mod_fail:908415224657375293>"

class Server(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(discord.ui.Button(label="Official Server", url="https://discord.gg/tTTuNRwRYJ", emoji="🔗"))

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        with suppress(AttributeError):
            if ctx.command.has_error_handler():
                return

        traceback.print_exception(type(error), error, error.__traceback__)

        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(
                f"{fail} You don't have the permission to use this command.\n"
                "Missing permission: "
                f"`{', '.join([err.capitalize().replace('_', ' ') for err in error.missing_permissions])}`.",
                ephemeral=True
            )
        elif isinstance(error, commands.NotOwner):
            await ctx.respond(f"{fail} Only the owner of the bot can use this command.", ephemeral=True)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(
                f"{fail} This command is on cooldown, try again in {round(error.retry_after, 2)} "
                "seconds.",
                ephemeral=True
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.respond(f"{fail} This command can't be used in DMs.", ephemeral=True)
        elif "Forbidden" in str(error):
            await ctx.respond(
                f"{fail} Missing Access error. Possible reasons:\n\n"
                "1. If I was supposed to perform an action on a *server member*, my roles are too low in the "
                "hierarchy. Please move my role higher.\n"
                "2. If I was supposed to perform an action on a *channel*, I don't have access to that channel.",
                ephemeral=True
            )

def setup(client):
    client.add_cog(Errors(client))
