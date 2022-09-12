from typing import Union

import config
from tortoise import fields
from tortoise.models import Model
from .reminder import Reminder
from ...colors import ConsoleColors as clrs


class Guild(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.IntField()
    settings = fields.JSONField(default=config.DEFAULT_GUILD_SETTINGS)

    def __str__(self):
        return self.discord_id

    def __repr__(self):
        return f'Guild({self.discord_id=}, {self.id=})'

    async def get_or_create_reminder(self) -> Reminder:
        reminder, created = await Reminder.get_or_create(guild_id=self.discord_id)

        if created:
            print(f'{clrs.OKBLUE} Created reminder for {self.discord_id}')

        return reminder

    async def get_reminder(self) -> Union[Reminder, None]:
        reminder = await Reminder.get_or_none(guild_id=self.discord_id)
        return reminder
