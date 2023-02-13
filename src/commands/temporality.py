import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from src.database_handler import session as db

temporality_mode = str()


def temporality_logic(mode: str) -> None:
    return


class Temporality(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="disappear-activate")
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
        await ctx.response.send_message(f"Hello, World!", ephemeral=True)


def setup(bot: discord.Bot):
    """This setup function is needed by pycord to "link" the cog to the bot.
    Args:
        bot (commands.Bot): the Bot-object.
    """
    bot.add_cog(Temporality(bot))
