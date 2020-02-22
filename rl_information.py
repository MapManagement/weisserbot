from twitchio.ext import commands
import command_editor


@commands.cog()
class RLInformation:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json("command_library.json")["commands"]

    @commands.command(name="age")
    async def age(self, ctx):
        await ctx.send(self.data["age"]["content"])

    @commands.command(name="beruf")
    async def job(self, ctx):
        await ctx.send(self.data["beruf"]["content"])

    @commands.command(name="face")
    async def face(self, ctx):
        await ctx.send(self.data["face"]["content"])

    @commands.command(name="herkunft")
    async def origin(self, ctx):
        await ctx.send(self.data["herkunft"]["content"])

    @commands.command(name="name")
    async def name(self, ctx):
        await ctx.send(self.data["name"]["content"])

    @commands.command(name="org")
    async def org(self, ctx):
        await ctx.send(self.data["org"]["content"])

    @commands.command(name="schule")
    async def school(self, ctx):
        await ctx.send(self.data["schule"]["content"])
