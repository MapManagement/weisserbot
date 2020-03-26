from twitchio.ext import commands


async def is_mod(ctx):
    return ctx.author.is_mod


async def is_sub(ctx):
    return ctx.author.is_subscriber
