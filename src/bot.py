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

            print(f'{ConsoleColors.OKGREEN.value}Successfully loaded {cog}')
