import random

import aiosqlite
import discord
from discord.commands import slash_command, Option
from discord.ext import commands


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "database.db"

    async def check_user(self, user_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("INSERT OR IGNORE INTO economy (user_id) VALUES (?)", (user_id,))
            await db.commit()

    async def get_bank(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT bank FROM economy WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    async def get_cash(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT cash FROM economy WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    @slash_command(description="")
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def add_money(self, ctx, user: Option(discord.Member, "", required=True),
                        anzahl: Option(int, "", required=True)):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("UPDATE economy SET bank = bank + ? WHERE user_id = ?", (anzahl, user.id))
            await db.commit()

        embed = discord.Embed(description=f"{user.mention} hat {anzahl} Diamanten erhalten!")
        await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(description="")
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def remove_money(self, ctx, user: Option(discord.Member, "", required=True),
                           anzahl: Option(int, "", required=True)):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("UPDATE economy SET bank = bank - ? WHERE user_id = ?", (anzahl, user.id))
            await db.commit()

        embed = discord.Embed(description=f"{user.mention} wurden {anzahl} Diamanten entfernt!")
        await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(description="")
    @discord.guild_only()
    async def balance(self, ctx, user: Option(discord.Member, "", required=True)):
        bank = await self.get_bank(user.id)
        cash = await self.get_cash(user.id)
        total = bank + cash

        embed = discord.Embed(title="Kontostand", description=f"Hier siehst du den Kontostand von {user.mention}")
        embed.add_field(name="Cash", value=f"💎 {cash}", inline=True)
        embed.add_field(name="Bank", value=f"💎 {bank}", inline=True)
        embed.add_field(name="Total", value=f"💎 {total}", inline=True)
        await ctx.respond(embed=embed)

    @slash_command(description="")
    @discord.guild_only()
    async def deposit(self, ctx, anzahl: Option(int, "", required=True)):
        bank = await self.get_bank(ctx.author.id)
        cash = await self.get_cash(ctx.author.id)

        if anzahl > cash:
            embed = discord.Embed(description="Du hast nicht so viel Geld.", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            bank += anzahl
            cash -= anzahl

            async with aiosqlite.connect(self.DB) as db:
                await db.execute("UPDATE economy SET bank = ?, cash = ? WHERE user_id = ?", (bank, cash, ctx.author.id))
                await db.commit()

            embed = discord.Embed(description=f"Du hast erfolgreich 💎 {anzahl} Diamanten eingezahlt.",
                                  color=discord.Color.green())
            await ctx.respond(embed=embed)

    @slash_command(description="")
    @discord.guild_only()
    async def work(self, ctx):
        if random.randint(1, 100) > 40:
            coins = random.randint(20, 80)
            positive = [f"Du hast gut gearbeitet und erhältst 💎 **{coins}** Diamanten!",
                        f"Du hast einen Kuchen gebacken und erhältst 💎 **{coins}** Diamanten!",
                        "Du hast ein paar Kekse gebacken und jemand hat sie gekauft. "
                        f"Er/Sie bezahlte 💎 **{coins}** Diamanten!",
                        f"Du hast ein paar Autos gewaschen und erhältst 💎 **{coins}** Diamanten!",
                        f"Du hast ein paar Codes verkauft und verdienst 💎 **{coins}** Diamanten!",
                        "Sie arbeiten heute hart im Büro, aber anstatt befördert zu werden, "
                        f"verdienen Sie 💎 **{coins}** Diamanten! Schön.",
                        f"Unser Chef war heute nett und hat dir 💎 **{coins}** Diamanten geschenkt!",
                        "Du hast eine gute Note, also hat deine Mutter beschlossen, "
                        f"dir 💎 **{coins}** Diamanten zu geben!",
                        f"Jemand hat 💎 **{coins}** Diamanten in deinem Livestream gespendet! Gut gemacht.",
                        f"Du hast einige Items verkauft und 💎 **{coins}** Diamanten verdient!",
                        f"Du arbeitest als Bauer und verdienst 💎 **{coins}** Diamanten!",
                        "Du fängst einen Fisch und gibst ihn deinem besten Freund. "
                        f"Er zahlt dir 💎 **{coins}** Diamanten für einen guten Job!",
                        "Du arbeitest in einem Restaurant und hast ein Trinkgeld von "
                        f"💎 **{coins}** Diamanten für einen guten Job bekommen!",
                        f"Du gewinnst einen Burger-Wettessen. Der Preis sind 💎 **{coins}** Diamanten!",
                        f"Du arbeitest als Polizist und verdienst 💎 **{coins}** Diamanten!"]
            desc = random.choice(positive)
            embed = discord.Embed(description=desc, color=discord.Color.green())

            async with aiosqlite.connect(self.DB) as db:
                await db.execute("UPDATE economy SET cash = cash + ? WHERE user_id = ?", (coins, ctx.author.id))
                await db.commit()

            await ctx.respond(embed=embed)
        else:
            coins = random.randint(10, 70)
            negative = [f"Du hast schlecht gearbeitet und verlierst 💎 **{coins}** Diamanten!"]
            desc = random.choice(negative)
            embed = discord.Embed(description=desc, color=discord.Color.red())

            async with aiosqlite.connect(self.DB) as db:
                await db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?", (coins, ctx.author.id))
                await db.commit()

            await ctx.respond(embed=embed)

    @slash_command(description="")
    @discord.guild_only()
    async def slut(self, ctx):
        if random.randint(1, 100) > 60:
            coins = random.randint(20, 80)
            positive = [f"Du hast einen guten Job gemacht und verdienst 💎 **{coins}** Diamanten!"]
            embed = discord.Embed(description=random.choice(positive), color=discord.Color.green())

            async with aiosqlite.connect(self.DB) as db:
                await db.execute("UPDATE economy SET cash = cash + ? WHERE user_id = ?", (coins, ctx.author.id))
                await db.commit()

            await ctx.respond(embed=embed)
        else:
            coins = random.randint(10, 70)
            negative = [
                "Die Frau von nebenan hat dich verarscht und dir das Portemonnaie gestohlen! "
                f"Du verlierst 💎 **{coins}** Diamanten!"
            ]
            embed = discord.Embed(description=random.choice(negative), color=discord.Color.red())

            async with aiosqlite.connect(self.DB) as db:
                await db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?", (coins, ctx.author.id))
                await db.commit()

            await ctx.respond(embed=embed)

    @slash_command(description="")
    @discord.guild_only()
    async def crime(self, ctx):
        await ctx.respond("👷‍♂️| Der Crime-Befehl ist momentan in Wartungen!", ephemeral=True)
        # positive = [f"Du hast erfolgreich eine Bank überfallen und die Beute beträgt {eco} **{coins}** Diamaten!"]
        # negative = [f"Die Polizei hat dich beim überfallen einer Bank geschnappt und du musst {eco} **{coins}**
        # Diamaten zahlen!"]

    @slash_command(description="")
    @discord.guild_only()
    async def withdraw(self, ctx, anzahl: Option(int, "", required=True)):
        cash = await self.get_cash(ctx.author.id)
        bank = await self.get_bank(ctx.author.id)

        if anzahl > bank or anzahl < 0:
            embed = discord.Embed(description="Du hast nicht so viel Geld!", color=discord.Color.red())
            embed.add_field(name="Aktuelle Diamanten auf Ihrer Bank:", value=f"💎 {bank}")
            return await ctx.send(embed=embed)
        else:
            bank -= anzahl
            cash += anzahl

            async with aiosqlite.connect(self.DB) as db:
                await db.execute("UPDATE economy SET bank = ?, cash = ? WHERE user_id = ?", (bank, cash, ctx.author.id))
                await db.commit()

            embed = discord.Embed(description=f"Du hast erfolgreich 💎 **{anzahl}** Diamanten abgehoben.",
                                  color=discord.Color.green())
            await ctx.respond(embed=embed)

    @slash_command(description="")
    @discord.guild_only()
    async def rob(self, ctx, user: Option(discord.Member, "", required=True)):
        cash = await self.get_cash(user.id)

        if cash < 100:
            embed = discord.Embed(description="Es lohnt sich nicht.", color=discord.Color.green())
            return await ctx.respond(embed=embed)
        if user == ctx.author:
            embed = discord.Embed(description="Du kannst dich nicht selber beklauen!", color=discord.Color.green())
            return await ctx.respond(embed=embed)
        if random.randint(1, 100) > 60:
            coins = random.randint(1, cash)
            positive = [
                f"Du hast die Brieftasche eines alten Mannes gestohlen und 💎 **{coins}** Diamanten herausgenommen!"
            ]

            embed = discord.Embed(description=random.choice(positive), color=discord.Color.green())

            async with aiosqlite.connect(self.DB) as db:
                await db.execute("UPDATE economy SET cash = cash + ? WHERE user_id = ?", (coins, ctx.author.id))
                await db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?", (coins, user.id))
                await db.commit()

            await ctx.respond(embed=embed)
        else:
            coins = random.randint(1, 175)
            negative = [
                f"Du wurdest von einem Polizisten erwischt! Du musstest 💎 **{coins}** Diamanten bezahlen, "
                "um aus dem Gefängnis zu kommen!",
                "Du hast versucht, einer alten Frau das Telefon zu stehlen, aber du wusstest nicht, "
                "dass sie ein Boxprofi ist! Sie schlug dir ins Gesicht und rief die Polizei. "
                f"Du hast 💎 **{coins}** Diamanten bezahlt, um rauszukommen!"
            ]
            embed = discord.Embed(description=random.choice(negative), color=discord.Color.red())

            async with aiosqlite.connect(self.DB) as db:
                await db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?", (coins, ctx.author.id))
                await db.execute("UPDATE economy SET cash = cash + ? WHERE user_id = ?", (coins, user.id))
                await db.commit()

            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
