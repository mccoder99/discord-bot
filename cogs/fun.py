import datetime
import os
import random

import asyncpraw
import discord
import requests
from discord.commands import slash_command, Option
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def gif(self, ctx, search: Option(str, "", required=True)):
        key = os.getenv("API_KEY")
        params = {"q": search, "key": key, "limit": "10", "client_key": "discord_bot", "media_filter": "gif"}
        result = requests.get("https://tenor.googleapis.com/v2/search", params=params)
        data = result.json()
        number = random.randint(0, 9)
        url = data['results'][number]['media_formats']['gif']['url']
        await ctx.respond(url)

    @slash_command()
    async def meme(self, ctx):
        await ctx.defer()

        async with asyncpraw.Reddit(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"),
                                    username="mccoder99", password=os.getenv("PASSWORD"), user_agent="") as reddit:
            subreddit = await reddit.subreddit(random.choice(["dankmemes", "ich_iel", "ProgrammerHumor"]))
            hot = subreddit.hot(limit=25)

            all_posts = []
            async for post in hot:
                if not post.is_video:
                    all_posts.append(post)

            random_post = random.choice(all_posts)

            embed = discord.Embed(title=random_post.title)
            embed.set_image(url=random_post.url)
            await ctx.respond(embed=embed)

    # cat
    # dog
    # joke
    # quote
    # trivia

    @slash_command()
    async def say(self, ctx, text: Option(str, "", required=True)):
        await ctx.respond(text)

    @slash_command()
    async def roll(self, ctx):
        number = random.randint(1, 6)
        await ctx.respond(f"Du hast eine {number} gewürfelt!")

    # weather

    @slash_command(description="› Umarme einen User den du magst. 🤗")
    async def hug(self, ctx, user: Option(discord.Member, "Schreibe hier den jeweiligen User rein.", required=True)):
        key = os.getenv("API_KEY")
        params = {"q": "hug", "key": key, "limit": "10", "client_key": "discord_bot", "media_filter": "gif"}
        result = requests.get("https://tenor.googleapis.com/v2/search", params=params)
        data = result.json()
        number = random.randint(0, 9)
        url = data['results'][number]['media_formats']['gif']['url']

        embed = discord.Embed(description=f"**{ctx.author.display_name}** hat **{user.display_name}** umarmt. "
                                          "Einfach süß die Beiden!",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_author(name=f"{ctx.author.name} umarmt jemanden",
                         icon_url="https://cdn-icons-png.flaticon.com/512/2374/2374691.png")
        embed.set_image(url=url)
        embed.set_footer(text=f"Umarmt von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @slash_command(description="› Schlage einen User den du nicht magst. 🥊")
    async def slap(self, ctx, user: Option(discord.Member, "Schreibe hier den jeweiligen User rein.", required=True)):
        key = os.getenv("API_KEY")
        params = {"q": "slap", "key": key, "limit": "10", "client_key": "discord_bot", "media_filter": "gif"}
        result = requests.get("https://tenor.googleapis.com/v2/search", params=params)
        data = result.json()
        number = random.randint(0, 9)
        url = data['results'][number]['media_formats']['gif']['url']

        embed = discord.Embed(description=f"**{ctx.author.display_name}** hat **{user.display_name}** geschlagen. "
                                          "Spüre ich da eine gewisse Spannung?",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_author(name=f"{ctx.author.name} schlägt jemanden",
                         icon_url="https://cdn-icons-png.flaticon.com/512/4544/4544237.png")
        embed.set_image(url=url)
        embed.set_footer(text=f"Geschlagen von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @slash_command(description="› Küsse einen User den du liebst. 😘")
    async def kiss(self, ctx, user: Option(discord.Member, "Schreibe hier den jeweiligen User rein.", required=True)):
        key = os.getenv("API_KEY")
        params = {"q": "kiss", "key": key, "limit": "10", "client_key": "discord_bot", "media_filter": "gif"}
        result = requests.get("https://tenor.googleapis.com/v2/search", params=params)
        data = result.json()
        number = random.randint(0, 9)
        url = data['results'][number]['media_formats']['gif']['url']

        embed = discord.Embed(description=f"**{ctx.author.display_name}** hat **{user.display_name}** geküsst. "
                                          "Klingeln da etwa die Hochzeitsglocken?",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_author(name=f"{ctx.author.name} küsst jemanden",
                         icon_url="https://cdn-icons-png.flaticon.com/512/2454/2454267.png")
        embed.set_image(url=url)
        embed.set_footer(text=f"Geküsst von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @slash_command(description="› Töte einen User den du hasst. 🔪")
    async def kill(self, ctx, user: Option(discord.Member, "Schreibe hier den jeweiligen User rein.", required=True)):
        key = os.getenv("API_KEY")
        params = {"q": "kill", "key": key, "limit": "10", "client_key": "discord_bot", "media_filter": "gif"}
        result = requests.get("https://tenor.googleapis.com/v2/search", params=params)
        data = result.json()
        number = random.randint(0, 9)
        url = data['results'][number]['media_formats']['gif']['url']

        embed = discord.Embed(description=f"**{ctx.author.display_name}** hat **{user.display_name}** getötet. "
                                          "Ruft die Polizei!",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_author(name=f"{ctx.author.name} tötet jemanden",
                         icon_url="https://cdn-icons-png.flaticon.com/512/6010/6010029.png")
        embed.set_image(url=url)
        embed.set_footer(text=f"Getötet von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @slash_command(description="› Stelle dem Bot eine Frage und er wird dir antworten. 🔮")
    async def magicball(self, ctx, frage: Option(str, "Schreibe hier deine Frage rein.", required=True)):
        antworten = ["Ja", "Nein", "Vielleicht", "Wahrscheinlich schon", "Eher nicht"]
        await ctx.respond(f"{frage} - {random.choice(antworten)}")


def setup(bot):
    bot.add_cog(Fun(bot))
