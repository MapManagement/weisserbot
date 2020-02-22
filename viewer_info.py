from twitchio.ext import commands
import command_editor


@commands.cog()
class ViewerInfo:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json("command_library.json")["commands"]

    @commands.command(name="arena")
    async def arena(self, ctx):
        await ctx.send(self.data["arena"]["content"])

    @commands.command(name="auszahlung")
    async def payout(self, ctx):
        await ctx.send(self.data["auszahlung"]["content"])

    @commands.command(name="bttv")
    async def bttv(self, ctx):
        await ctx.send(self.data["bttv"]["content"])

    @commands.command(name="caps")
    async def capslock(self, ctx):
        await ctx.send(self.data["caps"]["content"])

    @commands.command(name="donate")
    async def donate(self, ctx):
        await ctx.send(self.data["donate"]["content"])

    @commands.command(name="donation")
    async def donation(self, ctx):
        await ctx.send(self.data["donation"]["content"])

    @commands.command(name="duo")
    async def duo_mate(self, ctx):
        await ctx.send(self.data["duo"]["content"])

    @commands.command(name="earnings")
    async def earnings(self, ctx):
        await ctx.send(self.data["earnings"]["content"])

    @commands.command(name="friendlist")
    async def friendlist(self, ctx):
        await ctx.send(self.data["friendlist"]["content"])

    @commands.command(name="info")
    async def info(self, ctx):
        await ctx.send(self.data["info"]["content"])

    @commands.command(name="mitmachen")
    async def participate(self, ctx):
        await ctx.send(self.data["mitmachen"]["content"])

    @commands.command(name="moehren")
    async def carrots(self, ctx):
        await ctx.send(self.data["moehren"]["content"])

    @commands.command(name="prime")
    async def prime(self, ctx):
        await ctx.send(self.data["prime"]["content"])

    @commands.command(name="shop")
    async def fn_shop(self, ctx):
        await ctx.send(self.data["shop"]["content"])

    @commands.command(name="spam")
    async def spam(self, ctx):
        print(self.data)
        await ctx.send(self.data["spam"]["content"])

    @commands.command(name="spielersuche")
    async def lookin_for_mate(self, ctx):
        await ctx.send(self.data["spielersuche"]["content"])

    @commands.command(name="sub")
    async def subscription(self, ctx):
        await ctx.send(self.data["sub"]["content"])

    @commands.command(name="subgifts")
    async def subgifts(self, ctx):
        await ctx.send(self.data["subgifts"]["content"])

    @commands.command(name="vip")
    async def vip(self, ctx):
        await ctx.send(self.data["vip"]["content"])

    @commands.command(name="überlesen")
    async def not_read(self, ctx):
        await ctx.send(self.data["überlesen"]["content"])

    @commands.command(name="cc")
    async def cc(self, ctx):
        await ctx.send(self.data["cc"]["content"])

    @commands.command(name="commands")
    async def commands(self, ctx):
        await ctx.send(self.data["commands"]["content"])
