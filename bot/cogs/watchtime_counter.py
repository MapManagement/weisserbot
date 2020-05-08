from twitchio.ext import commands
from bot.utils import secrets
import sqlalchemy
import asyncio
import requests
import json


def write_json(file, data):
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=4)


def read_json(file):
    with open(file, "r", encoding="utf8") as json_file:
        data = json.load(json_file)
        return data


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
        existence_check = cursor().execute("SELECT EXISTS (SELECT name FROM users WHERE name = %(user_name)s)",
                                           {"user_name": user_name}).fetchone()
        if existence_check[0]:
            user_watchtime = cursor().execute(f"SELECT minutes FROM users WHERE name = %(user_name)s",
                                              {"user_name": user_name}).fetchone()[0]
            await ctx.send(
                f"/me You already watched {round(user_watchtime / 60, 2)} hours! | @{ctx.message.author.name}")
        else:
            await ctx.send(f"/me Sorry, couldn't find any data for {str(user_name)}! | @{ctx.message.author.name}")

    async def watchtime_tracker(self):
        url = f"https://api.twitch.tv/kraken/streams/87252610"
        headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': secrets.twitch_api_key}
        streamer_request = requests.get(url, headers=headers)
        streamer_data = streamer_request.json()
        while True:
            await asyncio.sleep(720)
            if "stream" in streamer_data.keys() and streamer_data.values() is not None:
                chatters_request = requests.get("https://tmi.twitch.tv/group/user/weissemoehre/chatters")
                chatters_data = chatters_request.json()
                chatters = chatters_data["chatters"]
                for section in chatters.values():
                    for chatter in section:
                        users = read_json("utils/temp_watchtime.json")
                        if chatter in users["users"]:
                            users["users"][str(chatter)] += 12
                        else:
                            users["users"][str(chatter)] = 12
                        write_json("utils/temp_watchtime.json", users)

    async def temp_watchtime_to_db(self):
        while True:
            await asyncio.sleep(3600)
            users = read_json("utils/temp_watchtime.json")
            cleared_json = {"users": {}}
            write_json("utils/temp_watchtime.json", cleared_json)
            for user in users["users"]:
                time = users["users"][user]
                existence_check = cursor().execute \
                    (f"SELECT EXISTS (SELECT name FROM users WHERE name = %(chatter_name)s)",
                     {"chatter_name": user}).fetchone()
                if existence_check[0]:
                    cursor().execute(f"UPDATE users SET minutes = minutes + %(new_watchtime)s WHERE name = %(chatter_name)s",
                                     {"new_watchtime": time, "chatter_name": user})
                else:
                    cursor().execute(f"INSERT INTO users (name, minutes) VALUES (%(chatter_name)s, %(new_watchtime)s)",
                                     {"new_watchtime": time, "chatter_name": user})
