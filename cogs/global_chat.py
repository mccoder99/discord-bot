import datetime
import json
import os

import discord
from discord.commands import slash_command
from discord.ext import commands

if os.path.isfile("servers.json"):
    with open("servers.json", encoding="utf-8") as f:
        servers = json.load(f)
else:
    servers = {"servers": []}
    with open("servers.json", "w") as f:
        json.dump(servers, f, indent=4)


class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def guild_exists(guild_id):
        for server in servers["servers"]:
            if int(server["guild_id"] == int(guild_id)):
                return True
        return False

    @staticmethod
    def get_global_chat(guild_id, channel_id):
        global_chat = None
        for server in servers["servers"]:
            if int(server["guild_id"]) == int(guild_id):
                if channel_id:
                    if int(server["channel_id"]) == int(channel_id):
                        global_chat = server
                else:
                    global_chat = server
        return global_chat

    @staticmethod
    def get_global_chat_id(guild_id):
        global_chat = -1
        i = 0
        for server in servers["servers"]:
            if int(server["guild_id"]) == int(guild_id):
                global_chat = i
            i += 1
        return global_chat

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.get_global_chat(message.guild.id, message.channel.id):
            await self.send_all(message)

    async def send_all(self, message):
        for server in servers["servers"]:
            guild = self.bot.get_guild(int(server["guild_id"]))
            if guild:
                channel = guild.get_channel(int(server["channel_id"]))
                if channel:
                    perms = channel.permissions_for(guild.me)
                    if perms.send_messages:
                        if perms.embed_links and perms.attach_files and perms.external_emojis:
                            if message.author.id == 307534389808463872:
                                author_field_name = "Global-Admin"
                                color = discord.Color.red()
                                file = discord.File("images/koenig.png", filename="admin.png")
                                filename = "admin.png"
                            elif message.author.id == 0:
                                author_field_name = "Global-Moderator"
                                color = discord.Color.blue()
                                file = discord.File("images/polizist.png", filename="moderator.png")
                                filename = "moderator.png"
                            elif message.author.id == 0:
                                author_field_name = "Entwickler (Team)"
                                color = discord.Color.teal()
                                file = discord.File("images/gamer.png", filename="developer.png")
                                filename = "developer.png"
                            elif message.author == message.guild.owner:
                                author_field_name = "Server-Besitzer (Aktuell. Server)"
                                color = discord.Color.orange()
                                file = discord.File("images/vermieter.png", filename="owner.png")
                                filename = "owner.png"
                            else:
                                author_field_name = ""
                                color = discord.Color.greyple()
                                file = discord.File("images/mann.png", filename="user.png")
                                filename = "user.png"

                            embed = discord.Embed(title=message.author.display_name, description=message.content,
                                                  timestamp=datetime.datetime.utcnow(), color=color)
                            embed.set_author(name=author_field_name, icon_url=f"attachment://{filename}")
                            embed.set_thumbnail(url=message.author.display_avatar.url)

                            if message.guild.icon.url:
                                embed.set_footer(text=f"{message.guild.name} • {message.guild.id}",
                                                 icon_url=message.guild.icon.url)
                            else:
                                embed.set_footer(text=f"{message.guild.name} • {message.guild.id}")

                            if message.guild.id == 1094746240253710457:
                                serverinvite = " ⋄ [`📍`Server-Invite](https://discord.gg/bh872TvURQ)"
                            else:
                                serverinvite = " "
                            links = "[`🤖`Bot-Invite](https://discord.com/oauth2/authorize?client_id=" \
                                    f"{self.bot.user.id}&permissions=8&scope=bot+applications.commands)" \
                                    " ⋄ [`🚑`Support-Server](https://discord.gg/z9PeYSMHBm)"
                            links += serverinvite
                            embed.add_field(name=" ", value=links, inline=False)
                            await channel.send(embed=embed, file=file)
        await message.delete()

    @slash_command()
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def add_global(self, ctx):
        if not self.guild_exists(ctx.guild.id):
            embed1 = discord.Embed(
                title="<a:noice:814768549720883210> Neuer Server",
                description=f"Der Server `{ctx.guild.name}` ist dem GlobalChat beigetreten <a:Chat:803676134092308551>"
            )
            for server in servers["servers"]:
                guild = self.bot.get_guild(int(server["guild_id"]))
                if guild:
                    channel = guild.get_channel(int(server["channel_id"]))
                    if channel:
                        perms = channel.permissions_for(guild.me)
                        if perms.send_messages:
                            if perms.embed_links and perms.attach_files and perms.external_emojis:
                                await channel.send(embed=embed1)

            server = {"guild_id": ctx.guild.id, "guild_name": ctx.guild.name, "channel_id": ctx.channel.id}
            servers["servers"].append(server)
            with open("servers.json", "w") as file:
                json.dump(servers, file, indent=4)
            await ctx.channel.edit(topic="Willkommen im Global-Chat", slowmode_delay=5)

            embed2 = discord.Embed(title="Willkommen im Global-Chat",
                                   description="Dein Server ist einsatzbereit!\n"
                                               "Ab jetzt werden alle Nachrichten in diesem Channel direkt an alle"
                                               " anderen Server weitergeleitet!",
                                   color=discord.Color.embed_background())
            embed2.set_thumbnail(url=self.bot.user.avatar.url)
            embed2.set_footer(text="Bitte beachte, dass im Global-Chat stets ein Slowmode von mindestens 5 Sekunden "
                                   "gesetzt sein sollte.")
            await ctx.respond(embed=embed2)

        else:
            embed = discord.Embed(description="Du hast bereits einen Global-Chat auf deinem Server.\r\n"
                                              "Bitte beachte, dass jeder Server nur einen Global-Chat besitzen kann.",
                                  color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)

    @slash_command()
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def remove_global(self, ctx):
        if self.guild_exists(ctx.guild.id):
            global_id = self.get_global_chat_id(ctx.guild.id)
            if global_id != -1:
                servers["servers"].pop(global_id)
                with open("servers.json", "w") as file:
                    json.dump(servers, file, indent=4)
            embed = discord.Embed(title="Auf Wiedersehen",
                                  description="Der Global-Chat wurde entfernt. Du kannst ihn jederzeit mit"
                                              " `/add_global` neu hinzufügen",
                                  color=discord.Color.embed_background())
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(description="Du hast noch keinen Global-Chat auf deinem Server.\r\n"
                                              "Füge einen mit `/add_global` in einem frischen Channel hinzu.",
                                  color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(GlobalChat(bot))
