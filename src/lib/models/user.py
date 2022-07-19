from typing import Union

import config
from tortoise.models import Model
from tortoise import fields
from src.lib.osu import OsuPlayer


class User(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.IntField()
    balance = fields.IntField(default=0)
    connections = fields.JSONField(default=config.CONNECTIONS)

    def __str__(self):
        return self.discord_id

    def __repr__(self):
        return f'User({self.discord_id=}, {self.id=})'

    async def get_osu_player(self) -> Union[None, OsuPlayer]:
        username = self.connections['osu'].get('username')
        if username is None:
            return None

        player = await OsuPlayer.from_nickname(username)

        return player


