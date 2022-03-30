import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option
import datetime
import asyncio

embed_color = 0xF00C0C

class OpenTicket(discord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)

    @discord.ui.button(label="Open", emoji="🔓", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def open(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.disabled = True
        await interaction.response.edit_message(view=self)

        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT role_id FROM Tickets WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()

        ticket_role = interaction.guild.get_role(result[0])
        user = self.client.get_user(int(interaction.channel.topic[9:]))

        await interaction.channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await interaction.channel.set_permissions(user, send_messages=True, view_channel=True)
        await interaction.channel.set_permissions(ticket_role, send_messages=True, view_channel=True)

        await interaction.channel.send(
            f"This ticket has been reopened by {interaction.user.mention}.\n"
            "To delete the ticket, press the `Delete` button of the attached message."
        )

        cursor.execute(f"SELECT logs_id FROM Tickets WHERE guild_id = {interaction.guild.id}")
        channel_id = cursor.fetchone()

        logs_channel = self.client.get_channel(channel_id[0])

        log_embed = discord.Embed(
            title="Ticket reopened",
            description=f"{interaction.user.mention} reopened the ticket {interaction.channel.mention}.",
            color=embed_color
        )
        log_embed.timestamp = datetime.datetime.utcnow()

        await logs_channel.send(embed=log_embed)

class NewTicketButtons(discord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", emoji="🔒", style=discord.ButtonStyle.blurple, custom_id="close_ticket")
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.disabled = True
        await interaction.response.edit_message(view=self)

        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT role_id FROM Tickets WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()

        ticket_role = interaction.guild.get_role(result[0])
        user = self.client.get_user(int(interaction.channel.topic[9:]))

        await interaction.channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await interaction.channel.set_permissions(user, send_messages=False, view_channel=True)
        await interaction.channel.set_permissions(ticket_role, send_messages=True, view_channel=True)

        await interaction.channel.send(
            f"This ticket has been closed by {interaction.user.mention}.\n"
            "To reopen the ticket, click on the button below.", view=OpenTicket(self.client)
        )

        cursor.execute(f"SELECT logs_id FROM Tickets WHERE guild_id = {interaction.guild.id}")
        channel_id = cursor.fetchone()

        logs_channel = self.client.get_channel(channel_id[0])

        log_embed = discord.Embed(
            title="Ticket closed",
            description=f"{interaction.user.mention} closed the ticket {interaction.channel.mention}.",
            color=embed_color
        )
        log_embed.timestamp = datetime.datetime.utcnow()

        await logs_channel.send(embed=log_embed)

    @discord.ui.button(label="Delete", emoji="❌", style=discord.ButtonStyle.grey, custom_id="delete_ticket")
    async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT logs_id FROM Tickets WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()

        logs_channel = self.client.get_channel(result[0])

        log_embed = discord.Embed(
            title="Ticket deleted",
            description=f"{interaction.user.mention} closed the ticket #{str(interaction.channel.name)}.",
            color=embed_color
        )
        log_embed.timestamp = datetime.datetime.utcnow()

        await interaction.response.send_message("This ticket will be deleted in 5 seconds.")
        await asyncio.sleep(5)
        await interaction.channel.delete()
        await logs_channel.send(embed=log_embed)

class NewTicket(discord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)

    @discord.ui.button(label="Open a ticket", emoji="📩", style=discord.ButtonStyle.green, custom_id="new_ticket")
    async def new_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT role_id FROM Tickets WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()

        if result is None:
            await interaction.response.send_message(
                f"This server has not yet configured the role for tickets. Contact a server "
                "admin to solve this issue.", ephemeral=True
            )
        else:
            ticket_role = interaction.guild.get_role(result[0])

            cursor.execute(f"SELECT category_id FROM Tickets WHERE guild_id = {interaction.guild.id}")
            result = cursor.fetchone()

            if result is None:
                category = None
            else:
                category = self.client.get_channel(result[0])

            channel = await interaction.guild.create_text_channel(f"{interaction.user.name}-ticket", category=category)

            await channel.set_permissions(interaction.user, send_messages=True, view_channel=True)
            await channel.set_permissions(interaction.guild.default_role, view_channel=False)
            await channel.set_permissions(ticket_role, send_messages = True, view_channel = True)
            
            await channel.edit(topic=f"User ID: {interaction.user.id}")

            embed = discord.Embed(
                title="Thanks for opening a ticket!",
                description=f"{interaction.user.mention}, while a staff member arrives at you, "
                            f"describe your problem or tell us what you need.",
                color=embed_color
            )

            await interaction.response.send_message(f"Ticket opened! {channel.mention}", ephemeral=True)

            message = await channel.send(content=f"{interaction.user.mention} {ticket_role.mention}", embed=embed,
                                         view=NewTicketButtons(self.client))
            await message.pin()

            cursor.execute(f"SELECT logs_id FROM Tickets WHERE guild_id = {interaction.guild.id}")
            channel_id = cursor.fetchone()

            if channel_id is None:
                return
            else:
                logs_channel = self.client.get_channel(channel_id[0])

                log_embed = discord.Embed(
                    title="Ticket opened",
                    description=f"{interaction.user.mention} opened the ticket {channel.mention}.",
                    color=embed_color
                )
                log_embed.timestamp = datetime.datetime.utcnow()

                await logs_channel.send(embed=log_embed)

class Tickets(commands.Cog):
    def __init__(self, client):
        self.client = client

    tickets_group = SlashCommandGroup("ticket", "Setup the ticket system for your server")

    @tickets_group.command(description="See the usable commands for the ticket system.")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Ticket commands",
            description="Available commands for the ticket system.",
            color=embed_color
        )
        embed.add_field(name="/ticket role <role>", value="Set the role that will have access to the tickets.")
        embed.add_field(name="/ticket logs <channel>", value="Set the logs channel for ticket events.",
                        inline=False)
        embed.add_field(name="/ticket category <category>", value="Set the category where tickets will be created.",
                        inline=False)
        embed.add_field(name="/ticket panel <channel> <title> <description>",
                        value="Send the panel to the desired channel to open tickets.",
                        inline=False)

        await ctx.respond(embed=embed)

    @tickets_group.command(description="Set the role that will have access to tickets.")
    @commands.has_permissions(administrator=True)
    async def role(
            self,
            ctx,
            role: Option(discord.Role, "Role that will have access to tickets.")
    ):
        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT role_id FROM Tickets WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            cursor.execute(
                f"INSERT INTO Tickets(guild_id, role_id) VALUES(?,?)", (ctx.guild.id, role.id)
            )
        else:
            cursor.execute(
                "UPDATE Tickets SET role_id = ? WHERE guild_id = ?", (role.id, ctx.guild.id)
            )

        self.client.db.commit()

        await ctx.respond(f"Role has been set to `{role.name}`.")

    @tickets_group.command(description="Set the logs channel for ticket events.")
    @commands.has_permissions(administrator=True)
    async def logs(
            self,
            ctx,
            channel: Option(discord.TextChannel, "Channel where events will be logged.")
    ):
        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT logs_id FROM Tickets WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            cursor.execute(
                f"INSERT INTO Tickets(guild_id, logs_id) VALUES(?,?)", (ctx.guild.id, channel.id)
            )
        else:
            cursor.execute(
                "UPDATE Tickets SET logs_id = ? WHERE guild_id = ?", (channel.id, ctx.guild.id)
            )

        self.client.db.commit()

        await ctx.respond(f"Logs channel has been set to {channel.mention}.")

    @tickets_group.command(description="Set the category where tickets will be created.")
    @commands.has_permissions(administrator=True)
    async def category(
            self,
            ctx,
            category: Option(discord.CategoryChannel, "Category where tickets will be created.")
    ):
        cursor = self.client.db.cursor()
        cursor.execute(f"SELECT category_id FROM Tickets WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            cursor.execute(
                f"INSERT INTO Tickets(guild_id, category_id) VALUES(?,?)", (ctx.guild.id, category.id)
            )
        else:
            cursor.execute(
                "UPDATE Tickets SET category_id = ? WHERE guild_id = ?", (category.id, ctx.guild.id)
            )

        self.client.db.commit()

        await ctx.respond(f"Category has been set to `{category.name}`.")

    @tickets_group.command(description="Send in a channel the panel for opening tickets.")
    @commands.has_permissions(administrator=True)
    async def panel(
            self,
            ctx,
            channel: Option(discord.TextChannel, "Channel where the panel will be sent."),
            title: Option(str, "The title of the panel."),
            description: Option(str, "The description of the panel.")
    ):
        embed = discord.Embed(
            title=f"{title}",
            description=f"{description}",
            color=embed_color
        )

        await channel.send(embed=embed, view=NewTicket(self.client))
        await ctx.respond(f"Panel sent in {channel.mention}.", ephemeral=True)

def setup(client):
    client.add_cog(Tickets(client))
