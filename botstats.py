import asyncio
import os

import discord
from discord.ext import commands

from utils.checks import developer
from utils.dataIO import dataIO
from utils.db import db


class botstats(commands.Cog):
    """You can display your bot stats in your game status..."""

    def __init__(self, bot):
        self.bot = bot
        self.derp = "data/botstats/json.json"
        self.imagenius = dataIO.load_json(self.derp)

    @commands.check(developer)
    @commands.group(pass_context=True)
    async def botstats(self, ctx):
        """Display Bot Stats in game status that update every 10 seconds!"""

        servercolor = ctx.author.color

        msg = ""
        if ctx.invoked_subcommand is None:
            for x in ctx.command.all_commands:
                if x not in ctx.command.all_commands[x].aliases:
                    if not ctx.command.all_commands[x].hidden:
                        msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
            embed = discord.Embed(colour=servercolor)
            embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Subcommands", value=msg, inline=False)

            try:
                await ctx.send(embed=embed)
            except:
                return
        return

    @commands.check(developer)
    @botstats.command(pass_context=True)
    async def toggle(self, ctx):
        """Turn BotStatus on and off, like a boss"""

        servers = str(len(self.bot.guilds))
        users = db.users.count()
        if self.imagenius["TOGGLE"] is False:
            self.imagenius["TOGGLE"] = True
            self.imagenius["MAINPREFIX"] = ctx.prefix
            dataIO.save_json(self.derp, self.imagenius)
            prefix = self.imagenius["MAINPREFIX"]
            await ctx.send("The botstats have been turned on!")
            await self.botstatz()
        else:
            self.imagenius["TOGGLE"] = False
            prefix = self.imagenius["MAINPREFIX"]
            dataIO.save_json(self.derp, self.imagenius)
            await ctx.send("The botstats have been turned off!")
            await self.botstatz()

    @commands.check(developer)
    @botstats.command(pass_context=True)
    async def message(self, ctx, *, message):
        """You can set the way your botstats is set!


		{0} = Bot's Prefix
		{1} = Servers
		{2} = Total Users

		Default Message: {0}help | {1} servers | {2} users
		"""

        prefix = self.imagenius["MAINPREFIX"]
        if self.imagenius["TOGGLE"] is True:
            await ctx.send("Before you change the message, turn off your bot! `{}botstats toggle`".format(prefix))
        else:
            self.imagenius["MESSAGE"] = message
            dataIO.save_json(self.derp, self.imagenius)
            await ctx.send("Congrats, you have set your message to ```{}```".format(message))

    @commands.check(developer)
    @botstats.command(pass_context=True)
    async def timeout(self, ctx, seconds: int):
        """Decide how often the BotStatus


		Default is 15
		"""

        if seconds >= 15:
            self.imagenius["SECONDS2LIVE"] = seconds
            dataIO.save_json(self.derp, self.imagenius)
            await ctx.send("Your bot status will now update every {} seconds! #BOSS".format(seconds))
        else:
            await ctx.send("NO, IT CAN'T BE UNDER 15 SECONDS. THE PEOPLE AT DISCORD WILL FREAK....")

    async def botstatz(self):
        while True:
            if self.imagenius["TOGGLE"] is True:
                status = discord.Status.dnd
                servers = str(len(self.bot.guilds))
                users = db.users.count()
                botstatus = self.imagenius["MESSAGE"]
                prefix = self.imagenius["MAINPREFIX"]
                message = botstatus.format(prefix, servers, users)
                activity = discord.Game(name=message)
                await self.bot.change_presence(status=discord.Status.online, activity=activity)
                await asyncio.sleep(self.imagenius["SECONDS2LIVE"])
            else:
                await self.bot.change_presence(status=discord.Status.online)

                await asyncio.sleep(60)
                return
        else:
            pass

    async def on_ready(self):
        if self.imagenius["TOGGLE"] is True:
            while True:
                status = discord.Status.dnd
                servers = str(len(self.bot.guild))
                users = db.users.count()
                botstatus = self.imagenius["MESSAGE"]
                prefix = self.imagenius["MAINPREFIX"]
                message = botstatus.format(prefix, servers, users)
                activity = discord.Game(name=message)
                await self.bot.change_presence(status=discord.Status.online, activity=activity)
                await asyncio.sleep(self.imagenius["SECONDS2LIVE"])
            else:
                pass
        else:
            pass

    """def get_status(self):
		typesofstatus = {
			"idle" : discord.Status.idle,
			"dnd" : discord.Status.dnd,
			"online" : discord.Status.online, 
			"invisible" : discord.Status.invisible
		}
		for server in self.bot.guild:
			member = server.me
			break
		status = "dnd"
		status = typesofstatus.get(str(status))
		return status"""


def check_folders():
    if not os.path.exists("data/botstats"):
        print("Creating the botstats folder, so be patient...")
        os.makedirs("data/botstats")
        print("Finish!")


def check_files():
    twentysix = "data/botstats/json.json"
    json = {
        "MAINPREFIX": "This can be set when starting botstats thru [p]botstats toggle",
        "TOGGLE": False,
        "SECONDS2LIVE": 15,
        "MESSAGE": "{0}help | {1} servers | {2} users"
    }

    if not dataIO.is_valid_json(twentysix):
        print("Derp Derp Derp...")
        dataIO.save_json(twentysix, json)
        print("Created json.json!")


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(botstats(bot))
