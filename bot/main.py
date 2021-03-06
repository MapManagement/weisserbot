from twitchio.ext import commands
from bot.utils import secrets
from bot.cogs import watchtime_counter
import asyncio


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=secrets.irc_token, client_id=secrets.client_id, nick=secrets.nickname,
                         prefix=secrets.prefix, initial_channels=secrets.channels)
        self._loop = asyncio.get_event_loop()
        self.load_cogs()

    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send(f"Hello | {ctx.message.author.name}")

    async def event_ready(self):
        print(f"Logging in as {self.nick}. Joining {self.initial_channels[0]}'s chat.\n"
              "Ready to work!\n"
              "----------------")
        await asyncio.gather(self.twitter_cycler(), watchtime_counter.WatchTime(Bot).watchtime_tracker(),
                             watchtime_counter.WatchTime(Bot).temp_watchtime_to_db())

    async def event_message(self, message):
        await self.handle_commands(message)

    async def event_usernotice_subscription(self, metadata):
        channel = metadata.channel
        user_name = metadata.user.name
        months = metadata.cumulative_months
        await channel.send(f"/me Vielen Dank für deinen Sub im {months}. Monat, @{user_name}!")

    async def twitter_cycler(self):
        channel = Bot.get_channel(self, "WeisseMoehre")
        while True:
            await asyncio.sleep(600)
            await channel.send("/me Twitter: https://twitter.com/WeisseMoehre")
            await asyncio.sleep(600)
            await channel.send("/me Instagram: https://www.instagram.com/weissemoehre/?hl=de")

    def load_cogs(self):
        extensions = ["bot.cogs.command_handler", "bot.cogs.command_editor", "bot.cogs.watchtime_counter"]
        for extension in extensions:
            Bot.load_module(self, name=extension)


if __name__ == "__main__":
    twitchbot = Bot()
    twitchbot.run()
