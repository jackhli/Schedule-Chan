import discord
import os
import psutil
import json
import time
from discord.ext import commands

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['commands', 'command'], description="Shows all commands available on the bot")
    # Command written by TheDrone7 on repl.it. I had to search around for hours trying to find something to replace the ugly help 
    # command and he had a new command updated for the new discord.py. 
    # I did make many edits but the structure of the code is still his, so thanks!
    async def help(self, ctx, cog='all'):

        # Get a list of all cogs
        cogs = [c for c in self.bot.cogs.keys()]

        # If cog is not specified by the user, we list all cogs and commands

        if cog == 'all':
            help_embed = discord.Embed(
                title='Help',
                color=0x43bab8
            )
            help_embed.set_footer(
                text=f'Requested by {ctx.message.author.name}',
                icon_url=ctx.author.avatar_url
            )
            for cog in cogs:
                # Get a list of all commands under each cog
                cog_commands = self.bot.get_cog(cog).get_commands()
                commands_list = ''
                for comm in cog_commands:
                    commands_list += f'**{comm.name}** - {comm.description}\n'
                    # Add the cog's details to the embed.
                help_embed.add_field(
                    name=cog.capitalize(),
                    value=commands_list,
                    inline=True
                )
               # Also added a blank field '\u200b' is a whitespace character.
            pass
        else:
            # If the cog was specified
            lower_cogs = [c.lower() for c in cogs]
            # If the cog actually exists.
            if cog.lower() in lower_cogs:
                help_embed = discord.Embed(
                    title=f'{cog.capitalize()} Commands',
                    color=0x43bab8
                )
                help_embed.set_footer(
                    text=f'Requested by {ctx.message.author.name}',
                    icon_url=ctx.author.avatar_url
                )
                # Get a list of all commands in the specified cog
                commands_list = self.bot.get_cog(cogs[ lower_cogs.index(cog.lower()) ]).get_commands()
                help_text=''
                # Add details of each command to the help text
                # Command Name
                # Description
                # [Aliases]
                #
                # Format
                for command in commands_list:
                    help_text += f'**{command.name}** - {command.description}\n'
                    # Also add aliases, if there are any
                    if len(command.aliases) > 0:
                        help_text += f'Aliases: `{"`, `".join(command.aliases)}`\n'
                    else:
                        # Add a newline character to keep it pretty
                        # That IS the whole purpose of custom help
                        help_text += '\n'

                        # Finally the format
                        help_text += f'Format: `@{self.bot.user.name}#{self.bot.user.discriminator}' \
                        f' {command.name} {command.usage if command.usage is not None else ""}`\n\n\n\n'

                help_embed.description = help_text
            else:
                # Notify the user of invalid cog and finish the command
                await ctx.send('Invalid catagory specified.\nUse `[p]help` to list all commands.')
                return

        await ctx.send(embed=help_embed)
        return

    @commands.command(aliases=["latency"], description="Shows the ping of the bot")
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! My ping is {round(self.bot.latency * 1000)}ms")

    @commands.command(description="Links and about page")
    async def about(self, ctx):
        about_embed = discord.Embed(title="Schedule-Chan by dinglemyberry", color=0x43bab8,
            description="**Features:**\n -Create channels that appear only on designated times.\n -Get scheduled reminders"
        )
        about_embed.add_field(
            name="🌐 Link to GitHub:",
            value="[GitHub Link](https://github.com/toucanee/Schedule-Chan)"
        )
        about_embed.add_field(
            name="👋 Discord Server:",
            value="Join the Discord Server [here](https://discord.gg/tHMNW2A)!"
        )
        
        about_embed.set_footer(text="Made by dinglemyberry#6969")


        await ctx.send(embed=about_embed)

def setup(bot):
    bot.add_cog(Information(bot))