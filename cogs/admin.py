import datetime
import os
import random
import sys

import discord
from discord.commands import slash_command, Option
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @discord.ext.commands.is_owner()
    @discord.guild_only()
    async def activity(self, ctx,
                       typ: Option(str, "", required=True, choices=["playing", "watching", "listening", "streaming"]),
                       status: Option(str, "", required=True, choices=["online", "idle", "dnd"]),
                       name: Option(str, "", required=True)):
        if typ == "playing":
            activity = discord.Game(name=name)
        elif typ == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=name)
        elif typ == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=name)
        else:
            activity = discord.Streaming(name=name, url="https://youtu.be/dQw4w9WgXcQ")

        if status == "online":
            status = discord.Status.online
        elif status == "idle":
            status = discord.Status.idle
        else:
            status = discord.Status.dnd

        await self.bot.change_presence(activity=activity, status=status)
        await ctx.respond("Der Status wurde geändert.", ephemeral=True)

    @activity.error
    async def activity_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Du bist nicht mein Entwickler!", ephemeral=True)

    @slash_command()
    @discord.ext.commands.is_owner()
    @discord.guild_only()
    async def geninvite(self, ctx, server_id: Option(description="", required=True)):
        server = self.bot.get_guild(int(server_id))
        invite = await random.choice(server.text_channels).create_invite(max_uses=1, unique=False)
        await ctx.respond(f"Invite für **{server.name}** ({server.id})\n{invite.url}", ephemeral=True)

    @geninvite.error
    async def geninvite_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Du bist nicht mein Entwickler!", ephemeral=True)

    @slash_command()
    @discord.ext.commands.is_owner()
    @discord.guild_only()
    async def allserver(self, ctx):
        msg = "```js\n"
        msg += "{!s:19s} | {!s:>5s} | {} | {}\n".format("ID", "Member", "Name", "Owner")
        for guild in self.bot.guilds:
            msg += "{!s:19s} | {!s:>5s}| {} | {}\n".format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += "```"
        await ctx.respond(msg, ephemeral=True)

    @allserver.error
    async def allserver_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Du bist nicht mein Entwickler!", ephemeral=True)

    @slash_command()
    @discord.ext.commands.is_owner()
    @discord.guild_only()
    async def leaveguild(self, ctx, server_id: Option(description="", required=True)):
        guild = self.bot.get_guild(int(server_id))
        await guild.leave()
        await ctx.respond(f"Ich habe den Server `{guild.name}` verlassen!", ephemeral=True)

    @leaveguild.error
    async def leaveguild_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Du bist nicht mein Entwickler!", ephemeral=True)

    @slash_command(description="")
    @discord.ext.commands.is_owner()
    @discord.guild_only()
    async def shutdown(self, ctx):
        embed = discord.Embed(title="Herunterfahren", description="Der Bot wurde erfolgreich heruntergefahren!",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Heruntergefahren von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

        os.execv(sys.executable, ["python"] + sys.argv)

    @shutdown.error
    async def shutdown_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Du bist nicht mein Entwickler!", ephemeral=True)


def setup(bot):
    bot.add_cog(Admin(bot))
