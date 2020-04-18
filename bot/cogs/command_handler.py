from twitchio.ext import commands
from bot.utils import secrets
import sqlalchemy


def create_db_connection():
    url = secrets.db_login
    connector = sqlalchemy.create_engine(url)
    return connector


def cursor():
    return create_db_connection()


@commands.cog()
class CommandHandler:

    def __init__(self, bot):
        self.bot = bot

    async def event_message(self, message):
        if message.content.startswith("!"):
            author = message.author.name
            command_name = message.content[1:len(message.content)]
            if not self.is_command_disabled(command_name):
                command_content = self.get_command_content(command_name)
                if command_content is not None:
                    await message.channel.send(self.command_response(command_content[0], author))

    def get_command_content(self, name: str):
        result = cursor().execute("SELECT content FROM commands WHERE name = %(command_name)s",
                                  {"command_name": name}).fetchone()
        return result

    def command_response(self, content: str, inquirer: str):
        response = f"/me {content} | @{inquirer}"
        return response

    def is_command_disabled(self, name: str):
        result = cursor().execute("SELECT disabled FROM commands WHERE name = %(command_name)s",
                                  {"command_name": name}).fetchone()
        return result is None or result[0] == 1
