import diskord
from diskord.ext import commands
import os
import datetime
from dotenv import load_dotenv
from itertools import cycle
from asyncio import sleep

client = commands.Bot(
    command_prefix=["re!", "Re!", "<@856643485340139580> ", "<@!856643485340139580> "],
    case_insensitive=True,
    intents=diskord.Intents.all()
)
client.remove_command("help")

async def change_status():
    statuses = cycle(
        [
            "re!help",
            "re!vote"
        ]
    )

    while not client.is_closed():
        await client.change_presence(activity=diskord.Game(name=next(statuses)))
        await sleep(10)

@client.event
async def on_ready():
    print(f"{client.user} is online | {len(client.guilds)} servers")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if (
            message.content == f"<@!{client.user.id}>"
            or message.content == f"<@{client.user.id}>"
    ):
        await message.channel.send(
            "My prefix is `re!`. Type `re!help` to see the available commands."
        )

    await client.process_commands(message)

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(869313065441701919)

    embed = diskord.Embed(
        title="Joined a server!",
        description=f"I joined **{guild.name}** right now and I'm in **{len(client.guilds)} servers** now!",
        color=0xF00C0C
    )
    embed.timestamp = datetime.datetime.utcnow()

    await channel.send("Hey <@825292137338765333>, I joined a new server!", embed=embed)

    muted_role = await guild.create_role(name="Muted")

    for channel in guild.channels:
        await channel.set_permissions(
            muted_role, send_messages=False, speak=False
        )

@client.event
async def on_guild_channel_create(channel):
    guild = channel.guild
    muted_role = diskord.utils.get(guild.roles[::-1], name="Muted")

    if muted_role:
        await channel.set_permissions(muted_role, send_messages=False, speak=False)

load_dotenv()

client.run(os.getenv("TOKEN"))
