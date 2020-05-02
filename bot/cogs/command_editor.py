import requests
import sqlalchemy
import datetime
from bot.utils import checks, secrets
from twitchio.ext import commands

blacklisted_commands = ["new_cmd", "del_cmd", "edit_cmd", "turn_cmd", "followage", "subcount",
                        "test", "watchtime", "uptime"]


def create_db_connection():
    url = secrets.db_login
    connector = sqlalchemy.create_engine(url)
    return connector


def cursor():
    return create_db_connection()


def command_exists(name: str):
    existence_check = cursor().execute("SELECT EXISTS (SELECT name FROM commands WHERE name = %(command_name)s)",
                                       {"command_name": name}).fetchone()
    return existence_check[0]


def create_command(name: str, content: str, editor: str):
    if not command_exists(name) and name not in blacklisted_commands:
        date = datetime.datetime.today().strftime("%Y-%m-%d")
        cursor().execute(f"INSERT INTO commands (name, content, edited_at, editor, disabled) VALUES "
                         f"(%(command_name)s, %(command_content)s, %(edited_at)s, %(editor)s, %(disabled)s)",
                         {"command_name": name, "command_content": content,
                          "edited_at": date, "editor": editor, "disabled": 0})
        return f"/me Created command named '{name}'!"
    else:
        return f"/me There is already a command named '{name}'!"


def edit_command(name: str, content: str, editor: str):
    if command_exists(name):
        date = datetime.datetime.today().strftime("%Y-%m-%d")
        cursor().execute(f"UPDATE commands SET content = %(command_content)s, editor = %(command_editor)s, "
                         f"edited_at = %(command_date)s WHERE name = %(command_name)s",
                         {"command_content": content, "command_editor": editor,
                          "command_date": date, "command_name": name})
        return f"/me Edited command named '{name}'!"
    else:
        return f"/me There is no command named '{name}'!"


def delete_command(name: str):
    if command_exists(name):
        cursor().execute("DELETE FROM commands WHERE name = %(command_name)s",
                         {"command_name": name})
        return f"/me Deleted command named '{name}'!"
    else:
        return f"/me There is no command named '{name}'!"


def set_command_state(name: str, state: str):
    states = {"on": 0, "off": 1}
    if state in states.keys():
        if command_exists(name):
            cursor().execute(f"UPDATE commands SET disabled = %(command_state)s WHERE name = %(command_name)s",
                             {"command_state": states[state], "command_name": name})
            return f"/me Turned command name '{name}' {state}!"
        else:
            return f"/me There is no command named '{name}'!"
    else:
        return "/me Use 'on' for activating or 'off' for deactivating a command!"


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
            await ctx.send(result)

    @commands.command(name="edit_cmd")
    async def update_command(self, ctx, name: str, *, content: str):
        if await checks.is_mod(ctx):
            author = ctx.author.name
            result = edit_command(name, content, author)
            await ctx.send(result)

    @commands.command(name="turn_cmd")
    async def set_command_state(self, ctx, name: str, state: str):
        if await checks.is_mod(ctx):
            result = set_command_state(name, state)
            await ctx.send(result)

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
        await ctx.send(f"/me Du folgst Moehre schon ~{round(days, 2)} Tage. | @{ctx.author.name}")

    @commands.command(name="subcount", aliases=["subs"])
    async def subcount(self, ctx):
        url = "https://api.twitch.tv/kraken/channels/87252610/subscriptions"
        headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": secrets.client_id,
                   "Authorization": f"OAuth {secrets.irc_old_api}"}
        sub_request = requests.get(url, headers=headers)
        subs = sub_request.json()
        await ctx.send(f"/me Moehre hat schon {subs['_total']} Subs! | @{ctx.author.name}")

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        url = "https://api.twitch.tv/helix/streams?user_id=87252610"
        headers = {'Client-ID': secrets.twitch_api_key}
        stream_request = requests.get(url, headers=headers)
        stream = stream_request.json()["data"]

        if stream:
            datetime_now = datetime.datetime.now()
            stream_started_at = datetime.datetime.strptime(stream[0]["started_at"], "%Y-%m-%dT%H:%M:%SZ")
            raw_uptime = datetime_now - stream_started_at - datetime.timedelta(hours=2)
            total_seconds = raw_uptime.total_seconds()
            days = int(total_seconds // 86400)
            hours = int((total_seconds % 86400) // 3600)
            minutes = int(((total_seconds % 86400) % 3600) // 60)
            seconds = int(total_seconds % 60)
            uptime = f"{days} Tagen, {hours} Stunden, {minutes}" \
                     f" Minuten, {seconds} Sekunden"
            await ctx.send(f"/me Moehre ist schon seit {uptime} online | @{ctx.author.name}")
        else:
            await ctx.send(f"/me Moehre ist derzeit offline | @{ctx.author.name}")
