import discord
from os import environ
from dotenv import load_dotenv
from discord.ext import commands
from src.database_handler import session as db, Channels, Messages
from src.commands.temporality import (
    seperate_str_and_int,
    make_relative_timestamp,
)

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


@bot.event
async def on_message(message: discord.message):
    if message.author.id == bot.user.id:
        return

    if not db.query(Channels).filter_by(id=message.channel.id).first():
        return

    timeout = seperate_str_and_int(
        db.query(Channels.timeout).filter_by(id=message.channel.id).one_or_none()[0]
    )

    expiration_date = make_relative_timestamp(timeout[0], timeout[1])

    db_message = Messages(
        id=message.id, channel_id=message.channel.id, deletion_timestamp=expiration_date
    )
    db.add(db_message)
    db.commit()


bot.load_extension("src.commands.temporality")

bot.run(__token__)
