import discord
import aiohttp
from typing import Union


async def get(string: str, params: dict) -> Union[dict, None]:
    async with aiohttp.ClientSession() as session:
        async with session.get(string, params=params) as resp:

            if resp.status == 404:
                return None

            if resp.status != 200:
                print(f'❌ Request failed to {resp.url.host}. Error Code (Status): {resp.status}')
                embed = discord.Embed(colour=discord.Colour.orange(), title=f"Request failed to {resp.url.host}")
                embed.description = f"Failed request to `{resp.url}` with **{resp.status}**."

                from .bot import Saber

                await Saber.send_log_message(embed)
            return await resp.json(content_type=None)
