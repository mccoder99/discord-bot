import datetime
import random

import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mention in message.content:
            await message.channel.send("🌟 | **BUDDY ON TOP** - (*Mein Prefix: `/`*)")
        else:
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome = [
            f"**<a:buddy_beigetreten:1094674894719037541> | {member.mention} ist der Gruppe beigetreten.**",
            f"**<a:buddy_beigetreten:1094674894719037541> | Ein wildes {member.mention} erscheint!**",
            f"**<a:buddy_beigetreten:1094674894719037541> | {member.mention} ist gelandet.**",
            f"**<a:buddy_beigetreten:1094674894719037541> | Willkommen, {member.mention}! Sag hallo!**",
            f"**<a:buddy_beigetreten:1094674894719037541> | {member.mention} ist auf den Server gehüpft.**",
            f"**<a:buddy_beigetreten:1094674894719037541> | Juhu, du hast es geschafft, {member.mention}!**",
            f"**<a:buddy_beigetreten:1094674894719037541> | {member.mention} ist gerade auf den Server geschlittert.**",
            f"**<a:buddy_beigetreten:1094674894719037541> | Heißen wir {member.mention} herzlich willkommen!**",
            f"**<a:buddy_beigetreten:1094674894719037541> | {member.mention} ist gerade aufgetaucht!**",
            f"**<a:buddy_beigetreten:1094674894719037541> | Schön, dich zu sehen, {member.mention}.**"
        ]
        await self.bot.get_channel(1094659967669248070).send(random.choice(welcome))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(title="Bot hinzugefügt",
                              description=f"Ein Server hat `{self.bot.user.name}` hinzugefügt!",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        embed.add_field(name="Weitere Informationen",
                        value=f"Server-Name: `{guild.name}`\nServer-ID: `{guild.id}`\nEigentümer: `{guild.owner}`\n"
                              f"Mitglieder: `{len(guild.members)}`", inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await self.bot.get_channel(1094659987105652827).send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(title="Bot entfernt",
                              description=f"Ein Server hat `{self.bot.user.name}` entfernt!",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed.add_field(name="Weitere Informationen",
                        value=f"Server-Name: `{guild.name}`\nServer-ID: `{guild.id}`\nEigentümer: `{guild.owner}`\n"
                              f"Mitglieder: `{len(guild.members)}`", inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await self.bot.get_channel(1094659988158418964).send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
