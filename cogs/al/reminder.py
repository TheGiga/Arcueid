import discord
from discord import SlashCommandGroup, guild_only, NotFound
from discord.ext import tasks
from discord.ext.commands import has_permissions

import config
from src.anilibria import Api
from src.anilibria.api_config import AL_TITLE
from src.models import Guild, Reminder
from src.colors import ConsoleColors as clrs


class ALReminderRU(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.reminder_loop.start()
        self.api = Api(discord_instance=bot)

    reminder = SlashCommandGroup("anilibria", "[RU/UA] Оповещения о новых релизах.")
    reminder_ping = reminder.create_subgroup(name='ping', description="[RU/UA] Настройки пингов в оповещениях.")

    @guild_only()
    @has_permissions(manage_guild=True)
    @reminder_ping.command(
        name='set_role', description='[RU/UA] Установить роль для упоминания при отправке оповещения.'
    )
    async def reminder_set_ping_role(
            self, ctx: discord.ApplicationContext,
            role: discord.Option(discord.Role, name='роль', description="Роль для упоминания")
    ):
        db_guild_object, created = await Guild.get_or_create(discord_id=ctx.guild.id)

        reminder = await db_guild_object.get_reminder()

        if created or reminder is None:
            return await ctx.respond(
                content="Оповещения не включены!, используйте </reminder set:1015015152644542485> для их включения.",
                ephemeral=True
            )

        reminder.ping = role.id
        await reminder.save()

        await ctx.respond(
            content=f"☑ Роль {role.mention} успешно установлена для упоминания в оповещениях.",
            ephemeral=True
        )

    @guild_only()
    @has_permissions(manage_guild=True)
    @reminder_ping.command(
        name='remove_role', description='[RU/UA] Отключить упоминание роли в оповещениях.'
    )
    async def reminder_set_ping_role(
            self, ctx: discord.ApplicationContext
    ):
        db_guild_object, created = await Guild.get_or_create(discord_id=ctx.guild.id)

        reminder = await db_guild_object.get_reminder()

        if created or reminder is None:
            return await ctx.respond(
                content="Оповещения не включены!, используйте </reminder set:1015015152644542485> для их включения.",
                ephemeral=True
            )

        reminder.ping = 0
        await reminder.save()

        await ctx.respond(
            content=f"☑ Вы успешно выключили упоминание роли в оповещениях.",
            ephemeral=True
        )

    @guild_only()
    @has_permissions(manage_guild=True)
    @reminder.command(name='reminder_disable', description='[RU/UA] Отключить отправку оповещений.')
    async def reminder_disable(
            self, ctx: discord.ApplicationContext
    ):
        db_guild_object, created = await Guild.get_or_create(discord_id=ctx.guild.id)

        reminder = await db_guild_object.get_reminder()

        if created or reminder is None:
            return await ctx.respond(
                content="Оповещения уже отключены, используйте </reminder set:1015015152644542485> для их включения.",
                ephemeral=True
            )

        await reminder.delete()

        await ctx.respond(
            content=f'✅ Оповещения о выходе новых серий успешно отключены.', ephemeral=True
        )

    @guild_only()
    @has_permissions(manage_guild=True)
    @reminder.command(name='reminder_set', description='[RU/UA] Включить отправку оповещений.')
    async def reminder_set(
            self, ctx: discord.ApplicationContext, channel: discord.Option(
                discord.TextChannel, name='канал', description='Канал в который будут отправляться оповещения.'
            )
    ):
        db_guild_object, created = await Guild.get_or_create(discord_id=ctx.guild.id)

        if created:
            print(f'Created object for guild {ctx.guild}({ctx.guild.id}), not in `on_guild_join`.')

        if not channel.can_send():
            return await ctx.respond(
                '❌ **У бота недостаточно прав для отправления сообщений в данный канал!** \n'
                'Выдайте следующие права: `Send Messages`, `Embed Links`; Либо используйте другой канал.',
                ephemeral=True
            )

        await ctx.defer()

        reminder = await db_guild_object.get_or_create_reminder()
        reminder.channel_id = channel.id
        await reminder.save()

        embed = discord.Embed(colour=discord.Colour.embed_background(), timestamp=discord.utils.utcnow())
        embed.description = """
**Данный канал установлен для получения уведомлений о выходе новых серий аниме на сайте `anilibria.tv`**.

Для включения упоминания роли пропишите </reminder ping set_role:1>
Для отключения уведомлений пропишите </reminder disable:1015015152644542485>
        """  # TODO: Add reminder ping set_role command id

        embed.set_footer(icon_url=self.bot.user.avatar.url, text=config.DEFAULT_FOOTER)

        await ctx.respond(
            content=f'✅ Канал {channel.mention} успешно установлен для получения оповещений!', ephemeral=True
        )
        await channel.send(embed=embed)

    @tasks.loop(minutes=5)
    async def reminder_loop(self):
        if not self.bot.is_ready():
            return

        to_post = await self.api.get_updates()

        if len(to_post) == 0:
            return

        print(f'{clrs.OKGREEN}There is updates, processing...')

        db_reminders = await Reminder.exclude(channel_id=0)

        reminders = [x.guild_id for x in db_reminders]

        print(f'{clrs.OKCYAN}Reminders: {reminders}')

        for reminder_object in db_reminders:
            guild = self.bot.get_guild(reminder_object.guild_id)
            if guild is None:
                try:
                    guild = await self.bot.fetch_guild(reminder_object.guild_id)
                except NotFound:
                    print(f"{clrs.FAIL}Guild with ID {reminder_object.guild_id} not found!")
                    continue

            channel = guild.get_channel(reminder_object.guild_id)
            role_id = reminder_object.ping

            if channel is None:
                try:
                    channel = await guild.fetch_channel(reminder_object.channel_id)
                except NotFound:
                    print(f"{clrs.FAIL}Channel with ID {reminder_object.channel_id} not found!")
                    continue

            for update in to_post:
                embed = update.form_embed()

                view = discord.ui.View()
                watch_episode = discord.ui.Button(label='Смотреть серию', emoji="🖥️", url=AL_TITLE.format(update.code))
                view.add_item(watch_episode)

                await channel.send(
                    content=f"<@&{role_id}>" if role_id != 0 else "",
                    embed=embed, view=view
                )

            print(f'{clrs.OKGREEN}Posted to {guild.name}')


def setup(bot: discord.Bot):
    bot.add_cog(ALReminderRU(bot=bot))
