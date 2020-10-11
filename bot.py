import discord
import os
import time
import json
import asyncio
from discord.ext import commands

with open("config.json", "r") as f:
    config = json.load(f)

bot = commands.Bot(
    command_prefix = config['prefix']
    )
bot.remove_command('help')

# Startup
@bot.event
async def on_ready():
    print('Bot is ready.')

    if "streaming" in config["activity_type"]:
        await bot.change_presence(activity=discord.Streaming(name=config["activity"], url="https://www.twitch.tv/toucanee"))
        print("Status changed to streaming {}".format(config["activity"]))

    elif "playing" in config["activity_type"]:
        await bot.change_presence(activity=discord.Game(name=config["activity"]))
        print("Status changed to playing {}".format(config["activity"]))

    elif "watching" in config["activity_type"]:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config["activity"]))
        print("Status changed to watching {}".format(config["activity"]))

    elif "listening" in config["activity_type"]:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=config["activity"]))
        print("Status changed to listening to {}".format(config["activity"]))

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

try:
    bot.run(config['token'])
except Exception as err:
    print(f'Error: {err}')