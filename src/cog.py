import discord
from discord.ext import commands
from discord.commands import (
    slash_command,
)


class ExampleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="hello")
    async def hello_world(self, ctx: discord.Interaction):
        await ctx.response.send_message(f"Hello, World!", ephemeral=True)


def setup(bot: discord.Bot):
    """This setup function is needed by pycord to "link" the cog to the bot.
    Args:
        bot (commands.Bot): the Bot-object.
    """
    bot.add_cog(ExampleCog(bot))
