import discord
from discord.commands import slash_command, Option
from discord.ext import commands


class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Starte das Radio")
    @discord.guild_only()
    async def play(self, ctx, radio: Option(str, "Wähle einen Radiosender aus.", required=True,
                                            choices=["I Love Radio", "I Love 2 Dance", "Hip Hop", "Radio Rock",
                                                     "Mashup", "Deutschrap", "The Beach", "X-Mas", "Top 100 Charts",
                                                     "Music & Chill", "Sonstiges"]),
                   url: Option(str, "Gebe einen Stream-Link an.", required=False)):
        await ctx.defer(ephemeral=True)

        if radio == "I Love Radio":
            url = "https://streams.ilovemusic.de/iloveradio1.mp3"
        elif radio == "I Love 2 Dance":
            url = "https://streams.ilovemusic.de/iloveradio2.mp3"
        elif radio == "Hip Hop":
            url = "https://streams.ilovemusic.de/iloveradio3.mp3"
        elif radio == "Radio Rock":
            url = "https://streams.ilovemusic.de/iloveradio4.mp3"
        elif radio == "Mashup":
            url = "https://streams.ilovemusic.de/iloveradio5.mp3"
        elif radio == "Deutschrap":
            url = "https://streams.ilovemusic.de/iloveradio6.mp3"
        elif radio == "The Beach":
            url = "https://streams.ilovemusic.de/iloveradio7.mp3"
        elif radio == "X-Mas":
            url = "https://streams.ilovemusic.de/iloveradio8.mp3"
        elif radio == "Top 100 Charts":
            url = "https://streams.ilovemusic.de/iloveradio9.mp3"
        elif radio == "Music & Chill":
            url = "https://streams.ilovemusic.de/iloveradio10.mp3"
        else:
            url = url

        if radio == "Sonstiges":
            if url is None:
                return await ctx.respond("Du musst einen gültigen Link angeben!", ephemeral=True)

        if ctx.author.voice is None:
            embed = discord.Embed(description="Du musst erst einem Voice Channel beitreten.", color=discord.Color.red())
            return await ctx.respond(embed=embed, ephemeral=True)

        if not ctx.author.voice.channel.permissions_for(ctx.guild.me).connect:
            embed = discord.Embed(
                description="Ich habe keine Rechte, um deinem Channel beizutreten.", color=discord.Color.red()
            )
            return await ctx.respond(embed=embed, ephemeral=True)

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        ctx.voice_client.play(discord.FFmpegPCMAudio(url))
        await ctx.respond("Das Radio wurde gestartet", ephemeral=True)

    @slash_command(description="Stoppe das Radio")
    @discord.guild_only()
    async def leave(self, ctx):
        if ctx.voice_client is None:
            embed = discord.Embed(description="Ich bin mit keinem Voice Channel verbunden.", color=discord.Color.red())
            return await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.voice_client.disconnect()
            await ctx.respond("Bis bald", ephemeral=True)


def setup(bot):
    bot.add_cog(Radio(bot))
