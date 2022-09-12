from tortoise.models import Model
from tortoise import fields


class Punishment(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    author_id = fields.IntField()
    guild_id = fields.IntField()
    reason = fields.TextField()
    date = fields.DatetimeField()
    muted_for = fields.TimeDeltaField()
    type = fields.TextField(default='mute')

    def __str__(self):
        return f'<@{self.user_id}> was punished by <@{self.author_id}> with reason `{self.reason}`'

    def __repr__(self):
        return f'Punishment({self.id=}, {self.user_id=} {self.author_id=})'
