import datetime
import config
import discord
from tortoise import fields
from tortoise.models import Model


class Guild(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.IntField()
    settings = fields.JSONField(default=config.DEFAULT_GUILD_SETTINGS)

    def __str__(self):
        return self.discord_id

    def __repr__(self):
        return f'Guild({self.discord_id=}, {self.id=})'
