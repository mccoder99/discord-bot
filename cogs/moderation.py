from datetime import datetime, timedelta

import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from discord.utils import basic_autocomplete


async def unban_autocomplete(ctx):
    list_of_bans = await ctx.interaction.guild.bans().flatten()
    banned_user = [f"{x.user}" for x in list_of_bans]
    return banned_user


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="› Kickt einen Spieler vom Server. 👏")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def kick(self, ctx, user: Option(discord.Member, "Welcher User soll gekickt werden?", required=True),
                   grund: Option(str, "Was ist die Begründung?", required=False)):
        if grund is None:
            grund = "Rejoin"

        if user == ctx.author.id:
            return await ctx.respond("Du kannst dich nicht selber kicken!", ephemeral=True)

        await user.kick(reason=grund)
        await ctx.respond(f"Das Mitglied {user.mention} wurde vom Server gekickt!")

    @slash_command(description="› Sperrt einen User vom Server. 📛")
    @discord.default_permissions(ban_members=True)
    @discord.guild_only()
    async def ban(self, ctx, user: Option(discord.Member, "Welcher User soll gesperrt werden?", required=True),
                  grund: Option(str, "Was ist die Begründung?", required=False)):
        if grund is None:
            grund = "Hausverbot"

        if user == ctx.author.id:
            return await ctx.respond("Du kannst dich nicht selber sperren!", ephemeral=True)

        await user.ban(reason=grund)
        await ctx.respond(f"Das Mitglied {user.mention} wurde vom Server ausgeschlossen!")

    @slash_command(description="› Löscht eine bestimmte Anzahl von Nachrichten. ✍")
    @discord.default_permissions(manage_messages=True)
    @discord.guild_only()
    async def clear(self, ctx, anzahl: Option(int, "Wie viele Nachrichten sollen gelöscht werden?", required=True),
                    grund: Option(str, "Was ist die Begründung?", required=False)):
        if grund is None:
            grund = "Löschung erfolgreich"

        if anzahl <= 100:
            with ctx.channel.typing():
                deleted = await ctx.channel.purge(
                    limit=anzahl, reason=grund, after=datetime.utcnow() - timedelta(days=14)
                )
                await ctx.respond(f"{len(deleted)} Nachrichten wurden gelöscht.")
        else:
            await ctx.respond("Das Limit liegt bei 100.", ephemeral=True)

    @slash_command(description="› Entsperrt einen User vom Server. ✅")
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def unban(self, ctx, user: Option(str, "Welcher User soll entsperrt werden?", required=True,
                                            autocomplete=basic_autocomplete(unban_autocomplete)),
                    grund: Option(str, "Was ist die Begründung?", required=False)):
        if grund is None:
            grund = "Sperrung aufgehoben"

        async for ban in ctx.guild.bans():
            if f"{ban.user}" == f"{user}":
                await ctx.guild.unban(ban.user, reason=grund)
                return await ctx.respond(f"Das Mitglied {ban.user.mention} wurde vom Server entsperrt!")
            else:
                continue

        return await ctx.respond("Dein Account ist offensichtlich nicht gesperrt!", ephemeral=True)

    @slash_command()
    @discord.guild_only()
    async def slowmode(self, ctx, channel: Option(discord.TextChannel, "", required=True),
                       delay: Option(int, "", required=True)):
        if delay < 0:
            await ctx.respond("Slowmode delay must be greater than 0!", ephemeral=True)
            return
        await channel.edit(slowmode_delay=delay)
        await ctx.respond(f"Slowmode delay set to {delay} seconds in {channel.mention}")

    @slash_command()
    @discord.guild_only()
    async def lock(self, ctx, channel: Option(discord.TextChannel, "", required=True)):
        role = discord.utils.get(ctx.guild.roles, name="@everyone")
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False
        await channel.set_permissions(role, overwrite=overwrite)
        await ctx.respond(f"{channel.mention} has been locked. Only administrators can send messages now.")

    @slash_command()
    @discord.guild_only()
    async def unlock(self, ctx, channel: Option(discord.TextChannel, "", required=True)):
        role = discord.utils.get(ctx.guild.roles, name="@everyone")
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = True
        await channel.set_permissions(role, overwrite=overwrite)
        await ctx.respond(f"{channel.mention} has been unlocked. Everyone can send messages now.")

    @slash_command()
    @discord.guild_only()
    async def add_role(self, ctx, user: Option(discord.Member, "", required=True),
                       role: Option(discord.Role, "", required=True)):
        await user.add_roles(role)
        await ctx.respond(f"{user.mention} has been given the {role.name} role.")

    @slash_command()
    @discord.guild_only()
    async def remove_role(self, ctx, user: Option(discord.Member, "", required=True),
                          role: Option(discord.Role, "", required=True)):
        await user.remove_roles(role)
        await ctx.respond(f"{user.mention} has been removed from the {role.name} role.")

    @slash_command(description="› Schaltet einen User serverweit stumm. 🔇")
    @discord.default_permissions(moderate_members=True)
    @discord.guild_only()
    async def timeout(self, ctx,
                      user: Option(discord.Member, "Welcher User soll stummgeschaltet werden?", required=True),
                      typ: Option(str, "", choices=["Sekunden", "Minuten", "Stunden", "Tage", "Wochen"], required=True),
                      dauer: Option(int, "", required=True),
                      grund: Option(str, "Was ist die Begründung?", required=False)):
        if grund is None:
            grund = "Fehlverhalten"

        if typ == "Sekunden":
            duration = timedelta(seconds=dauer)
        elif typ == "Minuten":
            duration = timedelta(minutes=dauer)
        elif typ == "Stunden":
            duration = timedelta(hours=dauer)
        elif typ == "Tage":
            duration = timedelta(days=dauer)
        else:
            duration = timedelta(weeks=dauer)

        try:
            await user.timeout_for(duration, reason=grund)
        except discord.Forbidden:
            return await ctx.respond("Ich kann diesen User nicht stummschalten!", ephemeral=True)

        await ctx.respond(f"Das Mitglied {user.mention} wurde erfolgreich stummgeschaltet!")

    @slash_command(description="› Hebt die Stummschaltung eines Users auf. ✅")
    @discord.default_permissions(moderate_members=True)
    @discord.guild_only()
    async def untimeout(self, ctx, user: Option(discord.Member, "", required=True),
                        grund: Option(str, "Was ist die Begründung?", required=False)):
        if grund is None:
            grund = "Stummschaltung aufgehoben"

        try:
            await user.timeout(None, reason=grund)
        except discord.Forbidden:
            return await ctx.respond("Ich kann die Stummschaltung von diesen User nicht aufheben!", ephemeral=True)

        await ctx.respond(f"Die Stummschaltung von {user.mention} wurde erfolgreich aufgehoben!")


def setup(bot):
    bot.add_cog(Moderation(bot))
