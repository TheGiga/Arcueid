import discord

import config
from discord import Bot, ExtensionNotFound, SlashCommandGroup
from src.enum import ConsoleColors


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

        # TODO: should i remake this bit? too many elif's

        for command in self.commands:
            if isinstance(command, discord.SlashCommandGroup):
                sub_commands = ''
                for sub_command in command.subcommands:
                    sub_commands += f'> `{sub_command.name}` - {sub_command.description}\n'
                embed.add_field(name=f'/{command.qualified_name}', value=sub_commands)
            elif isinstance(command, discord.UserCommand):
                user_commands += f'`{command.qualified_name}`\n'
            elif isinstance(command, discord.MessageCommand):
                message_commands += f'`{command.qualified_name}`\n'
            else:
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
