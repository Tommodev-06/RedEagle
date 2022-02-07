import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import datetime
import humanfriendly
import asyncio

embed_color = 0xF00C0C
success = "<:mod_success:908415224544100362>"
fail = "<:mod_fail:908415224657375293>"

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(description="Lock a text channel.")
    @commands.has_permissions(manage_messages=True)
    async def lock(
            self,
            ctx,
            channel: Option(discord.TextChannel, "Channel to be locked.", required=False),
            reason: Option(str, "Reason for locking the channel.", required=False, default=None)
    ):
        channel = ctx.channel or channel

        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False

        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.respond(f"{success} Successfully locked {channel.mention}",
                          ephemeral=True)

        embed = discord.Embed(
            title="Channel locked",
            description=f"This channel was locked by {ctx.author.mention} 🔒",
            color=embed_color
        )
        embed.add_field(name="Reason", value=reason)

        await channel.send(embed=embed)

    @slash_command(description="Unlock a text channel.")
    @commands.has_permissions(manage_messages=True)
    async def unlock(
            self,
            ctx,
            channel: Option(discord.TextChannel, "Channel to be unlocked.", required=False),
            reason: Option(str, "Reason for unlocking the channel.", required=False, default=None)
    ):
        channel = ctx.channel or channel

        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True

        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.respond(f"{success} Successfully unlocked {channel.mention}",
                          ephemeral=True)

        embed = discord.Embed(
            title="Channel unlocked",
            description=f"This channel was unlocked by {ctx.author.mention} 🔓",
            color=embed_color
        )
        embed.add_field(name="Reason", value=reason)

        await channel.send(embed=embed)

    @slash_command(description="Kick a user.")
    @commands.has_permissions(kick_members=True)
    async def kick(
            self,
            ctx,
            user: Option(discord.Member, "User to be kicked."),
            reason: Option(str, "Reason of the kick.", required=False, default=None)
    ):
        if user == ctx.author:
            await ctx.respond(f"{fail} You can't kick yourself", ephemeral=True)
            return

        if user.top_role > ctx.author.top_role or user.top_role == ctx.author.top_role or user == ctx.guild.owner:
            await ctx.respond(f'{fail} That user is above you or he/she is the owner of "{ctx.guild}", ',
                              "so you can't kick them.", ephemeral=True)
            return

        elif user.id == self.client.user.id:
            await ctx.respond(f"{fail} I can't kick myself!", ephemeral=True)
            return

        elif ctx.guild.me.top_role <= user.top_role:
            await ctx.respond(
                f"{fail} The user has a higher role or the same top role as mine.\n"
                "Please move my role higher!", ephemeral=True
            )
            return

        try:
            await user.send(f'You were kicked from "{ctx.guild}". Reason: {reason}.')
        except:
            pass

        await ctx.guild.kick(user, reason=f"Kicked by {ctx.author}. Reason: {reason}.")

        embed = discord.Embed(
            title="User kicked",
            description=f"{user.mention} was kicked by {ctx.author.mention}.",
            color=embed_color
        )
        embed.add_field(name="Reason", value=reason)

        await ctx.respond(embed=embed)

    @slash_command(description="Ban a user.")
    @commands.has_permissions(ban_members=True)
    async def ban(
            self,
            ctx,
            user: Option(discord.Member, "User to be banned."),
            reason: Option(str, "Reason of the ban.", required=False, default=None)
    ):
        if user == ctx.author:
            await ctx.respond(f"{fail} You can't ban yourself", ephemeral=True)
            return

        if user.top_role > ctx.author.top_role or user.top_role == ctx.author.top_role or user == ctx.guild.owner:
            await ctx.respond(f'{fail} That user is above you or he/she is the owner of "{ctx.guild}", ',
                              "so you can't ban them.", ephemeral=True)
            return

        elif user.id == self.client.user.id:
            await ctx.respond(f"{fail} I can't ban myself!", ephemeral=True)
            return

        elif ctx.guild.me.top_role <= user.top_role:
            await ctx.respond(
                f"{fail} The user has a higher role or the same top role as mine.\n"
                "Please move my role higher!", ephemeral=True
            )
            return

        try:
            await user.send(f'You were banned from "{ctx.guild}". Reason: {reason}.')
        except:
            pass

        await ctx.guild.ban(user, reason=f"Banned by {ctx.author}. Reason: {reason}.")

        embed = discord.Embed(
            title="User banned",
            description=f"{user.mention} was banned by {ctx.author.mention}.",
            color=embed_color
        )
        embed.add_field(name="Reason", value=reason)

        await ctx.respond(embed=embed)

    async def mute_checker(self, ctx, bot_role, user, muted_role):
        bot_role = ctx.guild.me.top_role

        if user == ctx.author:
            await ctx.respond(f"{fail} You can't mute yourself!", ephemeral=True)
            return False

        if user == self.client.user:
            await ctx.respond(f"{fail} I can't mute myself!", ephemeral=True)
            return False

        if bot_role <= user.top_role:
            await ctx.respond(
                f"{fail} The user has a higher role or the same top role as mine.\n"
                "Please move my role higher!", ephemeral=True
            )
            return False

        if user.guild_permissions.administrator:
            await ctx.respond(f"{fail} This user has administrator perms in this server, "
                              "so you can't mute them.", ephemeral=True)
            return False

        if user.top_role > ctx.author.top_role or user.top_role == ctx.author.top_role or user == ctx.guild.owner:
            await ctx.respond(f'{fail} That user is above you or he/she is the owner of "{ctx.guild}", ',
                              "so you can't mute them.", ephemeral=True)
            return False

        if bot_role <= muted_role:
            await ctx.respond(
                f"{fail} My role is too low. I can only mute users if my role is higher than "
                "the Muted role!", ephemeral=True
            )
            return False

    @slash_command(description="Mute a user.")
    @commands.has_permissions(manage_roles=True)
    async def mute(
            self,
            ctx,
            user: Option(discord.Member, "User to be muted."),
            reason: Option(str, "Reason of the mute.", required=False, default=None)
    ):
        muted_role = discord.utils.get(ctx.guild.roles[::-1], name="Muted")

        if (
                await self.mute_checker(ctx, ctx.guild.me.top_role, user, muted_role)
                == False
        ):
            return
        else:
            await user.add_roles(muted_role, reason=f"Muted by {ctx.author}. Reason: {reason}.")

            embed = discord.Embed(
                title="User muted",
                description=f"{user.mention} was muted by {ctx.author.mention}.",
                color=embed_color
            )
            embed.add_field(name="Reason", value=reason)

            await ctx.respond(embed=embed)
            await user.send(f'You were muted in "{ctx.guild}". Reason: {reason}.')

    @slash_command(description="Temporarily mute a user.")
    @commands.has_permissions(manage_roles=True)
    async def tempmute(
            self,
            ctx,
            user: Option(discord.Member, "Member to be temporarily muted."),
            time: Option(str, "Tempmute duration."),
            reason: Option(str, "Reason of the tempmute.", required=False, default=None)
    ):
        muted_role = discord.utils.get(ctx.guild.roles[::-1], name="Muted")  # Just for the lines below.

        if (
                await self.mute_checker(ctx, ctx.guild.me.top_role, user, muted_role)
                == False
        ):
            return

        if "s" or "m" or "d" or "w" in str(time):
            time = humanfriendly.parse_timespan(time)
            if time > 604800:
                await ctx.respond("The max value is one week (`7d` or `1w`).", ephemeral=True)
                return
            else:
                now = datetime.datetime.utcnow()
                until = now + datetime.timedelta(seconds=time)

                await user.timeout(until, reason=f"Temporarily muted by {ctx.author}. Reason: {reason}.")

                embed = discord.Embed(
                    title="User muted",
                    description=f"{user.mention} was temporarily muted by {ctx.author.mention}.",
                    color=embed_color
                )
                embed.add_field(name="Reason", value=reason)

                await ctx.respond(embed=embed)
                await user.send(f'You were temporarily muted in "{ctx.guild}". Reason: {reason}')

    @tempmute.error
    async def tempmute_error(self, ctx, time):
        if "s" or "m" or "d" or "y" not in str(time):
            await ctx.respond(
                "Invalid durantion. You can use `s` for seconds, `m` for minutes, `d` for days and `w` for weeks.",
                ephemeral=True
            )
            return

    @slash_command(description="Unmute a user.")
    async def unmute(
            self,
            ctx,
            user: Option(discord.Member, "Member to be unmuted.")
    ):
        muted_role = discord.utils.get(ctx.guild.roles[::-1], name="Muted")

        if ctx.guild.me.top_role <= muted_role:
            await ctx.respond(
                f"{fail} My role is too low. I can only unmute users if my role is higher than "
                "the Muted role!", ephemeral=True
            )
            return
        elif ctx.guild.me.top_role <= user.top_role:
            await ctx.send(
                f"{fail} The user has a higher role or the same top role as mine.\n"
                "Please move my role higher!", ephemeral=True
            )
            return

        if muted_role in user.roles:
            await user.remove_roles(muted_role)
        else:
            await user.remove_timeout()

        embed = discord.Embed(
            title="User unmuted",
            description=f"{user.mention} was unmuted by {ctx.author.mention}.",
            color=embed_color
        )

        await ctx.respond(embed=embed)

    @slash_command(description="Clear the specified amount of messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(
            self,
            ctx,
            amount: Option(int, "Amount of messages to be deleted.")
    ):
        messages = []
        async for message in ctx.channel.history(limit=amount + 1):
            messages.append(message)

        if amount > 100:
            await ctx.respond(f"{fail} You can delete up to 100 messages!", ephemeral=True)
        else:
            try:
                await ctx.channel.purge(limit=amount)
                await ctx.respond(f"{success} {len(messages)} messages have been deleted.")

                await asyncio.sleep(1.5)
                await ctx.interaction.delete_original_message()
            except:
                await ctx.respond(f"{fail} Due to Discord's ToS, you can't delete messages that "
                                  "are more than 14 days old.", ephemeral=True)
                return

    @slash_command(description="Set the slowmode to the specified seconds.")
    @commands.has_permissions(manage_messages=True)
    async def slowmode(
            self,
            ctx,
            seconds: Option(int, "Seconds of the slowmode.")
    ):
        if seconds > 21600:
            await ctx.respond(f"{fail} You can't set the slowmode to {seconds} seconds because the "
                              "maximum delay is 6 hours (21600 seconds).", ephemeral=True)
        elif seconds < 0:
            await ctx.respond(f"{fail} You can't set the slowmode to {seconds} seconds because "
                              "seconds must be greater than or equal to 0 (if you put 0, the slowmode will be off).",
                              ephemeral=True)
        elif seconds == 1:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.respond(f"{success} Set the slowmode in this channel to `1` second.")
        elif seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.respond(f"{success} Disabled the slowmode in this channel.")
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.respond(f"{success} Set the slowmode in this channel to `{seconds}` seconds.")

def setup(client):
    client.add_cog(Moderation(client))
