import aiohttp
from typing import Union


async def get(string: str, params: dict) -> Union[dict, None]:
    async with aiohttp.ClientSession() as session:
        print(params)
        print(string)
        async with session.get(string, params=params) as resp:

            print(f'🚀 Request sent to {resp.url}. Status: {resp.status}')

            if resp.status == 404:
                return None

            return await resp.json(content_type=None)
