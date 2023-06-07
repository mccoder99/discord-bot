import asyncio
import datetime
import os

import aiosqlite
import discord
import ezcord
from discord.commands import SlashCommandGroup
from discord.ext import commands


class TicketSupport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "database.db"

    ticket = SlashCommandGroup("ticket")

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TicketView(self.DB))
        self.bot.add_view(Main(self.DB))

    async def check_guild(self, guild_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("INSERT OR IGNORE INTO ticket_support (guild_id) VALUES (?)", (guild_id,))
            await db.commit()

    @ticket.command(description="› Fügt deinen Server zur Datenbank hinzu. ➕")
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def guild(self, ctx):
        await self.check_guild(ctx.guild.id)
        await ctx.respond("Dein Server wurde erfolgreich eingetragen!", ephemeral=True)

    @ticket.command(description="› Sendet das Ticket-Panel in den Kanal. 🎫")
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def send(self, ctx):
        await self.check_guild(ctx.guild.id)
        embed = discord.Embed(title="Support kontaktieren",
                              description="Klicke auf den Button, um ein neues Ticket zu erstellen.\n\n"
                                          "**⚠️ | Bitte erstelle nur ein Ticket, wenn du ein ernstes Problem hast!**",
                              color=discord.Color.embed_background())
        await ctx.channel.send(embed=embed, view=TicketView(self.DB))
        await ctx.respond("Du hast den Ticket-Support erfolgreich eingerichtet!", ephemeral=True)


def setup(bot):
    bot.add_cog(TicketSupport(bot))


class Logger:
    def __init__(self, channel):
        self.channel = channel

    async def create_log_file(self):
        with open(f"Log {self.channel.name}.txt", "w", encoding="utf-8") as f:
            f.write(f"Ticket | {self.channel.name}\n\n")
            f.write("-----------------------------------------\n")
            messages = await self.channel.history(limit=69420).flatten()
            for i in reversed(messages):
                f.write(f"{i.created_at}: {i.author}: {i.author.id}: {i.content}\n")
            f.write("-----------------------------------------\n\n")
            if len(messages) >= 69420:
                f.write("Es wurden mehr als 69420 Nachrichten in diesen Channel eingesendet. "
                        "Aus Speicher-Gründen wurden nur die letzten 69420 Nachrichten geloggt.")
            else:
                f.write(f"Es wurden {len(messages)} Nachrichten geschrieben")

    async def send_log_file(self, channel: discord.TextChannel):
        await channel.send(files=[discord.File(f"Log {self.channel.name}.txt", filename=f"{self.channel.name}.txt")])
        os.remove(f"Log {self.channel.name}.txt")


class TicketView(ezcord.View):
    def __init__(self, db):
        self.DB = db
        super().__init__(timeout=None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 120, commands.BucketType.user)

    @discord.ui.button(label="Ticket erstellen", style=discord.ButtonStyle.green, emoji="📩", custom_id="ticket", row=1)
    async def button_callback(self, button, interaction):
        button.disabled = False

        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()

        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT guild_id FROM ticket_support WHERE guild_id = ?",
                                  (interaction.guild.id,)) as cursor:
                result = await cursor.fetchone()
        if result is None:
            if interaction.guild.owner == interaction.user:
                await interaction.response.send_message(
                    "🤔 - Tickets können nicht erstellt werden, führe bitte erneut den Ticket Command aus.",
                    ephemeral=True)
            else:
                await interaction.response.send_message(
                    "🤔 - Ich weiß nicht wo ich dein Ticket erstellen soll, "
                    "frag bitte den Server-Owner ob er es aktiviert.", ephemeral=True)
        else:
            if retry:
                time = ezcord.times.dc_timestamp(int(retry), style='R')
                timeup = discord.Embed(title="Cooldown", description=f"Versuche es {time} erneut.",
                                       color=discord.Color.red())
                return await interaction.response.send_message(embed=timeup, ephemeral=True)
            else:
                interaction.message.author = interaction.user
                async with aiosqlite.connect(self.DB) as db:
                    async with db.execute(
                            "SELECT printf('%03d', ticket_count + 1) FROM ticket_support WHERE guild_id = ?",
                            (interaction.guild.id,)
                    ) as cursor:
                        result = await cursor.fetchone()

                channel_count = result[0]
                overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                              interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)}

                ticket_channel = await interaction.guild.create_text_channel(
                    f"🎫・ticket-{channel_count}", topic=f"Ticket von {interaction.user.name}\n\n**Informationen**\n"
                                                       f"Ticket-nummer: {channel_count}\n"
                                                       f"User-ID: {interaction.user.id}", overwrites=overwrites
                )
                await interaction.response.send_message(
                    f"Dein Ticket wurde erfolgreich erstellt, du findest es hier: {ticket_channel.mention}",
                    ephemeral=True)

                file = discord.File("images/ticket.png", filename="ticket_support.png")
                embed = discord.Embed(title=f"Willkommen in deinem Ticket!",
                                      description="**Um zu beginnen, bitte befolge diese Schritte**\n"
                                                  "Nenne uns dein Anliegen und habe ein bisschen Geduld.\n"
                                                  "In der Zwischenzeit kannst du auch die Regeln durchlesen."
                                                  "\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
                                                  "Unser Team wird sich so schnell wie "
                                                  "möglich um dein Anliegen drum kümmern.",
                                      timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
                embed.set_thumbnail(url="attachment://ticket_support.png")
                embed.set_footer(text=f"Erstellt von {interaction.user} • {interaction.user.id}",
                                 icon_url=interaction.user.display_avatar.url)
                await ticket_channel.send(interaction.user.mention, embed=embed, file=file, view=Main(self.DB))
                async with aiosqlite.connect(self.DB) as db:
                    await db.execute(
                        "UPDATE ticket_support SET ticket_count = ticket_count + 1 WHERE guild_id = ?",
                        (interaction.guild.id,)
                    )
                    await db.commit()


class Main(ezcord.View):
    def __init__(self, db):
        self.DB = db
        super().__init__(timeout=None)

    @discord.ui.button(label="Schließen", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close", row=1)
    async def button_callback1(self, button, interaction):
        button.disabled = True

        for child in self.children:
            child.disabled = True

        embed1 = discord.Embed(title="Ticket wurde geschlossen",
                               description=f"{interaction.user.mention} hat dein Ticket geschlossen. "
                                           "Dieser Channel wird in wenigen Sekunden gelöscht.",
                               timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=embed1)
        logger = Logger(interaction.channel)
        await logger.create_log_file()
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute(
                    "SELECT printf('%03d', ticket_count) FROM ticket_support WHERE guild_id = ?",
                    (interaction.guild.id,)) as cursor:
                result = await cursor.fetchone()

        channel_count = result[0]
        overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)}
        log_channel = await interaction.guild.create_text_channel(f"🔐・ticket-{channel_count}", overwrites=overwrites)
        await logger.send_log_file(log_channel)
        await asyncio.sleep(5)
        await interaction.channel.delete()

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.green, emoji="✅", custom_id="edit", row=1)
    async def button_callback2(self, button, interaction):
        button.disabled = True

        embed = discord.Embed(title="Ticket angenommen",
                              description=f"{interaction.user.mention} kümmert sich um dein Ticket",
                              color=discord.Color.embed_background())
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Regeln", style=discord.ButtonStyle.blurple, emoji="🔖", custom_id="rules", row=1)
    async def button_callback3(self, button, interaction):
        button.disabled = False

        embed = discord.Embed(title="Ticket Regeln",
                              description="1・Alle Nachrichten in diesem Ticket werden aufgezeichnet und können für "
                                          "spätere Zwecke wieder abgerufen werden.\n"
                                          "2・Nur das Server-Team darf diese Chats einsehen.\n"
                                          "3・Das Team darf keinerlei Details weitergeben. Sollte es doch geschehen, "
                                          "kann dies mit einem Serverausschluss bestraft werden.",
                              color=discord.Color.embed_background())
        await interaction.response.send_message(embed=embed, ephemeral=True)
