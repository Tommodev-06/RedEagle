import diskord
from diskord.ext import commands
from contextlib import suppress
import os
from asyncio import sleep

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def ownerhelp(self, ctx):
        embed = diskord.Embed(
            title="Owner-only commands",
            color=0xF00C0C
        )
        embed.add_field(name="Send a embed", value="`re!embed <title> // <description>`", inline=False)
        embed.add_field(name="Reload cogs", value="`re![reload|refresh]`", inline=False)
        embed.add_field(name="Check the perms for the Muted role", value="`re!mutecheck`", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def embed(self, ctx, *, args):
        title, desription = args.split("//")

        embed = diskord.Embed(
            title=f"{title}",
            description=f"{desription}",
            color=0xF00C0C
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["refresh"])
    @commands.is_owner()
    async def reload(self, ctx):
        msg = await ctx.send("Reloading cogs...")

        with suppress(commands.ExtensionNotLoaded):
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    self.client.unload_extension(f"cogs.{filename[:-3]}")

            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    self.client.load_extension(f"cogs.{filename[:-3]}")

        await sleep(2)
        await msg.edit(content="Cogs reloaded!")

    @commands.command()
    @commands.is_owner()
    async def mutecheck(self, ctx):
        muted_role = diskord.utils.get(ctx.guild.roles[::-1], name="Muted")

        if not muted_role:
            msg = await ctx.send("The process may take some time. Please wait...")

            new_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(
                    new_role, send_messages=False, speak=False
                )

            await msg.edit("Success!")
        else:
            msg = await ctx.send("The process may take some time. Please wait...")

            for channel in ctx.guild.channels:
                await channel.set_permissions(
                    muted_role, send_messages=False, speak=False, add_reactions=False
                )

            await msg.edit("Success!")

def setup(client):
    client.add_cog(Owner(client))
