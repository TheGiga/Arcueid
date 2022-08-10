import random
import discord
import config
from src import Saber


class OwOify(discord.Cog):
    def __init__(self, bot: Saber):
        self.bot = bot

    # Thanks Cic1e#4354 for code, I stole and reworked it a little.

    @discord.message_command(name="OwO-ify message")
    async def owo_cmd(self, ctx, text: discord.Message):
        prefix = random.choice(config.PREFIXES)
        suffix = random.choice(config.SUFFIXES)
        content = text.content

        for word, ini in config.SUBSTITUTIONS.items():
            content = content.replace(word.lower(), ini)

        await ctx.respond(f"{prefix} {content} {suffix}")


def setup(bot: Saber):
    bot.add_cog(OwOify(bot=bot))
