import datetime

import aiosqlite
import discord
from discord.commands import slash_command, Option
from discord.ext import commands


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "database.db"

    async def get_channel(self, guild_id):
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT channel_id FROM logging WHERE guild_id = ?", (guild_id,)) as cursor:
                result = await cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    async def set_channel(self, guild_id, channel_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "REPLACE  INTO logging (guild_id, channel_id) VALUES (?, ?)", (guild_id, channel_id)
            )
            await db.commit()

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        message = payload.cached_message

        channel_id = await self.get_channel(payload.guild_id)
        channel = self.bot.get_channel(channel_id)

        if channel is None:
            return
        elif message.author.bot:
            return
        else:
            embed = discord.Embed(title="Nachricht gelöscht",
                                  description=f"Eine Nachricht auf `{message.guild.name}` wurde gelöscht.",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Weitere Informationen",
                            value=f"Verfasser: {message.author}\nNachricht: {message.content}", inline=True)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        message = payload.cached_message

        channel_id = await self.get_channel(payload.guild_id)
        channel = self.bot.get_channel(channel_id)

        if channel is None:
            return
        elif message.author.bot:
            return
        else:
            embed = discord.Embed(title="Nachricht bearbeitet",
                                  description=f"Eine Nachricht auf `{message.guild.name}` wurde bearbeitet.",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.yellow())
            embed.add_field(name="Weitere Informationen",
                            value=f"Verfasser: {message.author}\nNachricht: {message.content}", inline=True)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            await channel.send(embed=embed)

    @slash_command()
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def set_log(self, ctx, channel: Option(discord.TextChannel, "", required=True)):
        await self.set_channel(ctx.guild.id, channel.id)
        await ctx.respond(f"{channel.mention} wurde als Log-Channel festgelegt.", ephemeral=True)


def setup(bot):
    bot.add_cog(Logging(bot))
