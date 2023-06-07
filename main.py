import os

import discord
import ezcord
from dotenv import load_dotenv


class DiscordBot(ezcord.Bot):
    def __init__(self, **options):
        super().__init__(**options)


load_dotenv()
ezcord.set_log(log_level=10)

bot = DiscordBot(intents=discord.Intents.all(), error_webhook_url=os.getenv("ERROR_WEBHOOK_URL"), language="de",
                 activity=discord.Activity(type=discord.ActivityType.watching, name="🚧 | Wartungsarbeiten"),
                 status=discord.Status.dnd, debug_guilds=None)

if __name__ == "__main__":
    bot.load_cogs()
    bot.run(os.getenv("BOT_TOKEN"))
