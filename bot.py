import discord
import os
import time
from discord.ext import commands

# this specifies what extensions to load when the bot starts up
startup_extensions = ['commands']

token = open("token.txt","r").readline()
prefix = open("prefix.txt","r").readline()
client = commands.Bot(command_prefix = prefix)
client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command(aliases=['latency'])
async def ping(ctx):
    await ctx.send(f'Pong! My ping is {round(client.latency * 1000)}ms')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'commands.{extension}')

#for filename in os.listdir('./commands'):
#    if filename.endswith('.py'):
#        client.load_extension(f'cogs.{filename[:-3]}')

@client.command(pass_context=True, aliases=['commands'])
async def help(ctx):
    embed = discord.Embed(title = 'Commands', color = 0x80ceff)
    embed.add_field(name = 'Ping', value = 'Pong!', inline = True)
    embed.add_field(name = 'Setup', value = 'Configure the scheduled voice channels', inline = True)

    await ctx.send(embed=embed)

client.run(token)