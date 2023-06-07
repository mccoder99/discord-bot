import datetime

import discord
from discord.commands import slash_command, Option
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="› Lade den Bot  auf deinen Server ein. 🤖")
    @discord.guild_only()
    async def invite(self, ctx):
        await ctx.respond(f"Lade den Bot hier ein: https://discord.com/oauth2/authorize?client_id={self.bot.user.id}"
                          "&permissions=8&scope=bot+applications.commands", ephemeral=True)

    @slash_command(description="› Ändere deinen Nicknamen auf dem Server. 📝")
    @discord.guild_only()
    async def nick(self, ctx, nick: Option(str, "", required=True)):
        try:
            await ctx.author.edit(nick=nick)
        except discord.Forbidden:
            return await ctx.respond(
                "Ich habe keine Berechtigung den Nickname von diesem User zu ändern.", ephemeral=True
            )
        await ctx.respond("Dein Nickname wurde erfolgreich geändert!", ephemeral=True)

    @slash_command(description="› Zeigt die Latenz von diesem Bot. 🔔")
    @discord.guild_only()
    async def ping(self, ctx):
        file = discord.File("images/latency.png", filename="ping.png")
        embed = discord.Embed(title=f"Latenz von {self.bot.user.name}",
                              description=f"Hier siehst du die `Latenz` von `{self.bot.user.name}`!\n\n"
                                          f"Die Latenz beträgt: `{round(self.bot.latency * 1000)}ms`",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_thumbnail(url="attachment://ping.png")
        embed.set_footer(text=f"Ausgeführt von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed, file=file)

    @slash_command(description="› Reiche einen Vorschlag für den Bot ein. 📚")
    @discord.guild_only()
    async def suggest(self, ctx, vorschlag: Option(str, "Schreibe hier deinen Vorschlag rein.", required=True)):
        file = discord.File("images/idea.png", filename="suggest.png")
        embed = discord.Embed(title="Neuer Vorschlag", description=vorschlag,
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_thumbnail(url="attachment://suggest.png")
        embed.set_footer(text=f"Eingereicht von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await self.bot.get_channel(1094659969619603466).send(embed=embed, file=file)
        await ctx.respond("Dein Vorschlag wurde erfolgreich eingereicht!", ephemeral=True)

    @slash_command(description="› Melde einen Bug an das Bot-Team. 📁")
    @discord.guild_only()
    async def report(self, ctx, meldung: Option(str, "Schreibe hier deine Meldung rein.", required=True)):
        file = discord.File("images/report.png", filename="report.png")
        embed = discord.Embed(title="Neue Meldung", description=meldung,
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_thumbnail(url="attachment://report.png")
        embed.set_footer(text=f"Gemeldet von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await self.bot.get_channel(1094659970806599781).send(embed=embed, file=file)
        await ctx.respond("Deine Meldung wurde erfolgreich weitergeleitet!", ephemeral=True)

    @slash_command(description="› Erhalte den Avatar von einem User. 🗽")
    @discord.guild_only()
    async def avatar(self, ctx, user: Option(discord.Member, "Schreibe hier den jeweiligen User rein.", required=True)):
        embed = discord.Embed(title=f"Avatar von {user.name}",
                              description=f"Hier siehst du den `Avatar` von `{user.name}`!",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_image(url=user.avatar.url)
        embed.set_footer(text=f"Angefordert von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @slash_command(description="› Erfahre etwas über einen bestimmten User. 👤", name="userinfo")
    @discord.guild_only()
    async def info(self, ctx, user: Option(discord.Member, "Schreibe hier den jeweiligen User rein.", required=True)):
        embed = discord.Embed(title=f"Userinfo von {user.name}",
                              description=f"Hier siehst du die `Userinfo` von `{user.name}`!",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.add_field(name="Name", value=f"```{user}```", inline=True)
        embed.add_field(name="Bot", value=f"```{'Ja' if user.bot else 'Nein'}```", inline=True)
        embed.add_field(name="Nickname", value=f"```{user.nick if user.nick else 'Nicht gesetzt'}```", inline=True)
        embed.add_field(name="Server betreten",
                        value=f"```{user.joined_at.strftime('%d.%m.%Y, %H:%M:%S')}```", inline=True)
        embed.add_field(name="Discord betreten",
                        value=f"```{user.created_at.strftime('%d.%m.%Y, %H:%M:%S')}```", inline=True)
        embed.add_field(name="Rollen", value=f"```{len(user.roles)-1}```", inline=True)
        embed.add_field(name="Höchste Rolle", value=f"```{user.top_role.name}```", inline=True)
        embed.add_field(name="Farbe", value=f"```{user.color}```", inline=True)
        embed.add_field(name="Booster", value=f"```{'Ja' if user.premium_since else 'Nein'}```", inline=True)
        embed.set_thumbnail(url=user.avatar.url)
        embed.set_footer(text=f"Angefordert von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @slash_command(description="› Zeigt dir Infos über den aktuellen Server. 📟")
    @discord.guild_only()
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=f"Serverinfo für {ctx.guild.name}",
                              description=f"Hier siehst du die `Serverinfo` für `{ctx.guild.name}`!",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.add_field(name="Name", value=f"```{ctx.guild.name}```", inline=True)
        embed.add_field(name="Eigentümer", value=f"```{ctx.guild.owner}```", inline=True)
        embed.add_field(name="Mitglieder", value=f"```{len(ctx.guild.members)}```", inline=True)
        embed.add_field(name="Verifikation", value=f"```{ctx.guild.verification_level}```", inline=True)
        embed.add_field(name="Höchste Rolle", value=f"```{ctx.guild.roles[-1]}```", inline=True)
        embed.add_field(name="Rollen", value=f"```{len(ctx.guild.roles)-1}```", inline=True)
        embed.add_field(name="Bots", value=", ".join(bot.mention for bot in ctx.guild.members if bot.bot), inline=True)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"Angefordert von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
