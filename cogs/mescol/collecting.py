import discord
from src import Saber
from src.models import Guild


# TODO: Implement the thing fully

class Collecting(discord.Cog):
    def __init__(self, bot: Saber):
        self.bot = bot
        self.cache = {}

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        guild = await Guild.get_or_none(discord_id=message.guild.id)

        if guild is None:
            return

        if guild.settings.get('mescol') is True:
            # do the thing
            return


def setup(bot: Saber):
    bot.add_cog(Collecting(bot=bot))
