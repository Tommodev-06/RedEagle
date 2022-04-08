from discord.ext import commands
from discord.commands import SlashCommandGroup, Option

class AFK(commands.Cog):
    def __init__(self, client):
        self.client = client

    afk_group = SlashCommandGroup("afk", "AFK system.")

    @afk_group.command(description="Set your AFK status.")
    async def set(self, ctx, reason: Option(str, "Reason you are AFK.", required=False)):
        if reason is None:
            reason = "not provided"

        cursor = self.client.db.cursor()
        cursor.execute("SELECT reason FROM AFK WHERE user_id = ? and guild_id = ?", (ctx.author.id, ctx.guild.id))
        data = cursor.fetchone()

        if data:
            if data[0] == reason:
                await ctx.respond("You are already AFK.", ephemeral=True)
                return
            else:
                cursor.execute(
                    "UPDATE AFK SET reason = ? WHERE user_id = ? AND guild_id = ?",
                    (reason, ctx.author.id, ctx.guild.id)
                )
                await ctx.respond("AFK status updated.", ephemeral=True)
        else:
            cursor.execute(
                "INSERT INTO AFK(guild_id, user_id, reason) VALUES (?,?,?)", (ctx.guild.id, ctx.author.id, reason)
            )
            await ctx.respond(f"I put you in AFK mode. Reason: {reason}.")

        self.client.db.commit()

    @afk_group.command(description="Remove your AFK status.")
    async def remove(self, ctx):
        cursor = self.client.db.cursor()
        cursor.execute(
            "SELECT reason FROM AFK WHERE user_id = ? and guild_id = ?", (ctx.author.id, ctx.guild.id)
        )
        data = cursor.fetchone()

        if not data:
            await ctx.respond("You do not have the AFK status set.", ephemeral=True)
            return
        else:
            cursor.execute(
                "DELETE FROM AFK WHERE user_id = ? AND guild_id = ?", (ctx.author.id, ctx.guild.id)
            )
            await ctx.respond("Your AFK status has been removed.", ephemeral=True)

def setup(client):
    client.add_cog(AFK(client))
