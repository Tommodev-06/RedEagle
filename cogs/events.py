import discord
from discord.ext import commands
import datetime
import random

class InviteButton(discord.ui.View):
    def __init__(self):
        super().__init__()

        invite_url = "https://discord.com/api/oauth2/authorize?client_id=856643485340139580&permissions=8&scope=bot%20applications.commands"

        self.add_item(discord.ui.Button(label="Invite", url=invite_url))

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id or message.author.bot:
            return

        cursor = self.client.db.cursor()

        # AFK system

        cursor.execute(
            "SELECT reason FROM AFK WHERE user_id = ? and guild_id = ?", (message.author.id, message.guild.id)
        )
        data = cursor.fetchone()

        if data:
            await message.channel.send(
                f"Welcome back {message.author.mention}! I removed your AFK status.", delete_after=10
            )
            cursor.execute(
                "DELETE FROM AFK WHERE user_id = ? AND guild_id = ?", (message.author.id, message.guild.id)
            )
        if message.mentions:
            for mention in message.mentions:
                cursor.execute(
                    "SELECT reason FROM AFK WHERE user_id = ? AND guild_id = ?", (mention.id, message.guild.id)
                )
                user_afk = cursor.fetchone()

                if user_afk and mention.id != message.author.id:
                    await message.channel.send(
                        f"**{mention}** is AFK. Reason: {user_afk[0]}.", delete_after=10
                    )

        self.client.db.commit()

        # Utilities

        if message.content == f"<@!{self.client.user.id}>" or message.content == f"<@{self.client.user.id}>":
            await message.reply(
                "Hello, this is RedEagle! Run `/help` to see available commands.\nIf you don't see RedEagle in the "
                "list of slash commands, re-invite it with the button below!", view=InviteButton()
            )
        elif "re!" in message.content or "Re!" in message.content:
            await message.reply(
                f"Hey **{message.author.name}**, from now I use slash commands! Run `/help` to see available commands.\n"
                "If you don't see RedEagle in the list of slash commands, re-invite it with the button below!",
                view=InviteButton()
            )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = await self.client.fetch_channel(869313065441701919)

        embed = discord.Embed(
            title="Joined a server!",
            description=f"I joined **{guild.name}** right now and I'm in **{len(self.client.guilds)} servers** now!",
            color=0xF00C0C
        )
        embed.timestamp = datetime.datetime.now()

        await channel.send("Hey <@825292137338765333>, I joined a new server!", embed=embed)

        muted_role = discord.utils.get(guild.roles, name="Muted")

        if muted_role:
            return
        else:
            muted_role = await guild.create_role(name="Muted")

            for channel in guild.text_channels:
                overwrite = channel.overwrites_for(muted_role)
                overwrite.send_messages = False

                await channel.set_permissions(muted_role, overwrite=overwrite)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        muted_role = discord.utils.get(channel.guild.roles, name="Muted")

        overwrite = channel.overwrites_for(muted_role)
        overwrite.send_messages = False

        await channel.set_permissions(muted_role, overwrite=overwrite)

def setup(client):
    client.add_cog(Events(client))
