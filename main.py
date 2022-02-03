import diskord
from diskord.ext import commands
import os
import dotenv
from itertools import cycle
from asyncio import sleep

client = commands.Bot(
    command_prefix=commands.when_mentioned_or(lambda bot,msg:msg.content.lower()=="re!"),
    case_insensitive=True,
    intents=diskord.Intents.all(),
    help_command=None
)

async def change_status():
    statuses = cycle(
        [
            "re!help",
            "re!invite",
            "re!vote"
        ]
    )

    while not client.is_closed():
        await client.change_presence(activity=diskord.Game(name=next(statuses)))
        await sleep(5)

@client.event
async def on_ready():
    print(f"{client.user} is online | {len(client.guilds)} servers")
    client.loop.create_task(change_status())

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")

dotenv.load_dotenv()

client.run(os.getenv("TOKEN"))
