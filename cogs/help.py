import discord

from src import Saber


class HelpCommand(discord.Cog):
    def __init__(self, bot: Saber):
        self.bot = bot
        self.description = "Help command."

    @discord.slash_command(name='help', description='General help and features.')
    async def help(self, ctx: discord.ApplicationContext):
        await ctx.respond(embed=self.bot.help_command_embed())


def setup(bot: Saber):
    bot.add_cog(HelpCommand(bot=bot))
