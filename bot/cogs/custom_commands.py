from bot.cogs import command_editor


def prepare(bot):
    bot.add_cog(CustomCommands(bot))


class CustomCommands:

    def __init__(self, bot):
        self.bot = bot
        self.data = command_editor.read_json(command_editor.cmd_lib_path)["commands"]

