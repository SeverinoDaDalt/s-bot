import discord
from discord.ext import commands
import asyncio

if __name__ == "__main__":
    with open("token.txt", "r") as i_f:
        token = i_f.read()
        bot.run(token)
