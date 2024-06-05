import datetime

OWNER_ID: int = 352062534469156864
OWNER_NAME: str = 'gigalegit-#0880'
PROJECT_NAME: str = 'Arcueid'
TESTING_BOT_ID: int = 965191147041464330  # For better testing experience, for example
# discord.ApplicationCommandInvokeError will be raised, instead of just sending message to channel, if bot has this id.

# SUPPORT SERVER
SUPPORT_SERVER_INVITE: str = 'https://discord.gg/27w6rzK892'
SUPPORT_SERVER_ID: int = 804835509968568351

# COGS
COGS: list = [
    'cogs.osu.stats',
    'cogs.social.profile',
    'cogs.owoify.message',
    'cogs.moderation.mute',
    'cogs.moderation.punishments',
    'cogs.al.reminder',
    'cogs.info',
    'cogs.help',
]

# USER CONNECTIONS TEMPLATE
CONNECTIONS: dict = {
    "osu": {
        'connection': "osu!",
        'username': ""
    }
}

# DEFAULT's
DEFAULT_FOOTER: str = f'Arcueid © gigabit- {datetime.datetime.utcnow().year}'

# GUILD's
DEFAULT_GUILD_SETTINGS = {
    "mescol": False,
    "beta": False
}

#  CONNECTION EMOJIS
CONNECTION_EMOJIS: dict = {
    "osu!": "<:osu:996567765676732516>"
}

# EMOJI'S
RANKING_EMOJIS: dict = {
    "D": "<:RankingD:1248023018463166515>",
    "C": "<:RankingC:1248023016642838569>",
    "B": "<:RankingB:1248023014205952020>",
    "A": "<:RankingA:1248023015632146462>",
    "S": "<:RankingS:1248023020908318752>",
    "SH": "<:RankingSH:1248023019599958117>",
    "X": "<:RankingX:1248023012775563315>",
    "XH": "<:RankingXH:1248023011219738695>"
}

OSU: str = "<:osu:996567765676732516>"
