import os

import aiohttp
import discord

import config
from discord import Bot, ExtensionNotFound, Webhook
from src.enum import ConsoleColors
from src.lib.models import Guild


class Saber(Bot):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)

        self.owner_id = config.OWNER_ID

        cogs = config.COGS
        for cog in cogs:
            try:
                self.load_extension(cog)
            except ExtensionNotFound:
                print(f'{ConsoleColors.FAIL.value}Extension {cog} not found!')
            else:
                print(f'{ConsoleColors.OKGREEN.value}Successfully loaded {cog}')

    async def on_guild_join(self, guild: discord.Guild):
        embed = discord.Embed(colour=discord.Colour.green(), timestamp=discord.utils.utcnow())
        embed.title = f"Joined guild: `{guild.name} ({guild.id})`"
        embed.add_field(name='📁 Guilds', value=str(self.guild_count))

        await Guild.get_or_create(discord_id=guild.id)
        await self.send_log_message(embed=embed)

    # Stole this bit from Toolkit's code https://github.com/Pycord-Development/Pycord-Manager /
    # (https://github.com/Dorukyum/Toolkit)

    async def on_application_command_error(
            self, ctx: discord.ApplicationContext, error: discord.ApplicationCommandError
    ):
        if isinstance(error, discord.ApplicationCommandInvokeError):
            await ctx.respond(
                "An unexpected error has occurred and I've notified my developer. "
                "In the meantime, consider joining my support server.",
                view=discord.ui.View(
                    discord.ui.Button(
                        label="Support", url=config.SUPPORT_SERVER_INVITE
                    ),
                    discord.ui.Button(
                        label="GitHub Repo",
                        url="https://github.com/TheGiga/Arcueid",
                    ),
                ),
            )

            header = f"Command: `/{ctx.command.qualified_name}`"
            if ctx.guild is not None:
                header += f" | Guild: `{ctx.guild.name} ({ctx.guild_id})`"

            embed = discord.Embed(colour=discord.Colour.red(), title=header)
            embed.description = str(error)

            await self.send_log_message(embed=embed)

        await ctx.respond(
            embed=discord.Embed(
                title=error.__class__.__name__,
                description=str(error),
                color=discord.Color.embed_background(),
            )
        )

        if self.user.id == config.TESTING_BOT_ID:
            raise error

    async def send_log_message(self, embed: discord.Embed = None):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.getenv("ERROR_LOG_WEBHOOK"), session=session)
            embed.set_footer(text=self.user)
            await webhook.send(embed=embed)

    @property
    def guild_count(self) -> int:
        return len(self.guilds)

    @property
    def user_count(self) -> int:
        overall = 0

        for guild in self.guilds:
            overall += guild.member_count

        return overall

    def help_command_embed(self) -> discord.Embed:
        embed = discord.Embed(colour=discord.Colour.embed_background(), timestamp=discord.utils.utcnow())
        embed.title = 'Help'

        user_commands = ''
        slash_commands = ''
        message_commands = ''

        for command in self.commands:
            match command.__class__:
                case discord.SlashCommandGroup:
                    sub_commands = ''
                    for sub_command in command.subcommands:
                        sub_commands += f'> `{sub_command.name}` - {sub_command.description}\n'
                    embed.add_field(name=f'/{command.qualified_name}', value=sub_commands)
                case discord.UserCommand:
                    user_commands += f'`{command.qualified_name}`\n'
                case discord.MessageCommand:
                    message_commands += f'`{command.qualified_name}`\n'
                case _:
                    slash_commands += f'`/{command.qualified_name}`\n'

        embed.description = f"""
**User Commands**:
{user_commands}
**Message Commands**:
{message_commands}
**Standalone Slash Commands**:
{slash_commands}
        """

        return embed
