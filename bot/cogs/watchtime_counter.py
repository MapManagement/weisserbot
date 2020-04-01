from twitchio.ext import commands
from bot.utils import secrets
import sqlalchemy
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
        existence_check = cursor().execute("SELECT EXISTS (SELECT Name FROM user WHERE Name = %(user_name)s)",
                                           {"user_name": str(user_name)}).fetchone()
        if existence_check[0]:
            user_watchtime = cursor().execute(f"SELECT Hours FROM user WHERE Name = %(user_name)s",
                                              {"user_name": str(user_name)}).fetchone()[0]
            await ctx.send(f"/me You already watched {round(user_watchtime/60, 2)} hours!" + f" | {ctx.message.author.name}")
        else:
            await ctx.send(f"/me Sorry, couldn't find any data for {str(user_name)}!")

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
                        existence_check = cursor().execute(f"SELECT EXISTS (SELECT Name FROM user WHERE Name = %(chatter_name)s)",
                                                           {"chatter_name": str(chatter)}).fetchone()
                        if existence_check[0]:
                            cursor().execute(f"UPDATE user SET Hours = Hours + 12 WHERE Name = %(chatter_name)s",
                                             {"chatter_name": str(chatter)})
                        else:
                            cursor().execute(f"INSERT INTO user (Name, Hours) VALUES (%(chatter_name)s, 12)",
                                             {"chatter_name": str(chatter)})
