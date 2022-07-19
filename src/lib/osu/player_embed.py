import datetime

import discord
from src.lib.osu import OsuPlayer
from config import RANKING_EMOJIS as RE


def get_player_embed(data: OsuPlayer) -> discord.Embed:
    osu_std = data.osu
    country = f':flag_{data.country.lower()}:'

    embed = discord.Embed(
        colour=discord.Colour.purple(), title=f"Displaying stats in {osu_std.mode} game mode.",
        timestamp=discord.utils.utcnow()
    )

    embed.description = \
        f"""
        {country} {data.country} #{osu_std.pp_country_rank}
        🇺🇳 WW #{osu_std.pp_rank}
        
        Playtime: ` {round(osu_std.total_seconds_played // 3600)} hours `
        """

    # DONE: Add other game modes
    # Maybe I shouldn't use string slicing and just expanded model, thinking on it.
    # Implemented other models. 16.07.2022

    embed.set_author(
        name=f'{data.nickname} Lv. {osu_std.better_level}', url=f'https://osu.ppy.sh/users/{data.user_id}'
    )

    embed.set_thumbnail(url=f'https://s.ppy.sh/a/{data.user_id}')

    embed.add_field(name='💪 PP', value=f'` {osu_std.pp} `')
    embed.add_field(name='🎯 Accuracy', value=f'` {osu_std.better_accuracy}% `')
    embed.add_field(name='📊 Play Count', value=f'` {osu_std.playcount} `')

    embed.add_field(
        name='ㅤ',
        value=f'{RE["XH"]} ` {osu_std.count_rank_ssh} ` {RE["X"]} ` {osu_std.count_rank_ss} ` '
              f'{RE["SH"]} ` {osu_std.count_rank_sh} ` {RE["S"]} ` {osu_std.count_rank_s} ` '
              f'{RE["A"]} ` {osu_std.count_rank_a} `'
    )

    embed.set_footer(text='by gigalegit-#0880')

    return embed
