import discord

import config
from src import Saber


class InfoCommand(discord.Cog):
    def __init__(self, bot: Saber):
        self.bot = bot
        self.description = "Informative command."

    @discord.slash_command(name='info', description='Informative command, gives basic info about the bot.')
    async def information(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(colour=discord.Colour.embed_background(), timestamp=discord.utils.utcnow())

        embed.description = '**Multi-Purpose discord bot**, mainly made for fun by `gigalegit-#0880`.\n' \
                            'Use `/help` to get list of command and features.\n\n' \
                            '**If you want to add the bot:** Open bot profile > Click `Add to Server`'
        embed.title = config.PROJECT_NAME

        embed.add_field(name='👥 User Count', value=str(self.bot.user_count))
        embed.add_field(name='📁 Guild Count', value=str(self.bot.guild_count))

        embed.set_thumbnail(url=self.bot.user.avatar.url)

        await ctx.respond(embed=embed)


def setup(bot: Saber):
    bot.add_cog(InfoCommand(bot=bot))
