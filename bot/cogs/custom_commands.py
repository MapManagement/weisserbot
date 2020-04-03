from bot.cogs import command_editor
from twitchio.ext import commands
import os


def prepare(bot):
    bot.add_cog(CustomCommands(bot))


class CustomCommands:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json(command_editor.lib_path + f"{os.sep}command_library.json")["commands"]

