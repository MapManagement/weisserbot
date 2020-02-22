from twitchio.ext import commands
import asyncio


async def cycler(to_cycle):
    print("before test")
    while True:
        print("test")
        await to_cycle
        await asyncio.sleep(1200)

