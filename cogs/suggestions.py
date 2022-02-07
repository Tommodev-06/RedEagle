import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option
import sqlite3

embed_color = 0xF00C0C
success = "<a:success:865522277729566741>"
fail = "<a:fail:866017479696318534>"

class Suggestions(commands.Cog):
    def __init__(self, client):
        self.client = client

    suggest_group = SlashCommandGroup("suggest", "Setup the suggestion system for your server")

    @suggest_group.command(description="Set the channel for suggestions.")
    async def channel(
            self,
            ctx,
            channel: Option(discord.TextChannel, "Channel where suggestions will be sent.")
    ):
        global sql, val

        db = sqlite3.connect("main.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM Suggestions WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            sql = "INSERT INTO Suggestions(guild_id, channel_id) VALUES(?,?)"
            val = (ctx.guild.id, channel.id)
            await ctx.respond(f"Channel has been set to {channel.mention}.")
        elif result is not None:
            sql = "UPDATE Suggestions SET channel_id = ? WHERE guild_id = ?"
            val = (channel.id, ctx.guild.id)
            await ctx.respond(f"Channel has been set to {channel.mention}.")

        cursor.execute(sql, val)
        db.commit()

    @suggest_group.command(description="Submit a suggestion for the server.")
    async def send(
            self,
            ctx,
            suggestion: Option(str, "Your suggestion to send.")
    ):
        await ctx.defer(ephemeral=True)

        db = sqlite3.connect("main.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM Suggestions WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            await ctx.respond(
                f"{fail} {ctx.author.mention}, this server has no a suggestion channel. Please contact a server "
                "admin to solve this issue.", ephemeral=True
            )
        else:
            channel = self.client.get_channel(int(result[0]))

            if len(suggestion) < 10:
                await ctx.respond("Your suggestion is too short. It must be at least 10 characters long.",
                                  ephemeral=True)
                return
            else:
                embed = discord.Embed(
                    title="Suggestion",
                    description=f"{suggestion}",
                    color=embed_color
                )
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")
                embed.set_thumbnail(url=f"{ctx.author.display_avatar}")
                embed.set_footer(text=f"User ID: {ctx.author.id}")

                message = await channel.send(embed=embed)

                await message.add_reaction("✅")
                await message.add_reaction("❌")

                await ctx.respond(f"Suggestion successfully submitted in {channel.mention}!", ephemeral=True)

def setup(client):
    client.add_cog(Suggestions(client))
