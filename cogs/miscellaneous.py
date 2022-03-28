import discord
from discord.ext import commands
from discord.commands import slash_command, Option

embed_color = 0xF00C0C

class ServerButton(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label="Official Server", url="https://discord.gg/tTTuNRwRYJ"))

class InviteButton(discord.ui.View):
    def __init__(self):
        super().__init__()

        invite_url = "https://discord.com/api/oauth2/authorize?client_id=856643485340139580&permissions=8&scope=bothttps://discord.com/api/oauth2/authorize?client_id=856643485340139580&permissions=8&scope=bot%20applications.commands"

        self.add_item(discord.ui.Button(label="Invite", url=invite_url))

class GalaxyNodes(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label="GalaxyNodes Server", url="https://discord.gg/DB7hmw29ZH"))

class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(description="Get the bot's latency.")
    async def ping(self, ctx):
        await ctx.respond(f":ping_pong: The bot latency is **{round(self.client.latency * 1000, 1)}ms**.")

    @slash_command(description="Get information about a user.")
    async def userinfo(
            self,
            ctx,
            user: Option(discord.Member, "User to show information about.", required=False)
    ):
        user = user or ctx.author

        embed = discord.Embed(
            title=f"Information about {user}",
            color=embed_color
        )
        embed.add_field(name="Joined the server", value=f"<t:{round(user.joined_at.timestamp())}:R>")
        embed.add_field(name="Account created", value=f"<t:{round(user.created_at.timestamp())}:R>")
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1), inline=False)
        if len(user.roles) > 1:
            roles = ", ".join([role.mention for role in list(user.roles[::-1]) if not role is ctx.guild.default_role])
            embed.add_field(name=f"Roles [{len(user.roles) - 1}]", value=roles)
        embed.set_thumbnail(url=f"{user.avatar}")
        embed.set_footer(text=f"User ID: {user.id}")

        await ctx.respond(embed=embed)

    @slash_command(description="Get information about this server.")
    async def serverinfo(self, ctx):
        humans = [member for member in ctx.guild.members if not member.bot]
        bots = [member for member in ctx.guild.members if member.bot]

        embed = discord.Embed(
            title=f"Information about {ctx.guild}",
            color=embed_color
        )

        total_text_channels = len(ctx.guild.text_channels)
        total_voice_channels = len(ctx.guild.voice_channels)
        total_channels = total_text_channels + total_voice_channels

        embed.add_field(name="Total channels", value=total_channels)
        embed.add_field(name="Text channels", value=total_text_channels)
        embed.add_field(name="Voice channels", value=total_voice_channels)
        embed.add_field(name="Members", value=ctx.guild.member_count)
        embed.add_field(name="Humans", value=f"{len(humans)} humans")
        embed.add_field(name="Bots", value=f"{len(bots)} bots")
        embed.add_field(name="Roles", value=len(ctx.guild.roles))
        embed.add_field(name="Boost", value=ctx.guild.premium_subscription_count)
        embed.add_field(name="Owner", value=ctx.guild.owner.mention)
        embed.add_field(name="Created", value=f"<t:{round(ctx.guild.created_at.timestamp())}:R>")
        embed.add_field(name="Emojis", value=f"{len(ctx.guild.emojis)} emojis")
        embed.add_field(name="Verification level", value=f"{str(ctx.guild.verification_level).capitalize()}")
        embed.set_footer(text=f"Guild ID: {ctx.guild.id}")
        embed.set_thumbnail(url=ctx.guild.icon)

        await ctx.respond(embed=embed)

    @slash_command(description="Get the profile picture of a user.")
    async def avatar(
            self,
            ctx,
            user: Option(discord.Member, "User whose avatar to show.", required=False)
    ):
        user = user or ctx.author
        
            
        embed = discord.Embed(
            title=f"Avatar of {user.name}",
            description=f"The avatar of {user} is available at this [link]({user.display_avatar}).",
            color=embed_color
        )
        embed.set_image(url=f"{user.display_avatar}")

        await ctx.respond(embed=embed)

    @slash_command(description="Make the bot say something.")
    @commands.has_permissions(administrator=True)
    async def say(
            self,
            ctx,
            text: Option(str, "Text to send.")
    ):
        await ctx.respond("Message sent!", ephemeral=True)
        await ctx.send(text)

    @slash_command(description="Create an embed with your text.")
    @commands.has_permissions(administrator=True)
    async def embedsay(
            self,
            ctx,
            title: Option(str, "The title of the embed."),
            description: Option(str, "The description of the embed.")
    ):
        embed = discord.Embed(
            title=title,
            description=description,
            color=embed_color
        )
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")
        embed.set_footer(text=f"{ctx.guild.name}")

        await ctx.respond("Embed created!", ephemeral=True)
        await ctx.channel.send(embed=embed)

    @slash_command(description="See our partnership with GalaxyNodes.")
    async def sponsor(self, ctx):
        embed = discord.Embed(
            title="RedEagle's sponsor",
            description="Me, Tommodev#0001, and GalaxyNodes, RedEagle's hosting service, decided to make a "
                        "partnership. GalaxyNodes is a hosting service for Discord Bot and also Minecraft Servers! If "
                        "you need a cheap and fast host, I recommend you to join their server.",
            color=embed_color
        )

        await ctx.respond(embed=embed, view=GalaxyNodes())

    @slash_command(description="Get information about RedEagle.")
    async def stats(self, ctx):
        developer = self.client.get_user(825292137338765333)
        
        embed = discord.Embed(
            title=f"Info and statistics on RedEagle",
            description=f"""
**Info**
<:developer:918867639886049301> {developer}
<:python:918867852176551966> Developed in Python
<:terminal:918868581150756894> Prefix: `/` (slash commands)
<:file_upload:918872362336804895> Version: `0.5`

**Statistics**
<:time:918871014182625281> Latency: `{round(self.client.latency * 1000, 1)}ms`
<:server:918872745033490482> Servers: `{len(self.client.guilds)} servers`
<:users:918873187670970389> Users: `{sum([len(guild.members) for guild in self.client.guilds])} users`
            """,
            color=embed_color
        )
        embed.set_thumbnail(url=f"{self.client.user.avatar}")

        await ctx.respond(embed=embed)

    @slash_command(description="Submit a suggestion for the bot.")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def advice(self, ctx, suggestion: str):
        if len(suggestion) < 10:
            await ctx.respond("Your suggestion is too short. It must be at least 10 characters long.",
                              ephemeral=True)
            return
        else:
            channel = await self.client.fetch_channel(869313090720772127)

            embed = discord.Embed(
                title="Suggestion",
                description=f"{suggestion}",
                color=embed_color
            )
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.display_avatar}")
            embed.set_footer(text=f"User ID: {ctx.author.id}")

            await ctx.respond("Suggestion successfully submitted!")
            message = await channel.send(embed=embed)
            
            await message.add_reaction("✅")
            await message.add_reaction("❌")

    @slash_command(description="See what's new in the latest version of RedEagle.")
    async def changelog(self, ctx):
        embed = discord.Embed(
            title=f"What's new in the 0.5 version?",
            description=f"""
➜ Moved to slash commands.
            """,
            color=embed_color
        )

        await ctx.respond(embed=embed)

    @slash_command(description="Get the invite link of RedEagle.")
    async def invite(self, ctx):
        await ctx.respond(
            "Thanks for your interest in the bot! Invite it with clicking the button below!", view=InviteButton()
        )

    @slash_command(description="Get the support server's link.")
    async def support(self, ctx):
        await ctx.respond(
            "If you need help with the bot or you want to stay updated, join the official server clicking the button below!",
            view=ServerButton()
        )

    @slash_command(description="Upvote RedEagle.")
    async def vote(self, ctx):
        embed = discord.Embed(
            title="Vote RedEagle",
            description=f"[Click here to vote on Top.gg](https://top.gg/bot/856643485340139580/vote)",
            color=embed_color
        )
        embed.set_thumbnail(url=f"{self.client.user.avatar}")

        await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(Miscellaneous(client))
