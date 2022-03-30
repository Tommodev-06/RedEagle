import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option

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
        await ctx.defer()

        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT channel_id FROM Welcome WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            cursor.execute(
                f"INSERT INTO Welcome(guild_id, channel_id) VALUES(?,?)", (ctx.guild.id, channel.id)
            )
        else:
            cursor.execute(
                "UPDATE Welcome SET channel_id = ? WHERE guild_id = ?", (channel.id, ctx.guild.id)
            )

        self.client.db.commit()

        await ctx.respond(f"Channel has been set to {channel.mention}.")

    @welcome_group.command(description="Set the welcome message.")
    @commands.has_permissions(administrator=True)
    async def message(
            self,
            ctx,
            message: Option(str, "Message to be sent when a user joins.")
    ):
        await ctx.defer()

        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT message FROM Welcome WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            cursor.execute(
                f"INSERT INTO Welcome(guild_id, message) VALUES(?,?)", (str(message), ctx.guild.id)
            )
        else:
            cursor.execute(
                "UPDATE Welcome SET message = ? WHERE guild_id = ?", (str(message), ctx.guild.id)
            )

        self.client.db.commit()

        await ctx.respond(f"Welcome message has been set to `{message}`.")

    @welcome_group.command(description="Disable the welcome system.")
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        await ctx.defer()

        cursor = self.client.db.cursor()
        cursor.execute(f"DELETE FROM Welcome WHERE guild_id = {ctx.guild.id}")

        self.client.db.commit()

        await ctx.respond("The welcome system has been disabled.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT channel_id FROM Welcome WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()

        if result is None:
            return
        else:
            cursor.execute(f"SELECT message FROM Welcome WHERE guild_id = {member.guild.id}")
            message = cursor.fetchone()

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

            channel = self.client.get_channel(int(result[0]))

            await channel.send(
                content=f"""{message[0].format(
                    count=count, members=total_members, guild=guild, mention=mention, name=name
                )}"""
            )

def setup(client):
    client.add_cog(Welcome(client))
