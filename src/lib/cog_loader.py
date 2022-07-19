import os
import traceback

from src.bot import Saber
from src.enum import ConsoleColors as Color


def loader(bot_instance: Saber) -> None:

    """
    Doesn't return anything. It used only when starting up bot.
    """

    for file in os.listdir("./cogs"):
        try:

            if file == "__pycache__":
                continue

            if ".py" in file:
                bot_instance.load_extension(f"cogs.{file[:-3]}")
                print(f"{Color.OKGREEN.value}Successfully loaded {file}")
            else:
                for subfile in os.listdir(f"./cogs/{file}"):

                    if subfile == "__pycache__":
                        continue

                    if ".py" in subfile:
                        bot_instance.load_extension(f"cogs.{file}.{subfile[:-3]}")
                        print(f"{Color.OKGREEN.value}Successfully loaded {file}/{subfile}")
        except Exception as e:
            print(f"{Color.FAIL.value}>>> Failed to load extension {file}.\n>>> {e}")
            print(f"{Color.WARNING.value}{traceback.format_exc()}")
