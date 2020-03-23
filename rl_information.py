from twitchio.ext import commands
import command_editor


@commands.cog()
class RLInformation:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json("command_library.json")["commands"]

    @commands.command(name="age")
    async def age(self, ctx):
        await ctx.send(self.data["age"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="beruf")
    async def beruf(self, ctx):
        await ctx.send(self.data["beruf"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="face")
    async def face(self, ctx):
        await ctx.send(self.data["face"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="herkunft")
    async def herkunft(self, ctx):
        await ctx.send(self.data["herkunft"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="name")
    async def name(self, ctx):
        await ctx.send(self.data["name"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="org")
    async def org(self, ctx):
        await ctx.send(self.data["org"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="schule")
    async def schule(self, ctx):
        await ctx.send(self.data["schule"]["content"] + f" | {ctx.message.author.name}")
