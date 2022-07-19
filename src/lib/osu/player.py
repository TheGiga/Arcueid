import os

from pydantic import BaseModel
from src.lib import async_get
from datetime import datetime, timedelta
from . import gamemodes


class OsuPlayer(BaseModel):
    nickname: str
    user_id: int
    join_date: datetime
    country: str

    osu: gamemodes.Std
    taiko: gamemodes.Taiko
    ctb: gamemodes.Ctb
    mania: gamemodes.Mania

    @classmethod
    async def from_nickname(cls, nickname: str):
        modes = {
            "osu!": 0,
            "Taiko": 1,
            "CtB": 2,
            "osu!mania": 3
        }

        api_key = os.getenv("osu_api_key")

        data = []

        for mode in modes:
            params = {
                'k': api_key,
                'u': nickname,
                'm': modes[mode],
                'type': 'string'
            }
            raw_data = await async_get(f'https://osu.ppy.sh/api/get_user', params=params)
            try:
                data.append(raw_data[0])
            except IndexError:
                data.append(None)

        if data[0] is None:
            return None

        osu_std: gamemodes.Base = gamemodes.Std.parse_obj(data[0])

        osu_std.better_level = round(float(osu_std.level))
        osu_std.pp = round(float(osu_std.pp_raw))
        osu_std.better_accuracy = round(float(osu_std.accuracy), ndigits=2)
        osu_std.total_playtime = timedelta(seconds=osu_std.total_seconds_played)

        osu_taiko: gamemodes.Base = gamemodes.Taiko.parse_obj(data[1])
        osu_ctb: gamemodes.Base = gamemodes.Ctb.parse_obj(data[2])
        osu_mania: gamemodes.Base = gamemodes.Mania.parse_obj(data[3])

        return cls(
            nickname=data[0].get('username'),
            user_id=data[0].get('user_id'),
            join_date=datetime.strptime(data[0].get('join_date'), '%Y-%m-%d %H:%M:%S'),
            country=data[0].get('country'),

            osu=osu_std,
            taiko=osu_taiko,
            ctb=osu_ctb,
            mania=osu_mania
        )
