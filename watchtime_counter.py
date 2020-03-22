from twitchio.ext import commands
import secrets
import sqlalchemy
import random
import asyncio
import requests


def create_db_connection():
    url = secrets.db_login
    connector = sqlalchemy.create_engine(url)
    return connector


def cursor():
    return create_db_connection()


@commands.cog()
class WatchTime:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="watchtime")
    async def send_watchtime(self, ctx):
        user_name = ctx.message.author.name
        existance_check = cursor().execute(f"SELECT EXISTS (SELECT Name FROM user WHERE Name = '{str(user_name)}')").fetchone()
        if existance_check[0]:
            user_watchtime = cursor().execute(f"SELECT Hours FROM user WHERE Name = '{str(user_name)}'").fetchone()[0]
            await ctx.send(f"You already watched {user_watchtime} hours!")
        else:
            await ctx.send(f"Sorry, couldn't find any data for {user_name}!")

    async def event_ready(self):
        url = f"https://api.twitch.tv/helix/streams?user_login=weissemoehre"
        headers = {'Client-ID': secrets.twitch_api_key}
        streamer_request = requests.get(url, headers=headers)
        streamer_data = streamer_request.json()
        while True:
            await asyncio.sleep(720)
            if streamer_data["data"]:
                chatters_request = requests.get("https://tmi.twitch.tv/group/user/weissemoehre/chatters")
                chatters_data = chatters_request.json()
                chatters = chatters_data["chatters"]
                for section in chatters.values():
                    for chatter in section:
                        # inserting the data into the db and adding 0.2 hours to every id that is listed
                        existance_check = cursor().execute(f"SELECT EXISTS (SELECT Name FROM user WHERE Name = '{str(chatter)}')").fetchone()
                        if existance_check[0]:
                            cursor().execute(f"UPDATE user SET (Hours = Hours + 0.2) WHERE Name = '{str(chatter)}'")
                        else:
                            cursor().execute(f"INSERT INTO user (Name, Hours) VALUES ('{str(chatter)}', 0")

