import datetime
import os
from dotenv import load_dotenv

load_dotenv()

import discord
from src import Saber, ConsoleColors as Colors, db_init
from art import tprint
from tortoise import run_async
from tests import InternalTests

intents = discord.Intents.default()
intents.__setattr__("members", True)  # I want to avoid stupid read-only warning, so using setattr
bot_instance: Saber = Saber(intents=intents)


@bot_instance.event
async def on_ready():
    print(Colors.OKGREEN)
    tprint("STARTED")
    print(f"""
╔══════════╤═══════════════════════════════════────┄┄┄┄
║ Name     │ {bot_instance.user}
║ ID       │ {bot_instance.user.id}
║ Time UTC │ {datetime.datetime.utcnow().strftime("%d-%m-%y %H:%M")}
╚══════════╧═══════════════════════════════════────┄┄┄┄
    """)
    print(f"{Colors.OKCYAN}======================================================")

    print(f"{Colors.WARNING} Running tests...")
    await InternalTests().run_all()


if __name__ == '__main__':
    run_async(db_init())
    bot_instance.run(os.getenv("TOKEN"))
