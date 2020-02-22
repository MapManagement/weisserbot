from twitchio.ext import commands
import command_editor


def prepare(bot):
    bot.add_cog(CustomCommands(bot))


class CustomCommands:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json("command_library.json")["commands"]

