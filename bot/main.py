from twitchio.ext import commands
from bot.utils import secrets
import asyncio


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=secrets.irc_token, client_id=secrets.client_id, nick=secrets.nickname,
                         prefix=secrets.prefix, initial_channels=secrets.channels)
        self._loop = asyncio.get_event_loop()
        self.load_cogs()

    async def event_ready(self):
        print(f"Logging in as {self.nick}. Joining {self.initial_channels[0]}'s chat.\n"
              "Ready to work!\n"
              "----------------")
        await asyncio.gather(self.twitter_cycler(), self.insta_cycler())

    async def event_message(self, message):
        await self.handle_commands(message)

    async def event_usernotice_subscription(self, metadata):
        channel = metadata.channel
        user_name = metadata.user.name
        months = metadata.cumulative_months
        await channel.send(f"/me Vielen Dank für deinen Sub im {months}. Monat, {user_name}!")

    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send("Hello" + f" | {ctx.message.author.name}")

    async def twitter_cycler(self):
        channel = Bot.get_channel(self, "WeisseMoehre")
        while True:
            await asyncio.sleep(1200)
            await channel.send("\me Twitter: https://twitter.com/WeisseMoehre")

    async def insta_cycler(self):
        channel = Bot.get_channel(self, "WeisseMoehre")
        await asyncio.sleep(600)
        while True:
            await asyncio.sleep(1200)
            await channel.send("/me Instagram: https://www.instagram.com/weissemoehre/?hl=de")

    def load_cogs(self):
        extensions = ["bot.cogs.social_media", "bot.cogs.custom_commands", "bot.cogs.gear", "bot.cogs.rl_information",
                      "bot.cogs.software", "bot.cogs.viewer_info", "bot.cogs.command_editor",
                      "bot.cogs.watchtime_counter"]
        for extension in extensions:
            Bot.load_module(self, name=extension)


if __name__ == "__main__":
    twitchbot = Bot()
    twitchbot.run()
