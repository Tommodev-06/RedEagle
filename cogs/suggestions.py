import diskord
from diskord.ext import commands
import sqlite3

embed_color = 0xF00C0C
success = "<a:success:865522277729566741>"
fail = "<a:fail:866017479696318534>"

class Suggestions(commands.Cog, description="Suggestion commands"):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def suggest(self, ctx):
        pass

    @suggest.command(help="Available commands for the suggestion system")
    async def help(self, ctx):
        embed = diskord.Embed(
            title="Suggestion commands",
            color=embed_color
        )
        embed.add_field(name="re!suggest channel <#channel>", value="Set the channel for suggestions.",
                        inline=False)
        embed.add_field(name="re!suggest send <suggestion>", value="Submit a suggestion for the server.")

        await ctx.send(embed=embed)

    @suggest.command(help="Set the channel for suggestions")
    async def channel(self, ctx, channel: diskord.TextChannel):
        global sql, val

        db = sqlite3.connect("main.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM Suggestions WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            sql = "INSERT INTO Suggestions(guild_id, channel_id) VALUES(?,?)"
            val = (ctx.guild.id, channel.id)
            await ctx.send(f"Channel has been set to {channel.mention}.")
        elif result is not None:
            sql = "UPDATE Suggestions SET channel_id = ? WHERE guild_id = ?"
            val = (channel.id, ctx.guild.id)
            await ctx.send(f"Channel has been set to {channel.mention}.")

        cursor.execute(sql, val)
        db.commit()

    @suggest.command(help="Submit a suggestion for the server")
    async def send(self, ctx, *, suggestion: str):
        db = sqlite3.connect("main.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM Suggestions WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            await ctx.message.delete()
            await ctx.send(
                f"{fail} {ctx.author.mention}, this server has no a suggestion channel. Please contact a server "
                "admin to solve this issue.",
                delete_after=5)
        else:
            channel = self.client.get_channel(int(result[0]))

            if len(suggestion) < 10:
                await ctx.reply("Your suggestion is too short. It must be at least 10 characters long.")
                return
            else:
                await ctx.message.delete()

                embed = diskord.Embed(
                    description=f"{suggestion}",
                    color=embed_color
                )
                embed.set_author(name=f"Suggestion from {ctx.author}", icon_url=f"{ctx.author.avatar}")
                embed.set_thumbnail(url=f"{ctx.author.avatar}")
                embed.set_footer(text=f"User ID: {ctx.author.id}")

                message = await channel.send(embed=embed)

                await message.add_reaction("✅")
                await message.add_reaction("❌")

                await ctx.reply(f"Suggestion successfully submitted in {channel.mention}!", mention_author=False)

def setup(client):
    client.add_cog(Suggestions(client))
