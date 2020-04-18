import requests
import sqlalchemy
import datetime
from bot.utils import checks, secrets
from twitchio.ext import commands

blacklisted_commands = ["new_command", "new_cmd", "delete_cmd", "del_cmd", "update_command", "edit_cmd"
                        "reload_mod", "followage", "subcount", "test", "watchtime", "send_watchtime"]


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


def create_command(name: str, content: str, creator: str):
    if not command_exists(name):
        date = datetime.datetime.today().strftime("%Y-%m-%d")
        print(date)
        cursor().execute(f"INSERT INTO commands (name, content, created_at, creator) VALUES "
                         f"(%(command_name)s, %(command_content)s, %(created_at)s, %(creator)s)",
                         {"command_name": name, "command_content": content,
                          "created_at": date, "creator": creator})
        return f"Created command named '{name}'!"
    else:
        return f"There is already a command named '{name}'!"


def edit_command(name: str, content: str):
    if command_exists(name):
        cursor().execute(f"UPDATE commands SET content = %(command_content)s WHERE name = %(command_name)s",
                         {"command_content": content, "command_name": name})
        return f"Edited command named '{name}'!"
    else:
        return f"There is no command named '{name}'!"


def delete_command(name: str):
    if command_exists(name):
        cursor().execute("DELETE FROM commands WHERE name = %(command_name)s",
                         {"command_name": name})
        return f"Deleted command named '{name}'!"
    else:
        return f"There is no command named '{name}'!"


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
            result = edit_command(name, content)
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
