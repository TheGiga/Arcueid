import datetime
import os
import discord
from dotenv import load_dotenv
from src import Saber, ConsoleColors as Colors, db_init
from art import tprint
from tortoise import run_async

load_dotenv()

intents = discord.Intents.all()
bot_instance: Saber = Saber(intents=intents)


@bot_instance.event
async def on_ready():
    print(Colors.OKGREEN.value)
    tprint("SABER")
    print(f"""
╔══════════╤═══════════════════════════════════────┄┄┄┄
║ Name     │ {bot_instance.user}
║ ID       │ {bot_instance.user.id}
║ Time UTC │ {datetime.datetime.utcnow().strftime("%d-%m-%y %H:%M")}
╚══════════╧═══════════════════════════════════────┄┄┄┄
    """)
    print(f"{Colors.OKCYAN.value}======================================================")

if __name__ == '__main__':
    run_async(db_init())
    bot_instance.run(os.getenv("TOKEN"))
