import json
import requests
import datetime
import os
import sqlalchemy
import datetime
from bot.utils import checks, secrets
from twitchio.ext import commands

lib_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + os.sep

blacklisted_commands = ["new_command", "new_cmd", "delete_cmd", "del_cmd", "update_command", "edit_cmd"
                        "reload_mod", "followage", "subcount", "test", "watchtime", "send_watchtime"]


def create_db_connection():
    url = secrets.db_login
    connector = sqlalchemy.create_engine(url)
    return connector


def cursor():
    return create_db_connection()


def read_json(file):
    with open(file, "r", encoding="utf8") as json_file:
        data = json.load(json_file)
        return data


def write_json(file, data):
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=4)


def create_command(name: str, content: str, creator: str):
    existence_check = cursor().execute("SELECT EXISTS (SELECT name FROM commands WHERE name = %(command_name)s)",
                                       {"command_name": str(name)}).fetchone()
    print(existence_check)
    if not existence_check[0]:
        date = datetime.datetime.today().strftime("%Y-%m-%d")
        print(date)
        cursor().execute(f"INSERT INTO commands (name, content, created_at, creator) VALUES "
                         f"(%(command_name)s, %(command_content)s, %(created_at)s, %(creator)s)",
                         {"command_name": str(name), "command_content": str(content),
                          "created_at": date, "creator": creator})
        return f"Created command named '{name}'!"
    else:
        return f"There is already a command named '{name}'!"


def edit_command(name: str, content: str):
    data = read_json(f"{lib_path}command_library.json")
    try:
        check_for_existence = data["commands"][name]
        data["commands"][name]["content"] = content
        write_json(f"{lib_path}command_library.json", data)
        return f"/me Edited command named '{name}'!", data["commands"][name]["pyfile"]
    except KeyError:
        return f"/me Couldn't find any command named '{name}'!", data["commands"][name]["pyfile"]


def delete_command(name: str):
    data = read_json(f"{lib_path}command_library.json")
    pyfile = data["commands"][name]["pyfile"]
    try:
        python_file = data["commands"][name]["pyfile"]
        del data["commands"][name]
        write_json(f"{lib_path}command_library.json", data)
        eraser = False

        with open(f"cogs/{python_file}.py", "r") as pyfile_read:
            lines = pyfile_read.readlines()
            with open(f"cogs/{python_file}.py", "w") as pyfile_write:
                for line in lines:
                    if eraser:
                        if line.endswith('")\n'):
                            eraser = False
                    else:
                        if f'    @commands.command(name="{name}")' in line:
                            eraser = True
                        else:
                            pyfile_write.write(line)
                pyfile_read.close()
                pyfile_write.close()
                return f"/me Deleted command named '{name}'!", pyfile
    except KeyError:
        return f"/me Couldn't find any command named '{name}'!", pyfile


@commands.cog()
class CommandEditor:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="new_cmd")
    async def new_command(self, ctx, name: str, *, content: str):
        if await checks.is_mod(ctx):
            author = ctx.author.name
            result = create_command(name, content, author)
            await ctx.send(result)

    @commands.command(name="del_cmd")
    async def delete_command(self, ctx, name: str):
        if await checks.is_mod(ctx):
            result = delete_command(name)
            self.bot.unload_module(f"cogs.{result[1]}")
            self.bot.load_module(f"cogs.{result[1]}")
            await ctx.send(result[0])

    @commands.command(name="edit_cmd")
    async def update_command(self, ctx, name: str, *, content: str):
        if await checks.is_mod(ctx):
            result = edit_command(name, content)
            self.bot.unload_module(f"bot.cogs.{result[1]}")
            self.bot.load_module(f"bot.cogs.{result[1]}")
            await ctx.send(result[0])

    @commands.command(name="reload_mod")
    async def reload_mod(self, ctx, module_name: str):
        if await checks.is_mod(ctx) or ctx.author.id == 151631704:
            self.bot.unload_module(f"cogs.{module_name}")
            self.bot.load_module(f"cogs.{module_name}")
            await ctx.send("/me Success!")

    @commands.command(name="followage")
    async def followage(self, ctx):
        user_id = ctx.message.author.id
        url = f"https://api.twitch.tv/kraken/users/{str(user_id)}/follows/channels/87252610"
        headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': secrets.twitch_api_key}
        follow_request = requests.get(url, headers=headers)
        follow = follow_request.json()
        followed_at = follow["created_at"]
        con_followed_at = datetime.datetime.strptime(followed_at, "%Y-%m-%dT%H:%M:%SZ")
        follow_time = datetime.datetime.now() - con_followed_at
        total_seconds = follow_time.total_seconds()
        days = total_seconds / 86400
        print(days)
        await ctx.send(f"/me Du folgst Moehre schon ~{round(days, 2)} Tage. | {ctx.author.name}")

    @commands.command(name="subcount")
    async def subcount(self, ctx):
        url = "https://api.twitch.tv/kraken/channels/87252610/subscriptions"
        headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": secrets.client_id,
                   "Authorization": f"OAuth {secrets.irc_old_api}"}
        sub_request = requests.get(url, headers=headers)
        subs = sub_request.json()
        await ctx.send(f"/me Moehre hat schon {subs['_total']} Subs! | {ctx.author.name}")
