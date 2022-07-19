import discord
from src.lib.osu import OsuPlayer


def get_player_view(data: OsuPlayer) -> discord.ui.View:
    view = discord.ui.View()
    button = discord.ui.Button(
        label='Player Profile',
        url=f'https://osu.ppy.sh/users/{data.user_id}'
    )

    view.add_item(button)

    return view
