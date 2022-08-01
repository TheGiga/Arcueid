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
    # taiko: gamemodes.Taiko
    # ctb: gamemodes.Ctb
    # mania: gamemodes.Mania

    # i'd like to rewrite this bit to be more fancy, looking on it

    @classmethod
    async def from_nickname(cls, nickname: str):

        modes = {
            "osu!": 0,
            "Taiko": 1,
            "CtB": 2,
            "osu!mania": 3
        }

        api_key = os.getenv("OSU_API_KEY")

        params = {
            'k': api_key,
            'u': nickname,
            'm': modes['osu!'],
            'type': 'string'
        }
        data = await async_get(f'https://osu.ppy.sh/api/get_user', params=params)
        try:
            data[0]
        except IndexError:
            return None

        osu_std: gamemodes.Base = gamemodes.Std.parse_obj(data[0])

        osu_std.better_level = round(float(osu_std.level))
        osu_std.pp = round(float(osu_std.pp_raw))
        osu_std.better_accuracy = round(float(osu_std.accuracy), ndigits=2)
        osu_std.total_playtime = timedelta(seconds=osu_std.total_seconds_played)

        result = cls(
            nickname=data[0].get('username'),
            user_id=data[0].get('user_id'),
            join_date=datetime.strptime(data[0].get('join_date'), '%Y-%m-%d %H:%M:%S'),
            country=data[0].get('country'),

            osu=osu_std
        )

        return result
