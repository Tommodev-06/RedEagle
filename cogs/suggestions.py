import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option

embed_color = 0xF00C0C
success = "<a:success:865522277729566741>"
fail = "<a:fail:866017479696318534>"

class Suggestions(commands.Cog):
    def __init__(self, client):
        self.client = client

    suggest_group = SlashCommandGroup("suggest", "Setup the suggestion system for your server")

    @suggest_group.command(description="Set the channel for suggestions.")
    @commands.has_permissions(administrator=True)
    async def channel(
            self,
            ctx,
            channel: Option(discord.TextChannel, "Channel where suggestions will be sent.")
    ):
        await ctx.defer()

        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT channel_id FROM Suggestions WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            cursor.execute(
                f"INSERT INTO Suggestions(guild_id, channel_id) VALUES(?,?)", (ctx.guild.id, channel.id)
            )
        else:
            cursor.execute(
                "UPDATE Suggestions SET channel_id = ? WHERE guild_id = ?", (channel.id, ctx.guild.id)
            )

        self.client.db.commit()

        await ctx.respond(f"Channel has been set to {channel.mention}.")

    @suggest_group.command(description="Disable the suggestion system.")
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        await ctx.defer()

        cursor = self.client.db.cursor()
        cursor.execute(f"DELETE FROM Suggestions WHERE guild_id = {ctx.guild.id}")

        self.client.db.commit()

        await ctx.respond("The suggestion system has been disabled.")

    @suggest_group.command(description="Submit a suggestion for the server.")
    async def send(
            self,
            ctx,
            suggestion: Option(str, "Your suggestion to send.")
    ):
        await ctx.defer(ephemeral=True)

        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT channel_id FROM Suggestions WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            await ctx.respond(
                f"{fail} {ctx.author.mention}, this server has no suggestion channel. Please contact a server "
                "admin to solve this issue.", ephemeral=True
            )
        else:
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

                channel = self.client.get_channel(int(result[0]))

                message = await channel.send(embed=embed)

                await message.add_reaction("✅")
                await message.add_reaction("❌")

                await ctx.respond(f"Suggestion successfully submitted in {channel.mention}!", ephemeral=True)

def setup(client):
    client.add_cog(Suggestions(client))
