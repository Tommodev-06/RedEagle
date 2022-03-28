import discord
from discord.commands import permissions
import os
import dotenv
from itertools import cycle
from asyncio import sleep
from cogs.tickets import NewTicket
import sys

client = discord.Bot(intents=discord.Intents(guilds=True, members=True, messages=True))
client.persistent_views_added = False

async def change_status():
    statuses = cycle(
        [
            "/help",
            "/invite",
            "/vote"
        ]
    )

    while not client.is_closed():
        await client.change_presence(activity=discord.Game(name=next(statuses)))
        await sleep(5)

@client.event
async def on_ready():
    print(f"{client.user} is online")
    client.loop.create_task(change_status())

    if not client.persistent_views_added:
        client.add_view(NewTicket(client))
        client.persistent_views_added = True

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        try:
            client.load_extension(f"cogs.{file[:-3]}")
        except Exception as e:
            print("Error reloading "+file[:-3]+":", e, file=sys.stderr)
@client.slash_command(description="Reload the cogs.", guild_ids=[846662078545657867], default_permission=False)
@permissions.is_owner()
async def reload(ctx):
    await ctx.defer(ephemeral=True)

    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            try:
                client.reload_extension(f"cogs.{file[:-3]}")
            except Exception as e:
                print("Error reloading "+file[:-3]+":", e, file=sys.stderr)
    await ctx.respond("Cogs reloaded.")

dotenv.load_dotenv()

client.run(os.getenv("TOKEN"))
