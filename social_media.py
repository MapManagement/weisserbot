from twitchio.ext import commands
import command_editor


@commands.cog()
class SocialMedia:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json("command_library.json")["commands"]

    @commands.command(name="twitter")
    async def twitter(self, ctx):
        await ctx.send(self.data["twitter"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="discord")
    async def discord(self, ctx):
        await ctx.send(self.data["discord"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="epic")
    async def epic(self, ctx):
        await ctx.send(self.data["epic"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="insta")
    async def insta(self, ctx):
        await ctx.send(self.data["insta"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="youtube")
    async def youtube(self, ctx):
        await ctx.send(self.data["youtube"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="playlist")
    async def playlist(self, ctx):
        await ctx.send(self.data["playlist"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="coc")
    async def coc(self, ctx):
        await ctx.send(self.data["coc"]["content"] + f" | {ctx.message.author.name}")

    @commands.command(name="chatstats")
    async def chatstats(self, ctx):
        await ctx.send(self.data["chatstats"]["content"] + f" | {ctx.message.author.name}")
