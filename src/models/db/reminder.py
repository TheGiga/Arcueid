from tortoise import fields
from tortoise.models import Model


class Reminder(Model):
    id = fields.IntField(pk=True)
    guild_id = fields.IntField()
    channel_id = fields.IntField(default=0)
    ping = fields.IntField(default=0)  # Role to ping, don't really want to rename it.

    def __repr__(self):
        return f'Reminder({self.channel_id=}, {self.guild_id=})'
