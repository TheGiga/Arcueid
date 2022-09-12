import calendar

import discord
import time_str
from discord import Forbidden
from discord.ext.commands.errors import UserNotFound
from discord.ext.commands import has_permissions
from datetime import datetime

from src import Saber
from src.models import User


class Moderation(discord.Cog):
    def __init__(self, bot: Saber):
        self.bot = bot

    @has_permissions(moderate_members=True)
    @discord.slash_command(name='mute', description='Timeout user for specific time.')
    async def mute(
            self,
            ctx: discord.ApplicationContext,
            member: discord.Option(discord.Member, description="User"),
            time: discord.Option(str, description="Time"),
            reason: discord.Option(str, description="Reason"),
    ):
        if ctx.author.id == member.id:
            return await ctx.respond(
                content="❌ Self harm is not allowed!",
                ephemeral=True
            )

        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.respond(
                ephemeral=True,
                content="You can't mute a person with role higher then yours!"
            )

        user, created = await User.get_or_create(discord_id=member.id)

        time = time_str.convert(time)

        await ctx.defer()

        try:
            punishment = await user.timeout(
                author=ctx.author,
                guild=ctx.guild,
                reason=reason,
                time=time
            )
        except UserNotFound:
            return await ctx.respond(content='❌ User not found!')
        except Forbidden:
            return await ctx.respond(content='⚠ Bot has no permissions to mute this user.')

        embed = discord.Embed(
            title=f'🚔 Case №{punishment.id}',
            timestamp=discord.utils.utcnow(),
            color=discord.Colour.embed_background()
        )

        embed.description = f"```css\n[ {punishment.reason} ]```"

        until = calendar.timegm(datetime.timetuple(datetime.utcnow() + punishment.muted_for))

        embed.add_field(name='👤 User', value=member.mention)
        embed.add_field(name='⏰ Unmute', value=f"<t:{until}:R>")
        embed.set_footer(text=f'Moderator: {ctx.author.name}#{ctx.author.discriminator}')

        await ctx.respond(embed=embed)


def setup(bot: Saber):
    bot.add_cog(Moderation(bot=bot))
