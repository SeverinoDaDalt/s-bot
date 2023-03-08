import discord
from discord.ext import commands
import json
import bot_commands
import utils


def main():
    # set logging
    utils.set_logging()
    # load config
    with open("config.json", "r") as i_f:
        config = json.load(i_f)
    # start bot
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=config["command_prefix"], intents=intents)

    @bot.event
    async def on_ready():
        await bot.add_cog(bot_commands.MusicBot(bot, config))
        print(f"Logged in as {bot.user}.")

    bot.run(config["token"])


if __name__ == "__main__":
    main()
