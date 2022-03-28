import discord
import os
import dotenv
from itertools import cycle
from asyncio import sleep
from cogs.tickets import NewTicket
import sqlite3

client = discord.Bot(intents=discord.Intents(guilds=True, messages=True))
client.persistent_views_added = False
client.db = sqlite3.connect("main.db")

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
        client.load_extension(f"cogs.{file[:-3]}")

dotenv.load_dotenv()

client.run(os.getenv("TOKEN"))
