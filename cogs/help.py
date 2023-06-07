import datetime

import discord
import ezcord
from discord.commands import slash_command
from discord.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="› Zeigt dir alle Befehle für diesen Bot. 📂")
    async def help(self, ctx):
        embed = discord.Embed(title="🌟 🗴 Buddy - Hilfe",
                              description="› Dieser Bot hat sehr **viele Features**, "
                                          "von allgemeinen Befehlen bis zu einem Radio ist alles dabei.\n"
                                          "`🚑` › Melde dich bei Fragen auf dem "
                                          "**[Support Server](https://discord.gg/z9PeYSMHBm)**.\n\n",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Angefragt von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed, view=HelpView(), ephemeral=True)


def setup(bot):
    bot.add_cog(HelpCommand(bot))


class HelpView(ezcord.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [discord.SelectOption(label="🗴 ALLGEMEINE BEFEHLE", value="general",
                                    description="› Hier siehst du allgemeine Befehle. 🔨", emoji="🔨"),
               discord.SelectOption(label="🗴 FUN-BEFEHLE", value="fun",
                                    description="› Hier siehst du alle Fun-Befehle. 😎", emoji="😎"),
               discord.SelectOption(label="🗴 MODERATION", value="moderation",
                                    description="› Schaue dir alle Moderation-Features an. 🚔", emoji="🚔"),
               discord.SelectOption(label="🗴 ECONOMY BEFEHLE", value="economy",
                                    description="› Hier siehst du Economy Befehle. 💰", emoji="💰"),
               discord.SelectOption(label="🗴 TICKET-SUPPORT", value="ticket_support",
                                    description="› Hier siehst du alle Ticket-Befehle. ❓", emoji="❓"),
               discord.SelectOption(label="🗴 LEVELSYSTEM", value="level_system",
                                    description="› Schaue dir alle Level-Features an. ✨", emoji="✨"),
               discord.SelectOption(label="🗴 RADIO BEFEHLE", value="radio",
                                    description="› Hier siehst du Radio Befehle. 📻", emoji="📻"),
               discord.SelectOption(label="🗴 GLOBAL-CHAT", value="global_chat",
                                    description="› Hier siehst du alle Global-Befehle. 🌍", emoji="🌍")]

    @discord.ui.select(placeholder="📚 | Wähle eine Kategorie!", min_values=1, max_values=1, options=options)
    async def select_callback(self, select, interaction):
        if "general" in select.values:
            file = discord.File("images/book.png", filename="general.png")
            embed = discord.Embed(title="🔨 🗴 Allgemeine Befehle (Kategorie) - Hilfe",
                                  description="› Hier findest du **allgemeine Bot-Befehle**, "
                                              "welche sich auf grundlegende Dinge (wie den Bot-Invite) beschränken.\n"
                                              "`🚑` › Melde dich bei Fragen auf dem "
                                              "**[Support Server](https://discord.gg/z9PeYSMHBm)**.\n\n"
                                              "> `🔔` - `/ping`\n› Zeigt die Latenz von diesem Bot.\n\n"
                                              "> `📚` - `/suggest <VORSCHLAG>`"
                                              "\n› Reiche einen Vorschlag für den Bot ein.\n\n"
                                              "> `📁` - `/report <MELDUNG>`\n› Melde einen Bug an das Bot-Team.\n\n"
                                              "> `🗽` - `/avatar <USER>`\n› Erhalte den Avatar von einem User.\n\n"
                                              "> `👤` - `/userinfo <USER>`"
                                              "\n› Erfahre etwas über einen bestimmten User.\n\n"
                                              "> `📟` - `/serverinfo`\n› Zeigt dir Infos über den aktuellen Server.\n\n"
                                              "**Das waren alle allgemeinen Befehle für diesen Bot.**",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
            embed.set_thumbnail(url="attachment://general.png")
            embed.set_footer(text=f"Angefragt von {interaction.user} • {interaction.user.id}",
                             icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, file=file)
        if "fun" in select.values:
            file = discord.File("images/laugh.png", filename="fun.png")
            embed = discord.Embed(title="😎 🗴 Fun-Befehle (Kategorie) - Hilfe",
                                  description="› Hier findest du alle unterhaltsamen **Fun-Befehle**, "
                                              "welche jederzeit zum Spaß verwendet werden können.\n\n"
                                              "`🚑` › Melde dich bei Fragen auf dem "
                                              "**[Support Server](https://discord.gg/z9PeYSMHBm)**.\n"
                                              "`📌` › Du musst bei jedem Befehl einen User **erwähnen!**\n\n"
                                              "> `🤗` - `/hug`\n› Umarme einen User den du magst.\n\n"
                                              "> `🥊` - `/slap`\n› Schlage einen User den du nicht magst.\n\n"
                                              "> `😘` - `/kiss`\n› Küsse einen User den du liebst.\n\n"
                                              "> `🔪` - `/kill`\n› Töte einen User den du hasst.\n\n"
                                              "> `🔮` - `/magicball <FRAGE>`"
                                              "\n› Stelle dem Bot eine Frage und er wird dir antworten.\n\n"
                                              "**Das waren alle Fun-Befehle für diesen Bot.**",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
            embed.set_thumbnail(url="attachment://fun.png")
            embed.set_footer(text=f"Angefragt von {interaction.user} • {interaction.user.id}",
                             icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, file=file)
        if "moderation" in select.values:
            file = discord.File("images/settings.png", filename="moderation.png")
            embed = discord.Embed(title="🚔 🗴 Moderation (Kategorie) - Hilfe",
                                  description="› Hier siehst du ein paar **Moderations-Features**, "
                                              "welche du verwenden kannst um deinen Server zu moderieren.\n\n"
                                              "`🚑` › Melde dich bei Fragen auf dem "
                                              "**[Support Server](https://discord.gg/z9PeYSMHBm)**.\n"
                                              "`📌` › Du musst bei jedem Befehl eine **Begründung** angeben!\n\n"
                                              "> `👏` - `/kick <USER>`\n› Kickt einen Spieler vom Server.\n\n"
                                              "> `📛` - `/ban <USER>`\n› Sperrt einen User vom Server.\n\n"
                                              "> `✍` - `/clear <ANZAHL>`"
                                              "\n› Löscht eine bestimmte Anzahl von Nachrichten.\n\n"
                                              "> `✅` - `/unban <USER>`\n› Entsperrt einen User vom Server.\n\n"
                                              "**Das waren alle Moderations-Features für diesen Bot.**",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
            embed.set_thumbnail(url="attachment://moderation.png")
            embed.set_footer(text=f"Angefragt von {interaction.user} • {interaction.user.id}",
                             icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, file=file)
        if "economy" in select.values:
            await interaction.response.send_message(
                "👷‍♂️ | Die Hilfe für die Economy Befehle ist momentan in Wartungen!", ephemeral=True
            )
        if "level_system" in select.values:
            file = discord.File("images/level-up.png", filename="level_system.png")
            embed = discord.Embed(title="✨ 🗴 Levelsystem (Kategorie) - Hilfe",
                                  description="› Hier siehst du ein paar **Level-Features**, "
                                              "welche du verwenden kannst um dein Level abzurufen.\n"
                                              "`🚑` › Melde dich bei Fragen auf dem "
                                              "**[Support Server](https://discord.gg/z9PeYSMHBm)**.\n\n"
                                              "> `🚀` - `/rank <USER>`\n› Zeigt den Rang eines bestimmten Users.\n\n"
                                              "> `👥` - `/leaderboard`\n› Erhalte eine Liste der 10 aktivsten User.\n\n"
                                              "**Das waren alle Level-Features für diesen Bot.**",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
            embed.set_thumbnail(url="attachment://level_system.png")
            embed.set_footer(text=f"Angefragt von {interaction.user} • {interaction.user.id}",
                             icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, file=file)
        if "ticket_support" in select.values:
            file = discord.File("images/ticket.png", filename="ticket_support.png")
            embed = discord.Embed(title="❓ 🗴 Ticket-Support (Kategorie) - Hilfe",
                                  description="› Hier findest du alle hilfreichen **Ticket-Befehle**, "
                                              "welche jederzeit verwendet werden können wenn du Hilfe brauchst.\n"
                                              "`🚑` › Melde dich bei Fragen auf dem "
                                              "**[Support Server](https://discord.gg/z9PeYSMHBm)**.\n"
                                              "`📌` › Du musst für jeden Befehl **Administrator** sein!\n\n"
                                              "> `➕` - `/ticket guild`\n› Fügt deinen Server zur Datenbank hinzu.\n\n"
                                              "> `🎫` - `/ticket send`\n› Sendet das Ticket-Panel in den Kanal.\n\n"
                                              "**Das waren alle Ticket-Befehle für diesen Bot.**",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
            embed.set_thumbnail(url="attachment://ticket_support.png")
            embed.set_footer(text=f"Angefragt von {interaction.user} • {interaction.user.id}",
                             icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, file=file)
        if "radio" in select.values:
            file = discord.File("images/radio.png", filename="radio.png")
            embed = discord.Embed(title="📻 🗴 Radio Befehle (Kategorie) - Hilfe",
                                  description="› Hier findest du **Radio Befehle**, "
                                              "welche du verwenden kannst um Radio zu spielen.\n"
                                              "`🚑` › Melde dich bei Fragen auf dem "
                                              "**[Support Server](https://discord.gg/z9PeYSMHBm)**.\n\n"
                                              "**Das waren alle Radio Befehle für diesen Bot.**",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
            embed.set_thumbnail(url="attachment://radio.png")
            embed.set_footer(text=f"Angefragt von {interaction.user} • {interaction.user.id}",
                             icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, file=file)
        if "global_chat" in select.values:
            await interaction.response.send_message("👷‍♂️ | Die Hilfe für den Global-Chat ist momentan in Wartungen!",
                                                    ephemeral=True)
