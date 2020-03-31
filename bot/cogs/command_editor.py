from twitchio.ext import commands
import json
import requests
import datetime
import os
from bot.utils import checks, secrets

cmd_lib_path = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__))) + "/command_library.json"
blacklisted_commands = ["new_command", "new_cmd", "delete_cmd", "del_cmd", "update_command", "edit_cmd"
                                                                                             "reload_mod", "followage",
                        "subcount", "test", "watchtime", "send_watchtime"]


def read_json(file):
    with open(file, "r", encoding="utf8") as json_file:
        data = json.load(json_file)
        return data


def write_json(file, data):
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=4)


def create_command(name: str, content: str):
    if not name in blacklisted_commands:
        blueprint_json = {"content": content, "pyfile": "social_media"}
        data = read_json(cmd_lib_path)
        try:
            check_for_existence = data["commands"][name]
            return "\me Command exists already!"
        except KeyError:
            data["commands"][name] = blueprint_json
            data["commands"][name]["content"] = content
            data["commands"][name]["pyfile"] = "custom_commands"
            write_json(cmd_lib_path, data)

            blueprint_cmd = f"""    @commands.command(name="{name}")\n    async def {name}(self, ctx):\n""" \
                            """        await ctx.send(self.data['""" + name + """""""']['content'] + f' | {ctx.message.author.name}')\n"""
            with open("custom_commands.py", "a") as cmd_file:
                cmd_file.write(blueprint_cmd)
                cmd_file.close()
            return f"\me Added command '{name}'!"
    else:
        return "\me Command exists already!"


def edit_command(name: str, content: str):
    data = read_json(cmd_lib_path)
    try:
        check_for_existence = data["commands"][name]
        data["commands"][name]["content"] = content
        write_json(cmd_lib_path, data)
        return f"\me Edited command named '{name}'!", data["commands"][name]["pyfile"]
    except KeyError:
        return f"\me ouldn't find any command named '{name}'!", data["commands"][name]["pyfile"]


def delete_command(name: str):
    data = read_json(cmd_lib_path)
    pyfile = data["commands"][name]["pyfile"]
    try:
        python_file = data["commands"][name]["pyfile"]
        del data["commands"][name]
        write_json("command_library.json", data)
        eraser = False

        with open(f"{python_file}.py", "r") as pyfile_read:
            lines = pyfile_read.readlines()
            with open(f"{python_file}.py", "w") as pyfile_write:
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
                return f"\me Deleted command named '{name}'!", pyfile
    except KeyError:
        return f"\me Couldn't find any command named '{name}'!", pyfile


@commands.cog()
class CommandEditor:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="new_cmd")
    async def new_command(self, ctx, name: str, *, content: str):
        if await checks.is_mod(ctx):
            result = create_command(name, content)
            self.bot.unload_module("custom_commands")
            self.bot.load_module("custom_commands")
            await ctx.send(result)

    @commands.command(name="del_cmd")
    async def delete_command(self, ctx, name: str):
        if await checks.is_mod(ctx):
            result = delete_command(name)
            self.bot.unload_module(result[1])
            self.bot.load_module(result[1])
            await ctx.send(result[0])

    @commands.command(name="edit_cmd")
    async def update_command(self, ctx, name: str, *, content: str):
        if await checks.is_mod(ctx):
            result = edit_command(name, content)
            self.bot.unload_module(result[1])
            self.bot.load_module(result[1])
            await ctx.send(result[0])

    @commands.command(name="reload_mod")
    async def reload_mod(self, ctx, module_name: str):
        if await checks.is_mod(ctx) or ctx.author.id == 151631704:
            self.bot.unload_module(module_name)
            self.bot.load_module(module_name)
            await ctx.send("\me Success!")

    @commands.command(name="followage")
    async def followage(self, ctx):
        user_id = ctx.message.author.id
        url = f"https://api.twitch.tv/helix/users/follows?from_id={str(user_id)}"
        headers = {'Client-ID': secrets.twitch_api_key}
        follow_request = requests.get(url, headers=headers)
        follow = follow_request.json()
        for streamers in follow["data"]:
            if streamers["to_id"] == "87252610":
                followed_at = streamers["followed_at"]
                con_followed_at = datetime.datetime.strptime(followed_at, "%Y-%m-%dT%H:%M:%SZ")
                follow_time = datetime.datetime.now() - con_followed_at
                total_seconds = follow_time.total_seconds()
                days = total_seconds / 86400
                await ctx.send(f"\me Du folgst Moehre schon ~{round(days, 2)} Tage. | {ctx.author.name}")

    @commands.command(name="subcount")
    async def subcount(self, ctx):
        url = f"https://api.twitch.tv/helix/subscriptions?broadcaster_id=87252610"
        headers = {"Client-ID": secrets.twitch_api_key}
        sub_request = requests.get(url, headers=headers)
        print(sub_request.content)
