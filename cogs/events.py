import diskord
from diskord.ext import commands
import datetime

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return

        if (
                message.content == f"<@!{self.client.user.id}>"
                or message.content == f"<@{self.client.user.id}>"
        ):
            await message.channel.send(
                "My prefix is `re!`. Type `re!help` to see the available commands."
            )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = await self.client.fetch_channel(869313065441701919)

        embed = diskord.Embed(
            title="Joined a server!",
            description=f"I joined **{guild.name}** right now and I'm in **{len(self.client.guilds)} servers** now!",
            color=0xF00C0C
        )
        embed.timestamp = datetime.datetime.utcnow()

        await channel.send("Hey <@825292137338765333>, I joined a new server!", embed=embed)

        muted_role = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(
                muted_role, send_messages=False, speak=False
            )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        muted_role = diskord.utils.get(channel.guild.roles[::-1], name="Muted")

        await channel.set_permissions(
            muted_role, send_messages=False, speak=False
        )

def setup(client):
    client.add_cog(Events(client))
