from twitchio.ext import commands
import secrets
import sqlalchemy
import requests
import asyncio


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

    async def event_ready(self):
        url = f"https://api.twitch.tv/helix/streams?user_login=weissemoehre"
        headers = {'Client-ID': secrets.twitch_api_key}
        streamer_request = requests.get(url, headers=headers)
        streamer_data = streamer_request.json()
        while True:
            await asyncio.sleep(600)
            if streamer_data["data"]:
                chatters_request = requests.get("https://tmi.twitch.tv/group/user/weissemoehre/chatters")
                chatters_data = chatters_request.json()
                chatters = chatters_data["chatters"]
                for section in chatters.values():
                    for chatter in section:
                        user_request = requests.get(f"https://api.twitch.tv/helix/users?login={str(chatter)}", headers=headers)
                        user_data = user_request.json()
                        user_id =user_data["data"][0]["id"]
                        # inserting the data into the db and adding 10 points to every id that is listed
