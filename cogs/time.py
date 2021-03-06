import discord
import time
import json
import requests
import datetime
import os
import asyncio
import re
from datetime import datetime
from datetime import date
from discord.ext import commands
import json

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=["timezone"], description="Shows the time in a specific place")
    async def time(self, ctx, *, place=None):
        if place:
            tapi = requests.get(f"https://api.ipgeolocation.io/timezone?apiKey=df9f9e6db5a7484f895856ba80a017bd&location={place}")
            timefull = tapi.json()
            datet = (timefull["date"])
            time = (timefull["time_12"])
            stripdate = datetime.strptime(datet, '%Y-%m-%d')
            time_embed = discord.Embed(
                title=f"Current Time in {place.title()}",
                color=0x43bab8,
                description=f"The current time in `{place.title()}` is:\n**{time}**\n**{stripdate.strftime('%A')}, {stripdate.strftime('%B')} {stripdate.strftime('%d')}, {stripdate.strftime('%Y')}**"
            )
            time_embed.set_footer(
                text=f'Requested by {ctx.message.author.name}',
                icon_url=ctx.author.avatar_url
            )
        else:
            localTime = datetime.now()
            localDate = date.today()
            stlocalTime = localTime.strftime("%#I:%M:%S %p")
            time_embed = discord.Embed(
                title=f"Current Time",
                color=0x43bab8,
                description=f"The current time is:\n**{stlocalTime}**\n**{localDate.strftime('%A')}, {localDate.strftime('%B')} {localDate.strftime('%d')}, {localDate.strftime('%Y')}**"
            )
            time_embed.set_footer(
                text=f'Requested by {ctx.message.author.name}',
                icon_url=ctx.author.avatar_url
            )
        await ctx.send(embed=time_embed)
        return
    
    @commands.command(aliases=["remindme", "reminder"], description="DM's you a set message at a given time")
    async def remind(self, ctx, time=None, *, message=None):
        user = ctx.message.author
        m = re.search(r"\d+$", time)
        error = discord.Embed(
            color=0xff4f4f
        )
        embedEnd = discord.Embed(
            color=0x43bab8
        )
        embedEnd2 = discord.Embed(
            color=0x43bab8
        )
        if time == None:
            error.add_field(
                name="Error",
                value="Please enter the command in the format of:\n`[p]remind [time(s, m, h, d)] [message]`."
            )
            await ctx.send(embed=error)
            return
        if m is not None:
            error.add_field(
                name="Error",
                value="Please enter the command in the format of:\n`[p]remind [time(s, m, h, d)] [message]`."
            )
            await ctx.send(embed=error)
            return
        if time.lower().endswith("s"):
            seconds = int(time[:-1])
            measure = f"{int(time[:-1])} seconds"
        elif time.lower().endswith("m"):
            seconds = int(time[:-1]) * 60
            measure = f"{int(time[:-1])} minutes"
        elif time.lower().endswith("h"):
            seconds = int(time[:-1]) * 60 * 60
            measure = f"{int(time[:-1])} hours"
        elif time.lower().endswith("d"):
            seconds = int(time[:-1]) * 60 * 60 * 24
            measure = f"{int(time[:-1])} days"
        if seconds == 0:
            error.add_field(
                name="Error",
                value=f"Please specify a valid number."
            )
            await ctx.send(embed=error)
            return
        if seconds > 5184000:
            error.add_field(
                name="Error",
                value=f"You specified too long of a duration.\n Please specify a value less than `2 Months` or `60 Days`."
            )
            await ctx.send(embed=error)
            return
        if message:
            embedEnd.add_field(
                name="Reminder",
                value=f"Alright, I'll remind you about `{message}` in `{measure}`."
            )
            await ctx.send(embed=embedEnd)
            await asyncio.sleep(seconds)
            embedEnd2.add_field(
                name="Reminder",
                value=f"Hello! You asked me to remind you about `{message}` in `{measure}`."
            )
            await user.send(embed=embedEnd2)
            return
        elif message == None:
            embedEnd.add_field(
                name="Reminder",
                value=f"Alright, I'll remind you in `{measure}`."
            )
            await ctx.send(embed=embedEnd)
            await asyncio.sleep(seconds)
            embedEnd2.add_field(
                name="Reminder",
                value=f"Hello! You asked me to remind you in `{measure}`."
            )
            await user.send(embed=embedEnd2)
            return

    @commands.command(aliases=["schedulechan", "sc"])
    async def schechan(self, ctx):
        await ctx.message.delete()
        errorEmbed = discord.Embed(
            color=0xff4f4f
        )
        
        # 1st Setup Question
        setupEmbed1 = discord.Embed(
            title="Setup",
            color=0x43bab8,
            description="Hey! What channel would you like to schedule?"
        )
        sentSetupEmbed1 = await ctx.send(embed=setupEmbed1)
        try:
            channel = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=15)
        except asyncio.TimeoutError:
            await sentSetupEmbed1.delete()
            errorEmbed.add_field(
                name="Error",
                value="You didn't respond in time!"
            )
            await ctx.send(embed=errorEmbed, delete_after=5.0)
        else:
            # 2nd Setup Question
            # await ctx.send(f'Hi {channel.content}!')
            setupEmbed2 = discord.Embed(
                title="Setup",
                color=0x43bab8,
                description="What time do you want this channel to appear?\n**Please use the format of hh:mm AM/PM**"
            )
            sentSetupEmbed2 = await ctx.send(embed=setupEmbed2)
            try:
                time = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=15)
            except asyncio.TimeoutError:
                await sentSetupEmbed1.delete()
                errorEmbed.add_field(
                    name="Error",
                    value="You didn't respond in time!"
                )
                await ctx.send(embed=errorEmbed, delete_after=5.0)
            else:
                setupEmbed3 = discord.Embed(
                    title="Setup",
                    color=0x43bab8,
                    description="What time do you want this channel to disappear?\n**Please use the format of hh:mm AM/PP**"
                )

def setup(bot):
    bot.add_cog(Time(bot))