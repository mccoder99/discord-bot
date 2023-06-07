import datetime
import random

import aiosqlite
import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "database.db"

    @staticmethod
    def get_level(xp):
        lvl = 0
        amount = 100

        while True:
            xp -= amount
            if xp < 0:
                return lvl
            lvl += 1
            amount += 100

    async def check_user(self, user_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("INSERT OR IGNORE INTO level_system (user_id) VALUES (?)", (user_id,))
            await db.commit()

    async def get_xp(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT xp FROM level_system WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return
        xp = random.randint(10, 20)

        await self.check_user(message.author.id)
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("UPDATE level_system SET msg_count = msg_count + 1, xp = xp + ? WHERE user_id = ?",
                             (xp, message.author.id))
            await db.commit()

        new_xp = await self.get_xp(message.author.id)

        old_level = self.get_level(new_xp - xp)
        new_level = self.get_level(new_xp)

        if old_level == new_level:
            return
        elif new_level == 5:
            role = message.guild.get_role(1096557552571007096)
            await message.author.add_roles(role)
            embed = discord.Embed(
                title="Level Up!",
                description=f"Du hast das Level {new_level} erreicht und die Rolle {role.mention} erhalten!",
                color=discord.Color.embed_background()
            )
            embed.set_thumbnail(url=message.author.avatar.url)
            await message.channel.send(embed=embed)
        elif new_level == 10:
            role = message.guild.get_role(1096557619075878972)
            await message.author.add_roles(role)
            embed = discord.Embed(
                title="Level Up!",
                description=f"Du hast das Level {new_level} erreicht und die Rolle {role.mention} erhalten!",
                color=discord.Color.embed_background()
            )
            embed.set_thumbnail(url=message.author.avatar.url)
            await message.channel.send(embed=embed)
        elif new_level == 15:
            role = message.guild.get_role(1096557617620471818)
            await message.author.add_roles(role)
            embed = discord.Embed(
                title="Level Up!",
                description=f"Du hast das Level {new_level} erreicht und die Rolle {role.mention} erhalten!",
                color=discord.Color.embed_background()
            )
            embed.set_thumbnail(url=message.author.avatar.url)
            await message.channel.send(embed=embed)
        elif new_level == 20:
            role = message.guild.get_role(1096557610192355378)
            await message.author.add_roles(role)
            embed = discord.Embed(
                title="Level Up!",
                description=f"Du hast das Level {new_level} erreicht und die Rolle {role.mention} erhalten!",
                color=discord.Color.embed_background()
            )
            embed.set_thumbnail(url=message.author.avatar.url)
            await message.channel.send(embed=embed)
        elif new_level == 25:
            role = message.guild.get_role(1096557598909661366)
            await message.author.add_roles(role)
            embed = discord.Embed(
                title="Level Up!",
                description=f"Du hast das Level {new_level} erreicht und die Rolle {role.mention} erhalten!",
                color=discord.Color.embed_background()
            )
            embed.set_thumbnail(url=message.author.avatar.url)
            await message.channel.send(embed=embed)
        elif new_level == 30:
            role = message.guild.get_role(1096557595747176508)
            await message.author.add_roles(role)
            embed = discord.Embed(
                title="Level Up!",
                description=f"Du hast das Level {new_level} erreicht und die Rolle {role.mention} erhalten!",
                color=discord.Color.embed_background()
            )
            embed.set_thumbnail(url=message.author.avatar.url)
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Level Up!", description=f"Du hast das Level {new_level} erreicht!",
                                  color=discord.Color.embed_background())
            embed.set_thumbnail(url=message.author.avatar.url)
            await message.channel.send(embed=embed)

    @slash_command(description="› Zeigt den Rang eines bestimmten Users. 🚀")
    async def rank(self, ctx, user: Option(discord.Member, "Schreibe hier den jeweiligen User rein.", required=True)):
        xp = await self.get_xp(user.id)
        lvl = self.get_level(xp)
        background = Editor("images/space.png").resize((800, 250))
        avatar = await load_image_async(user.display_avatar.url)
        circle_avatar = Editor(avatar).resize((200, 200)).circle_image()
        background.paste(circle_avatar, (25, 25))
        big_text = Font.poppins(size=50, variant="bold")
        small_text = Font.poppins(size=30, variant="regular")
        background.text((490, 50), f"{user}", color="white", font=big_text, align="center")
        background.text((490, 125), f"Level: {lvl}          XP: {xp}", color="#00ced1", font=small_text, align="center")
        file = discord.File(fp=background.image_bytes, filename='rank.png')
        return await ctx.respond(file=file)

    @slash_command(description="› Erhalte eine Liste der 10 aktivsten User. 👥")
    async def leaderboard(self, ctx):
        desc = ""
        counter = 1
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute(
                    "SELECT user_id, xp FROM level_system WHERE msg_count > 0 ORDER BY xp DESC LIMIT 10"
            ) as cursor:
                async for user_id, xp in cursor:
                    lvl = self.get_level(xp)
                    desc += f"`{counter}.` <@{user_id}> - **Level {lvl}** - {xp} XP"
                    counter += 1

        embed = discord.Embed(title="Rangliste", description=desc,
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Angefordert von {ctx.author} • {ctx.author.id}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(LevelSystem(bot))
