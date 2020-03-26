from twitchio.ext import commands
from bot.cogs import command_editor


@commands.cog()
class ViewerInfo:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json(command_editor.cmd_lib_path)["commands"]

    @commands.command(name="arena")
    async def arena(self, ctx):
        await ctx.send(self.data["arena"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="auszahlung")
    async def auszahlung(self, ctx):
        await ctx.send(self.data["auszahlung"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="bttv")
    async def bttv(self, ctx):
        await ctx.send(self.data["bttv"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="caps")
    async def caps(self, ctx):
        await ctx.send(self.data["caps"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="donate")
    async def donate(self, ctx):
        await ctx.send(self.data["donate"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="donation")
    async def donation(self, ctx):
        await ctx.send(self.data["donation"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="duo")
    async def duo(self, ctx):
        await ctx.send(self.data["duo"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="earnings")
    async def earnings(self, ctx):
        await ctx.send(self.data["earnings"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="friendlist")
    async def friendlist(self, ctx):
        await ctx.send(self.data["friendlist"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="info")
    async def info(self, ctx):
        await ctx.send(self.data["info"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="mitmachen")
    async def mitmachen(self, ctx):
        await ctx.send(self.data["mitmachen"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="moehren")
    async def moehren(self, ctx):
        await ctx.send(self.data["moehren"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="prime")
    async def prime(self, ctx):
        await ctx.send(self.data["prime"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="shop")
    async def shop(self, ctx):
        await ctx.send(self.data["shop"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="spam")
    async def spam(self, ctx):
        print(self.data)
        await ctx.send(self.data["spam"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="spielersuche")
    async def spielersuche(self, ctx):
        await ctx.send(self.data["spielersuche"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="sub")
    async def sub(self, ctx):
        await ctx.send(self.data["sub"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="subgifts")
    async def subgifts(self, ctx):
        await ctx.send(self.data["subgifts"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="vip")
    async def vip(self, ctx):
        await ctx.send(self.data["vip"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="ueberlesen")
    async def ueberlesen(self, ctx):
        await ctx.send(self.data["überlesen"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="cc")
    async def cc(self, ctx):
        await ctx.send(self.data["cc"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="commands")
    async def commands(self, ctx):
        await ctx.send(self.data["commands"]["content"] + f" | {ctx.message.author.name}")
