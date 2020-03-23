from twitchio.ext import commands
import asyncio


# work in progress
async def cycler(to_cycle):
    while True:
        await to_cycle
        await asyncio.sleep(1200)
