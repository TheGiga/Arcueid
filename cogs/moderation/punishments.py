import discord
from src import Saber
from src.lib.models import User
from src.lib.models import Punishment


class Punishments(discord.Cog):
    def __init__(self, bot: Saber):
        self.bot = bot

    @discord.slash_command(name='case', description='Shows information about punishment case.')
    async def case(
            self, ctx: discord.ApplicationContext,
            case_id: discord.Option(int, description="Case ID", name="case")
    ):
        embed = discord.Embed(
            colour=discord.Colour.embed_background(), timestamp=discord.utils.utcnow()
        )

        case = await Punishment.get_or_none(id=case_id)
        if case is None:
            embed.title = "❌ Case Not Found!"
            embed.description = f'Case with ID `{case_id}` not found!'
            return await ctx.respond(embed=embed, ephemeral=True)

        embed.title = f'CASE #{case_id}'
        embed.description = str(case)

        guild = self.bot.get_guild(case.guild_id)

        if guild is not None:
            embed.add_field(name='📁 Guild', value=guild.name)

        embed.add_field(name='📄 Type of action', value=case.type.upper())
        embed.set_footer(text='by gigalegit-#0880')

        await ctx.respond(embed=embed)

    @discord.slash_command(name='punishments', description='Shows punishments of specific user.')
    async def punishments(
            self, ctx: discord.ApplicationContext,
            member: discord.Option(discord.Member, required=False, description="User to get Punishments list from.")
    ):
        if member is None:
            member = ctx.author

        user, created = await User.get_or_create(discord_id=member.id)

        embed = discord.Embed(colour=discord.Colour.embed_background(), timestamp=discord.utils.utcnow())
        embed.title = f"Punishments of {member}"

        embed.set_footer(icon_url=member.display_avatar.url)

        if created is True or len(user.punishments) == 0:
            embed.description = "*This user has no punishments*"
            return await ctx.respond(embed=embed)

        await ctx.defer()

        text = ""

        for punishment_id in user.punishments:
            punishment = await Punishment.get(id=punishment_id)
            text += f'`#{punishment.id}` **{punishment.type.upper()}** | '

        embed.description = text[:-2] + f"\n\n*Use </case:1009892953604497429> " \
                                        "to get additional information about specific Case*."

        embed.set_footer(text='by gigalegit-#0880')

        await ctx.respond(embed=embed)


def setup(bot: Saber):
    bot.add_cog(Punishments(bot=bot))
