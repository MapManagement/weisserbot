from twitchio.ext import commands
import command_editor


@commands.cog()
class Gear:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json("command_library.json")["commands"]

    @commands.command(name="facecam")
    async def facecam(self, ctx):
        await ctx.send(self.data["facecam"]["content"])

    @commands.command(name="hardware")
    async def hardware(self, ctx):
        await ctx.send(self.data["hardware"]["content"])

    @commands.command(name="leitung")
    async def leitung(self, ctx):
        await ctx.send(self.data["leitung"]["content"])

    @commands.command(name="keyboard")
    async def keyboard(self, ctx):
        await ctx.send(self.data["keyboard"]["content"])

    @commands.command(name="maus")
    async def maus(self, ctx):
        await ctx.send(self.data["maus"]["content"])

    @commands.command(name="mousepad")
    async def mousepad(self, ctx):
        await ctx.send(self.data["mousepad"]["content"])

    @commands.command(name="mic")
    async def mic(self, ctx):
        await ctx.send(self.data["mic"]["content"])

    @commands.command(name="monitor")
    async def monitor(self, ctx):
        await ctx.send(self.data["monitor"]["content"])

    @commands.command(name="setup")
    async def setup(self, ctx):
        await ctx.send(self.data["setup"]["content"])
