from twitchio.ext import commands
import command_editor


@commands.cog()
class Software:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json("command_library.json")["commands"]

    @commands.command(name="brightness")
    async def brightness(self, ctx):
        await ctx.send(self.data["brightness"]["content"])

    @commands.command(name="colorblind")
    async def colorblind(self, ctx):
        await ctx.send(self.data["colorblind"]["content"])

    @commands.command(name="dx12")
    async def dx12(self, ctx):
        await ctx.send(self.data["dx12"]["content"])

    @commands.command(name="res")
    async def res(self, ctx):
        await ctx.send(self.data["res"]["content"])

    @commands.command(name="sens")
    async def sens(self, ctx):
        await ctx.send(self.data["sens"]["content"])

    @commands.command(name="settings")
    async def settings(self, ctx):
        await ctx.send(self.data["settings"]["content"])
