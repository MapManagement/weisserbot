from twitchio.ext import commands
from bot.cogs import command_editor
import os


@commands.cog()
class Gear:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json(command_editor.lib_path + f"{os.sep}command_library.json")["commands"]

    @commands.command(name="facecam")
    async def facecam(self, ctx):
        await ctx.send(self.data["facecam"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="hardware")
    async def hardware(self, ctx):
        await ctx.send(self.data["hardware"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="leitung")
    async def leitung(self, ctx):
        await ctx.send(self.data["leitung"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="keyboard")
    async def keyboard(self, ctx):
        await ctx.send(self.data["keyboard"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="maus")
    async def maus(self, ctx):
        await ctx.send(self.data["maus"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="mousepad")
    async def mousepad(self, ctx):
        await ctx.send(self.data["mousepad"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="mic")
    async def mic(self, ctx):
        await ctx.send(self.data["mic"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="monitor")
    async def monitor(self, ctx):
        await ctx.send(self.data["monitor"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="setup")
    async def setup(self, ctx):
        await ctx.send(self.data["setup"]["content"] + f" | {ctx.message.author.name}")
