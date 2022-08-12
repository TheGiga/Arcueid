import datetime
import config
import discord
from typing import Union
from tortoise import fields
from tortoise.models import Model
from src.lib.osu import OsuPlayer
from .punishment import Punishment


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
        if len(username) == 0:
            return None

        player = await OsuPlayer.from_nickname(username)

        return player

    async def timeout(self, author: discord.Member, guild: discord.Guild, time: datetime.timedelta, reason: str = None):
        user = guild.get_member(self.discord_id)

        if reason is None:
            reason = "No reason provided."

        if user is None:
            user = await guild.fetch_member(self.discord_id)

        punishment = await Punishment.create(
            user_id=self.discord_id,
            author_id=author.id,
            reason=reason,
            muted_for=time,
            date=datetime.datetime.utcnow()
        )

        # Exceptions should be caught outside this specific function.
        await user.timeout_for(duration=time, reason=reason)

        return punishment
