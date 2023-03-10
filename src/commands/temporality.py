from typing import List, Union

import discord, time
from discord.commands import Option, slash_command
from discord.ext import commands, tasks
from discord.errors import NotFound

from src.database_handler import Channels, Messages
from src.database_handler import session as db

allowed_units_time = ["s", "min", "h", "d", "w", "m", "y"]


def seperate_str_and_int(input: str) -> list:
    """Given an example string '123hello', this function will split this string into a list
    containing the elements [123] and ['hello'].

    Args:
        input (str): a string that starts with numbers which are followed by chars.

    Returns:
        List[str, int]: The output list
    """
    i = 0
    _output = list()
    for char in input:
        if not char.isdigit():
            _output.append(input[i:])
            _output.append(input[0:i])
            return _output
        else:
            i += 1


def make_relative_timestamp(unit: str, time_in_future: int) -> int:
    """Creates a timestamp that is $time seconds in the future.

    Args:
        unit (str): either s, min, h, d, w, m or y.
        time (int): positive integer

    Returns:
        int: unix timestamp
    """
    if not unit in allowed_units_time:
        return
    current_time = int(time.time())
    unit_multiplier_dict = {
        "s": 1,
        "min": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
        "m": 2629800,
        "y": 31556952,
    }
    return current_time + (int(time_in_future) * unit_multiplier_dict.get(unit))


class Temporality(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.message_cleanup.start()

    def cog_unload(self) -> None:
        self.message_cleanup.cancel()
        return super().cog_unload()

    @tasks.loop(seconds=1.0)
    async def message_cleanup(self):
        messages = db.query(Messages).all()
        for message in messages:
            if not message.deletion_timestamp <= int(time.time()):
                continue
            channel = db.query(Channels).filter_by(id=message.channel_id).one_or_none()
            if not channel.active:
                db.delete(message)
                db.commit()
                continue
            try:
                channel_fetched = self.bot.get_channel(channel.id)
                message_fetched = await channel_fetched.fetch_message(message.id)
                reactions = message_fetched.reactions
                if not reactions:
                    db.delete(message)
                    await message_fetched.delete()
                for reaction in reactions:
                    if reaction.emoji == "????" and await reaction.users().get(
                        id=message_fetched.author.id
                    ):
                        db.delete(message)
                    else:
                        db.delete(message)
                        await message_fetched.delete()
            except NotFound:
                pass
            db.commit()

    @message_cleanup.before_loop
    async def before_message_cleanup(self):
        print("Waiting...")
        await self.bot.wait_until_ready()

    @slash_command(name="activate")
    async def temporality_setup(
        self,
        ctx: discord.ApplicationContext,
        channel: Option(
            discord.TextChannel,
            description="The channel to activate automatically disappearing messages in.",
        ),
        time: Option(
            str,
            description="The amount of time the messages should get deleted after. Examples: 30min, 7h, 5d, 2w, 3m, 1y",
        ),
    ):
        if not ctx.user.guild_permissions.manage_messages:
            await ctx.response.send_message(
                f"womp womp. You do not have the required `MANAGE_MESSAGES` permission.",
                ephemeral=True,
            )
        if not seperate_str_and_int(time)[0] in allowed_units_time:
            await ctx.response.send_message(
                f"Time unit not recognized. Please use either `s, min, h, d, w, m` or `y`.",
                ephemeral=True,
            )
            return
        db_channel = db.query(Channels).filter_by(id=channel.id).one_or_none()
        if not db_channel:
            db_channel = Channels(id=channel.id, timeout=time)
            db.add(db_channel)
        else:
            db_channel.timeout = time
        db.commit()
        await ctx.response.send_message(
            f"Disappearing messages activated for channel #{channel.name} with a timer of {time}!"
        )
        return

    @slash_command(name="deactivate")
    async def temporality_deactivate(
        self,
        ctx: discord.ApplicationContext,
        channel: Option(
            discord.TextChannel,
            description="The channel to deactivate automatically disappearing messages in.",
        ),
    ):
        if not ctx.user.guild_permissions.manage_messages:
            await ctx.response.send_message(
                f"womp womp. You do not have the required `MANAGE_MESSAGES` permission.",
                ephemeral=True,
            )
        channel_deactivate = db.query(Channels).filter_by(id=channel.id).one_or_none()
        if not channel_deactivate:
            await ctx.response.send_message(
                "This channel does not have the temporality feature active. Did nothing.",
                ephemeral=True,
            )
            return
        await ctx.response.send_message(
            f"Deactivated disappearing messages for channel #{channel.name}."
        )
        messages = db.query(Messages).all()
        for message in messages:
            db.delete(message)
        db.delete(channel_deactivate)
        db.commit()
        return


def setup(bot: discord.Bot):
    """This setup function is needed by pycord to "link" the cog to the bot.
    Args:
        bot (commands.Bot): the Bot-object.
    """
    bot.add_cog(Temporality(bot))
