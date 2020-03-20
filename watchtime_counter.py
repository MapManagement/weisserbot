from twitchio.ext import commands
import secrets
import sqlalchemy


def create_db_connection():
    url = secrets.db_login
    connector = sqlalchemy.create_engine(url)
    return connector


def cursor():
    return create_db_connection()


def insert_new_user():
    pass


def update_user():
    pass


@commands.cog()
class WatchTime:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="watchtime")
    async def send_watchtime(self, ctx):
        pass
