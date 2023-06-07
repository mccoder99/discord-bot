import aiosqlite
from discord.ext import commands


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "database.db"

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS economy
                (user_id INTEGER PRIMARY KEY, bank INTEGER DEFAULT 0, cash INTEGER DEFAULT 0)
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS level_system
                (user_id INTEGER PRIMARY KEY, msg_count INTEGER DEFAULT 0, xp INTEGER DEFAULT 0)
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS logging
                (guild_id INTEGER PRIMARY KEY, channel_id INTEGER DEFAULT 0)
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS ticket_support
                (guild_id INTEGER PRIMARY KEY, ticket_count INTEGER DEFAULT 0)
                """
            )


def setup(bot):
    bot.add_cog(Database(bot))
