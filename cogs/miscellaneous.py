import diskord
from diskord.ext import commands

embed_color = 0xF00C0C
botversion = "0.4"

class Miscellaneous(commands.Cog, description="Miscellaneous commands"):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Get the bot's latency")
    async def ping(self, ctx):
        await ctx.send(content=f":ping_pong: The bot latency is **{round(self.client.latency * 1000, 1)}ms**.")

    @commands.command(help="Get information about a user", aliases=["ui"])
    async def userinfo(self, ctx, user: commands.MemberConverter = None):
        user = user or ctx.author

        embed = diskord.Embed(
            title=f"Information about {user}",
            color=embed_color
        )
        embed.add_field(name="Joined this server", value=f"<t:{round(user.joined_at.timestamp())}:R>")
        embed.add_field(name="Joined Discord", value=f"<t:{round(user.created_at.timestamp())}:R>")
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1), inline=False)
        if len(user.roles) > 1:
            roles = ", ".join([role.mention for role in list(user.roles[::-1]) if not role is ctx.guild.default_role])
            embed.add_field(name="Roles [{}]".format(len(user.roles) - 1), value=roles)
        embed.set_thumbnail(url=f"{user.avatar}")

        await ctx.send(embed=embed)

    @commands.command(help="Get information about this server", aliases=["si"])
    async def serverinfo(self, ctx):
        humans = [member for member in ctx.guild.members if not member.bot]
        bots = [member for member in ctx.guild.members if member.bot]

        embed = diskord.Embed(
            title=f"Information about {ctx.guild.name}",
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
        embed.set_thumbnail(url=ctx.guild.icon)

        await ctx.send(embed=embed)

    @commands.command(help="Get the profile picture of a user", aliases=["av", "pfp"])
    async def avatar(self, ctx, user: commands.MemberConverter = None):
        user = user or ctx.author

        embed = diskord.Embed(
            title=f"Avatar of {user.name}",
            description=f"The avatar of {user} is available at this [link]({user.avatar}).",
            color=embed_color
        )
        embed.set_image(url=f"{user.avatar}")

        await ctx.send(embed=embed)

    @commands.command(help="Make the bot say something")
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, text: str):
        await ctx.message.delete()
        await ctx.send(text)

    @commands.command(help="Create an embed with your text")
    @commands.has_permissions(administrator=True)
    async def embedsay(self, ctx, *, options):
        title, description = options.split("//")

        await ctx.message.delete()

        embed = diskord.Embed(
            title=title,
            description=description,
            color=embed_color
        )
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")
        embed.set_footer(text=f"{ctx.guild.name}")

        await ctx.send(embed=embed)

    @commands.command(help="See our partnership with GalaxyNodes")
    async def sponsor(self, ctx):
        embed = diskord.Embed(
            title="RedEagle's Sponsor",
            description="Me, Tommodev#9134, and GalaxyNodes, RedEagle's hosting service, decided to make a "
                        "partnership. GalaxyNodes is a hosting service for Discord Bot and also Minecraft Servers! If "
                        "you need a cheap and fast host, I recommend you to join their server [here]("
                        "https://discord.gg/DB7hmw29ZH).",
            color=embed_color
        )

        await ctx.send(embed=embed)

    @commands.command(help="Get information about RedEagle", aliases=["info"])
    async def stats(self, ctx):
        embed = diskord.Embed(
            title=f"Info and Stats about RedEagle",
            description=f"""
            **Bot Info**
            <:developer:918867639886049301> Tommodev#9134
            <:python:918867852176551966> Developed in Python
            <:terminal:918868581150756894> Prefixes: `re!` | `Re!` | `@mention `
            <:file_upload:918872362336804895> Version: `{botversion}`
            
            **Bot Stats**
            <:time:918871014182625281> Latency: `{round(self.client.latency * 1000, 1)}ms`
            <:server:918872745033490482> Servers: `{len(self.client.guilds)} servers`
            <:users:918873187670970389> Users: `{sum([len(guild.members) for guild in self.client.guilds])} users`
            <:list:918876883599368284> N. of commands: `{len(self.client.commands)} commands`
            """,
            color=embed_color
        )
        embed.set_thumbnail(url=f"{self.client.user.avatar}")

        await ctx.send(embed=embed)

    @commands.command(help="See what's new in the latest version of RedEagle")
    async def changelog(self, ctx):
        embed = diskord.Embed(
            title=f"What's new in the {botversion} version?",
            description=f"""
            
➜ New help command.
            
            """,
            color=embed_color
        )

        await ctx.send(embed=embed)

    @commands.command(help="Get the invite link of RedEagle")
    async def invite(self, ctx):
        await ctx.send(""" 
               
Thanks for your interest in the bot! Invite it with the link below!

https://dsc.gg/redeagle   
        
        """)

    @commands.command(help="Get the support server's link")
    async def support(self, ctx):
        await ctx.send("""
        
Join the support server with the link below!
    
https://discord.gg/tTTuNRwRYJ        
        
        """)

    @commands.command(help="Upvote RedEagle on Top.gg")
    async def vote(self, ctx):
        embed = diskord.Embed(
            title="Vote RedEagle",
            description=f"[Click here to vote on Top.gg](https://top.gg/bot/856643485340139580/vote)",
            color=embed_color
        )

        await ctx.send(embed=embed)

    @commands.command(help="Submit a suggestion")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion: str):
        if len(suggestion) < 10:
            await ctx.send("Your suggestion is too short. It must be at least 10 characters long.")
            return
        else:
            channel = await self.client.fetch_channel(869313090720772127)

            embed = diskord.Embed(
                title="Suggestion",
                description=f"{suggestion}",
                color=embed_color
            )
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")
            embed.set_footer(text=f"User ID: {ctx.author.id}")

            await ctx.send("Suggestion successfully submitted!")
            await channel.send(embed=embed)

def setup(client):
    client.add_cog(Miscellaneous(client))
