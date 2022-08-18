import discord
import config
from src import Saber
from src.lib.models import User
from src.lib.osu import OsuPlayer, get_player_embed, get_player_view
from discord import SlashCommandGroup


class OsuStats(discord.Cog):
    def __init__(self, bot: Saber):
        self.bot = bot

    osu = SlashCommandGroup("osu", "osu! statistics and tools")

    @discord.user_command(name='osu! stats')
    async def context_player(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()

        user, created = await User.get_or_create(discord_id=member.id)
        user: User
        data = await user.get_osu_player()

        if data is None:
            return await ctx.respond(
                ":x: **Couldn't get statistics...**\n"
                "This user doesn't seem to have osu! username linked. User `/osu link`",
                ephemeral=True
            )

        embed = get_player_embed(data)
        view = get_player_view(data)

        await ctx.respond(embed=embed, view=view)

    @osu.command(name='player', description='Shows osu! statistics in STD game mode.')
    async def player(
            self, ctx: discord.ApplicationContext,
            nickname: discord.Option(str, description='osu! player nickname', required=False)
    ):
        await ctx.defer()

        if nickname is None:
            user, created = await User.get_or_create(discord_id=ctx.author.id)
            user: User
            data = await user.get_osu_player()
        else:
            data = await OsuPlayer.from_nickname(nickname=nickname)

        if data is None:
            return await ctx.respond(
                ":x: **Couldn't get statistics...**"
                "\nRecheck nickname spelling or use `/osu link` to link your nickname.",
                ephemeral=True)

        embed = get_player_embed(data)
        view = get_player_view(data)

        await ctx.respond(embed=embed, view=view)

    @osu.command(
        name='link',
        description='Let you link osu! username to your account. (You can link any name, no limitations)'
    )
    async def link(self, ctx: discord.ApplicationContext, username: discord.Option(str, description="osu! nickname")):
        await ctx.defer()

        osu_data = await OsuPlayer.from_nickname(nickname=username)

        if osu_data is None:
            return await ctx.respond(content=f'❌ There is no user with nickname `{username}`.', ephemeral=True)

        user, created = await User.get_or_create(discord_id=ctx.author.id)
        user: User

        updated_connections = config.CONNECTIONS.copy()
        updated_connections['osu']['username'] = str(username)

        user.connections = updated_connections

        await user.save()

        country_flag = f':flag_{osu_data.country.lower()}:'

        await ctx.respond(
            content=f'☑ Successfully linked username {country_flag} `{osu_data.nickname}` to your discord account.',
            ephemeral=True
        )


def setup(bot: Saber):
    bot.add_cog(OsuStats(bot=bot))
