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
DEFAULT_FOOTER: str = f'MLP © gigabit- {datetime.datetime.utcnow().year}'

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
    "D": "<:osu_D:962171534577917983>",
    "C": "<:osu_C:962171534884106281>",
    "B": "<:osu_B:962171534867312671>",
    "A": "<:osu_A:962171534858924072>",
    "S": "<:osu_S:962171534674378802>",
    "SH": "<:osu_SH:962171534741471292>",
    "X": "<:osu_X:962171535060258877>",
    "XH": "<:osu_XH:962171534661800008>"
}

OSU: str = "<:osu:996567765676732516>"

# OWOIfy
PREFIXES: list = ["<3", "0w0", "H-hewwo??", "HIIII!", "Haiiii!", "Huohhhh.", "OWO", "OwO", "UwU", "Whats this?"]
SUFFIXES: list = ["( ͡° ᴥ ͡°)", "(இωஇ )", "(๑•́ ₃ •̀๑)", "(• o •)", "(●´ω｀●)", "(◠‿◠✿)", "(✿ ♡‿♡)", "(❁´◡`❁)",
                  "(人◕ω◕)", "(；ω；)", "(｀へ´)", "._.", "\\*nuzzles u\\*", ":3", ":D", ":P", ";-;", ";3", ";_;",
                  "<{^v^}>", ">_<", ">_>", "UwU", "XDDD", "^-^", "^_^", "x3", "xD", "ÙωÙ", "ʕʘ‿ʘʔ", "ㅇㅅㅇ",
                  "fwendo", "(＾ｖ＾)", "nya~"]
SUBSTITUTIONS: dict = {"love": "wuv", "Love": "Wuv", "loving": "wuving", "Loving": "Wuving", "r": "w", "l": "w",
                       "R": "W", "L": "W", "th ": "f ", "no": "nu", "No": "Nu", "has": "haz", "Has": "Haz",
                       "have": "haz", "Have": "Haz", " says": " sez", "you": "uu", "I've": "I", "the ": "da ",
                       "The ": "Da ", "THE ": "THE ", "qu": "qw", "Qu": "Qw", "pause ": "paws ", "Pause ": "Paws ",
                       "paus": "paws", "Paus": "paws", "u": "wu"}
