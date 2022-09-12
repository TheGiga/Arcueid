import discord

import config
from src import Saber
from src.models import User


class Profile(discord.Cog):
    def __init__(self, bot: Saber):
        self.bot = bot

    @discord.slash_command(name='profile', description='User profiles.')
    async def profile(
            self, ctx: discord.ApplicationContext,
            target: discord.Option(discord.Member, name='user', required=False)
    ):
        if target is None:
            target = ctx.author

        user, created = await User.get_or_create(discord_id=target.id)

        user_connections = user.connections

        embed = discord.Embed(colour=discord.Colour.embed_background())
        embed.title = target.display_name
        embed.timestamp = discord.utils.utcnow()
        if created is True:
            embed.description = "✅ **Profile successfully created!**"

        for connection in user_connections:
            username = user_connections[connection].get('username')
            connection_name = user_connections[connection].get("connection")
            if len(username) != 0:
                emoji = config.CONNECTION_EMOJIS.get(connection_name)
                embed.add_field(
                    name=f'{emoji if not None else ""} {connection_name}',
                    value=username
                )

        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text=f"UID: {user.id} • by gigalegit-#0880")

        await ctx.respond(embed=embed)


def setup(bot: Saber):
    bot.add_cog(Profile(bot=bot))
