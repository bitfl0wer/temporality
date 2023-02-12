import discord
from os import environ
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

if "TOKEN" not in environ:
    raise RuntimeError("TOKEN environment variable not set, exiting.")

__token__ = environ.get("TOKEN")


intents = discord.Intents.default()
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    """Gets executed once the bot is logged in."""
    print(f"Logged in as {bot.user}.")


bot.load_extension("src.commands.cog")
bot.run(__token__)
