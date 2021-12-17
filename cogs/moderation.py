import diskord
from diskord.ext import commands
import datetime
import asyncio

embed_color = 0xF00C0C
prefix = "re!"
success = "<a:success:865522277729566741>"
fail = "<a:fail:866017479696318534>"


# noinspection PyTypeChecker
class Moderation(commands.Cog, description="Moderation commands"):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Lock a text channel")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: diskord.TextChannel = None):
        channel = ctx.channel or channel

        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"{success} Successfully locked {channel.mention}", delete_after=2)

        embed = diskord.Embed(
            title="Channel locked",
            description=f"This channel was locked by {ctx.author.mention} 🔒",
            color=0x538AEE
        )
        embed.timestamp = datetime.datetime.utcnow()

        await channel.send(embed=embed)

    @commands.command(help="Unlock a text channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: diskord.TextChannel = None):
        channel = ctx.channel or channel

        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"{success} Successfully unlocked {channel.mention}", delete_after=2)

        embed = diskord.Embed(
            title="Channel unlocked",
            description=f"This channel was unlocked by {ctx.author.mention} 🔓",
            color=0x538AEE
        )
        embed.timestamp = datetime.datetime.utcnow()

        await channel.send(embed=embed)

    @commands.command(help="Kick a user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason: str = None):
        if member == ctx.author:
            await ctx.message.delete()
            await ctx.send(f"{fail} You can't kick yourself!", delete_after=3)
            return
        elif member.top_role >= ctx.author.top_role or member == ctx.guild.owner:
            await ctx.message.delete()
            await ctx.send(f"{fail} That user is above you or he/she is the owner of {ctx.guild}, so you can't kick "
                           f"him/her.",
                           delete_after=4.5)
            return
        elif member.id == self.client.user.id:
            await ctx.message.delete()
            await ctx.send(f"{fail} I can't kick myself!", delete_after=3)
            return
        elif ctx.guild.me.top_role <= member.top_role:
            await ctx.message.delete()
            await ctx.send(
                f"{fail} The user has a higher role or the same top role as mine.\n"
                + "Please move my role higher!", delete_after=3
            )
            return

        try:
            await member.send(f"You were kicked from {ctx.guild}! Reason: {reason}.")
        except:
            pass

        await ctx.guild.kick(member, reason=f"Kicked by {ctx.author}. Reason: {reason}")

        embed = diskord.Embed(
            title="User kicked",
            description=f"{member.mention} was kicked by {ctx.author.mention}.",
            color=0x538AEE
        )
        embed.add_field(name="Reason", value=reason)
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)

    @commands.command(help="ban a user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason: str = None):
        if member == ctx.author:
            await ctx.message.delete()
            await ctx.send(f"{fail} You can't ban yourself!", delete_after=3)
            return
        elif member.top_role >= ctx.author.top_role or member == ctx.guild.owner:
            await ctx.message.delete()
            await ctx.send(
                f"{fail} That user is above you or he/she is the owner of {ctx.guild}, so you can't ban him/her.",
                delete_after=4.5)
            return
        elif member.id == self.client.user.id:
            await ctx.message.delete()
            await ctx.send(f"{fail} I can't ban myself!", delete_after=3)
            return
        elif ctx.guild.me.top_role <= member.top_role:
            await ctx.message.delete()
            await ctx.send(
                f"{fail} The user has a higher role or the same top role as mine.\n"
                + "Please move my role higher!", delete_after=3
            )
            return

        try:
            await member.send(f"You were banned from {ctx.guild}! Reason: {reason}.")
        except:
            pass

        await ctx.guild.ban(member, reason=f"Banned by {ctx.author}. Reason: {reason}")

        embed = diskord.Embed(
            title="User banned",
            description=f"{member.mention} was banned by {ctx.author.mention}.",
            color=0x538AEE
        )
        embed.add_field(name="Reason", value=reason)
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)

    async def mute_checker(self, ctx, bot_role, member, muted_role):
        bot_role = ctx.guild.me.top_role

        if member == ctx.author:
            await ctx.message.delete()
            await ctx.send(f"{fail} You can't mute yourself!", delete_after=3)
            return False
        elif member == self.client.user:
            await ctx.message.delete()
            await ctx.send(f"{fail} I can't mute myself!", delete_after=3)
            return False
        elif bot_role <= member.top_role:
            await ctx.message.delete()
            await ctx.send(
                f"{fail} The user has a higher role or the same top role as mine.\n"
                + "Please move my role higher!", delete_after=3
            )
            return False
        elif member.guild_permissions.administrator:
            await ctx.message.delete()
            await ctx.send(f"{fail} This user has `Adminstrator` perms in this server, so you can't mute him/her.",
                           delete_after=3)
            return False
        elif member.top_role > ctx.author.top_role or member.top_role == ctx.author.top_role or member == ctx.guild.owner:
            await ctx.message.delete()
            await ctx.send(f"{fail} That user is above you or he/she is the wwner of {ctx.guild}, "
                           "so you can't mute him/her.", delete_after=3)
            return False
        elif bot_role <= muted_role:
            await ctx.message.delete()
            await ctx.send(
                f"{fail} My role is too low. I can only mute users if my role is higher than "
                "the Muted role!", delete_after=3
            )
            return False
        elif muted_role in member.roles:
            await ctx.message.delete()
            await ctx.send(f"{fail} This user is muted yet!", delete_after=3)
            return False

    @commands.command(help="Mute a user")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: commands.MemberConverter, *, reason: str = None):
        muted_role = diskord.utils.get(ctx.guild.roles[::-1], name="Muted")

        # noinspection PyTypeChecker
        if (
                await self.mute_checker(ctx, ctx.guild.me.top_role, member, muted_role)
                == False
        ):
            return
        else:
            await member.add_roles(muted_role, reason=f"Muted by {ctx.author}. Reason: {reason}")

            embed = diskord.Embed(
                title="User muted",
                description=f"{member.mention} was muted by {ctx.author.mention}.",
                color=0x538AEE
            )
            embed.add_field(name="Reason", value=reason)

            await ctx.send(embed=embed)

            embeddm = diskord.Embed(
                title="You were muted",
                description=f"You were muted in **{ctx.guild}** by **{ctx.author}**.",
                color=0x538AEE
            )
            embeddm.add_field(name="Reason", value=reason)

            await member.send(embed=embeddm)

    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}

    invalid_duration_msg = (
            "<a:fail:866017479696318534> **Invalid duration**! Here are some examples:\n\n"
            + f'`{prefix}tempmute @Brosky 2d Spam`- 2 days, with reason "Spam"\n'
            + f"`{prefix}tmute @Brosky 1h`- 1 hour without any reason\n"
            + f"`{prefix}tempmute @Brosky 20m`- 20 minutes without any reason\n"
            + "\nYou can also use `s` for seconds."
    )

    async def time2seconds(self, send, time):
        try:
            return int(time[:-1]) * self.time_convert[time[-1]]
        except:
            try:
                return int(time)
            except:
                await send(self.invalid_duration_msg)
                return False

    @commands.command(help="Tempmute a user", aliases=["tmute"])
    @commands.has_permissions(manage_roles=True)
    async def tempmute(self, ctx, member: commands.MemberConverter, duration: str, *, reason: str = None):
        muted_role = diskord.utils.get(ctx.guild.roles[::-1], name="Muted")
        unit_tuple = tuple([unit for unit in self.time_convert.keys()])
        sleep_duration = await self.time2seconds(ctx.send, duration.lower())

        if sleep_duration is False:
            return

        if not duration.lower().endswith(unit_tuple) or not duration[0].isdigit():
            await ctx.send(self.invalid_duration_msg)
            return

        if muted_role in member.roles:
            await ctx.send("<a:fail:866017479696318534> | This user is muted yet!")
            return

        if (
                await self.mute_checker(ctx, ctx.guild.me.top_role, member, muted_role)
                == False
        ):
            return

        await member.add_roles(muted_role, reason=reason)

        embed = diskord.Embed(
            title="User muted",
            description=f"{member.mention} was temporarily muted by {ctx.author.mention}.",
            color=embed_color
        )
        embed.add_field(name="Reason", value=reason)

        embdm = diskord.Embed(
            title="You were muted",
            description=f"You were temporarily muted in **{ctx.guild.name}** by **{ctx.author}**.",
            color=embed_color
        )
        embdm.add_field(name="Reason", value=reason)

        if not duration[-1].isalpha():
            embed.add_field(name="Auto-unmute after", value=str(duration) + " seconds")
            embdm.add_field(name="Auto-unmute after", value=str(duration) + " seconds")
        else:
            embed.add_field(name="Auto-unmute after", value=duration)
            embdm.add_field(name="Auto-unmute after", value=duration)

            await ctx.send(embed=embed)
            await member.send(embed=embdm)

            await asyncio.sleep(sleep_duration)
            await member.remove_roles(muted_role, reason="Tempmute finished")

            embch = diskord.Embed(
                title="User unmuted",
                description=f"{member.mention} was unmuted",
                color=embed_color
            )
            embch.add_field(name="Reason", value="Tempmute finished")

            embend = diskord.Embed(
                title="You were unmuted",
                description=f"You were unmuted in **{ctx.guild.name}**.",
                color=embed_color
            )
            embend.add_field(name="Reason", value="Tempmute finished")

            await member.send(embed=embend)
            await ctx.channel.send(embed=embch)

    @commands.command(help="Unmute a user")
    async def unmute(self, ctx, member: commands.MemberConverter):
        muted_role = diskord.utils.get(ctx.guild.roles[::-1], name="Muted")

        if not muted_role in member.roles:
            await ctx.message.delete()
            await ctx.send(f"{fail} This user isn't muted!")
            return

        elif ctx.guild.me.top_role <= muted_role:
            await ctx.message.delete()
            await ctx.send(
                f"{fail} My role is too low. I can only unmute users if my role is higher than "
                "the Muted role!", delete_after=3
            )
            return

        elif ctx.guild.me.top_role <= member.top_role:
            await ctx.message.delete()
            await ctx.send(
                f"{fail} The user has a higher role or the same top role as mine.\n"
                + "Please move my role higher!", delete_after=3
            )
            return

        await member.remove_roles(muted_role)

        embed = diskord.Embed(
            title="User unmuted",
            description=f"{member.mention} was unmuted by {ctx.author.mention}.",
            color=0x538AEE
        )

        await ctx.send(embed=embed)

        embeddm = diskord.Embed(
            title="You were unmuted",
            description=f"You were unmuted in **{ctx.guild.name}** by **{ctx.author}**.",
            color=0x538AEE
        )
        await member.send(embed=embeddm)

    @commands.command(help="Clear the specified amount of messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount > 100:
            await ctx.message.delete()
            await ctx.send(f"{fail} You can delete up to 100 messages!", delete_after=3)
        else:
            try:
                await ctx.channel.purge(limit=amount)
                await ctx.send(f"{success} {amount} messages have been deleted by {ctx.author}.", delete_after=3)
            except diskord.Forbidden:
                pass
                await ctx.send(
                    f"{fail} Due to Discord's ToS, you can't delete messages that are more than 14 days old.", delete_after=4
                )

    @commands.command(help="Set the slowmode to the specified seconds")
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int):
        if seconds > 21600:
            await ctx.message.delete()
            await ctx.send(f"{fail} Can't set the slowmode to {seconds} seconds because the "
                           "maximum delay is 6 hours (21600 seconds).", delete_after=3)
        elif seconds < 0:
            await ctx.message.delete()
            await ctx.send(f"{fail} Can't set the slowmode to {seconds} seconds because "
                           "seconds must be greater than or equal to 0 (if you put 0, the slowmode will be off).",
                           delete_after=3)
        elif seconds == 1:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"{success} Set the slowmode in this channel to `1` second.")
        elif seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"{success} Disabled the slowmode in this channel.")
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"{success} Set the slowmode delay in this channel to `{seconds}` seconds.")

def setup(client):
    client.add_cog(Moderation(client))
