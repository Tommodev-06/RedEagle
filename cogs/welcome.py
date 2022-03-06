import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option
import sqlite3

embed_color = 0xF00C0C

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    welcome_group = SlashCommandGroup("welcome", "Setup the welcome system for your server")

    @welcome_group.command(description="See the usable command for the welcome system.")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Welcome commands",
            description="Available commands for the welcome system.",
            color=embed_color
        )

        total_members = str(ctx.guild.member_count)

        if total_members.endswith == "1":
            count = f"{ctx.guild.member_count}st"
        elif total_members.endswith == "2":
            count = f"{ctx.guild.member_count}nd"
        elif total_members.endswith == "3":
            count = f"{ctx.guild.member_count}rd"
        else:
            count = f"{ctx.guild.member_count}th"

        embed.add_field(name="/welcome channel <channel>", value="Set the welcome channel.")
        embed.add_field(name="/welcome message <message>", value="Set the welcome message.", inline=False)
        embed.add_field(name="/welcome disable", value="Disable the welcome system.", inline=False)
        embed.add_field(name="Variables you can use in the welcome message",
                        value="`{count}` ➜ user count of the server (example: " + f"{count}).\n"
                              "`{members}` ➜ total members of the server (example: " + f"{total_members}).\n"
                              "`{guild}` ➜ for the server name (example: " + f"{ctx.guild.name}).\n"
                              "`{mention}` ➜ for mentioning the user (example: " + f"{ctx.author.mention}).\n"
                              "`{name}` ➜ for the name of the user (example: " + f"{ctx.author.name})."
                        )

        await ctx.respond(embed=embed)

    @welcome_group.command(description="Set the channel for welcome messages.")
    @commands.has_permissions(administrator=True)
    async def channel(
            self,
            ctx,
            channel: Option(discord.TextChannel, "Channel where welcome messages will be sent.")
    ):
        global sql, val

        db = sqlite3.connect("main.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM Welcome WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            sql = "INSERT INTO Welcome(guild_id, channel_id) VALUES(?,?)"
            val = (ctx.guild.id, channel.id)
            await ctx.respond(f"Channel has been set to {channel.mention}.")
        else:
            sql = "UPDATE Welcome SET channel_id = ? WHERE guild_id = ?"
            val = (channel.id, ctx.guild.id)
            await ctx.respond(f"Channel has been set to {channel.mention}.")

        cursor.execute(sql, val)
        db.commit()
        cursor.close()

    @welcome_group.command(description="Set the welcome message.")
    @commands.has_permissions(administrator=True)
    async def message(
            self,
            ctx,
            message: Option(str, "Message to be sent when a user joins.")
    ):
        global sql, val

        db = sqlite3.connect("main.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT message FROM Welcome WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            sql = "INSERT INTO Welcome(guild_id, message) VALUES(?,?)"
            val = (ctx.guild.id, message)
            await ctx.respond(f"Welcome message has been set to `{message}`.")
        elif result is not None:
            sql = "UPDATE welcome SET message = ? WHERE guild_id = ?"
            val = (message, ctx.guild.id)
            await ctx.respond(f"Welcome message has been set to `{message}`.")

        cursor.execute(sql, val)
        db.commit()
        cursor.close()

    @welcome_group.command(description="Disable the welcome system.")
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        db = sqlite3.connect("main.db")
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM Welcome WHERE guild_id = {ctx.guild.id}")

        await ctx.respond("The welcome system has been disabled.")

        db.commit()
        cursor.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect("main.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM Welcome WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()

        if result is None:
            return
        else:
            cursor.execute(f"SELECT message FROM Welcome WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()

            total_members = str(member.guild.member_count)
            guild = member.guild
            mention = member.mention
            name = member.name

            if total_members.endswith == "1":
                count = f"{member.guild.member_count}st"
            elif total_members.endswith == "2":
                count = f"{member.guild.member_count}nd"
            elif total_members.endswith == "3":
                count = f"{member.guild.member_count}rd"
            else:
                count = f"{member.guild.member_count}th"

            embed = discord.Embed(
                description=str(result1[0]).format(count=count, members=total_members, guild=guild, mention=mention, name=name),
                color=embed_color
            )
            embed.set_author(name=f"{member}", icon_url=f"{member.avatar}")
            embed.set_footer(text=f"User ID: {member.id}")

            channel = self.client.get_channel(int(result[0]))

            await channel.send(content=f"{member.mention}", embed=embed)

def setup(client):
    client.add_cog(Welcome(client))
