# TODO: Create serverSettings
# TODO: Add donations aswell as their perks
# TODO: Implement analytics into extension

#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
from json import load
"""Hopefully remove one of the following:"""
from sys import exc_info
from traceback import print_exc
"""Yeah, I mean one of the above"""
from datetime import datetime
from os import environ

#Import custom libraries

#Define variables
botSettings = load(open("./bot/data/botSettings.json"))
myExtensions = [
    "extensions.basic",
    "extensions.developer",
    "extensions.search"
]

#Define functions
async def reply(ctx, string):
    await ctx.send(f"{ctx.author.mention}, {string}")

#Set up bot
bot = commands.AutoShardedBot(
    #shard_count = 4,
    command_prefix = botSettings["prefix"],
    case_insensitive = True
)
bot.remove_command("help")

#Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await reply(ctx, "You must be a server admin to do that! :warning:")
    elif isinstance(error, commands.CheckFailure):
        pass
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(error)
        await reply(ctx, f"An error occured :warning:```\n{error}```")

@bot.event
async def on_error(event_method, *args):
    if (isinstance(exc_info()[1], discord.Forbidden)):
        print(f"Ignoring 403 exception in '{event_method}'.")
    else:
        print_exc()

#Internal events
@bot.event
async def on_ready():
    bot.startTime = datetime.now().replace(microsecond=0)
    print(f"Bot ready, logged in as '{bot.user.name}#{bot.user.discriminator}'. ({bot.user.id})")
    await bot.change_presence(activity=discord.Game(f"{botSettings['prefix']}help"))

# TODO: Set up Postgres connection here

#Start up bot
if __name__ == "__main__":
    for i in myExtensions:
        bot.load_extension(i)
    bot.run(environ["BOT_TOKEN"])
