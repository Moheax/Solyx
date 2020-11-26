import discord
import random
import time
import datetime
from discord.ext import commands
import asyncio
from random import choice as randchoice
from discord import Permissions
from utils.checks import staff, developer, owner
# from cogs.economy import NoAccount
from utils.db import db
from utils.dataIO import fileIO

import threading


class updates(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def updates(self, ctx):
		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		if userinfo and userinfo["blacklisted"] == "True":
			return

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has check the latests updates")
		
		em = discord.Embed(color=discord.Colour(0xffffff))
		em.set_author(name="Solyx latest updates!", icon_url=user.avatar_url)
		em.add_field(name="\n_ _\n**\u27a4** 26 Nov by TheMaksoo".format(ctx.prefix), value="Added new command -updates\nadded the command in -help and in -commands", inline=False)
		em.add_field(name="\n_ _\n**\u27a4** 26 Nov by TheMaksoo".format(ctx.prefix), value="Rewrote and updated -commands!", inline=False)
		em.add_field(name="\n_ _\n**\u27a4** 25 Nov by TheMaksoo".format(ctx.prefix), value="We have 4 new buildings.\nTo build something type -build\n**Camp:** a camp is required to make other buildings.\n\n**Sawmill:** a sawmill will be built inside your camp and \nyou get the option to create planks! (3 wood for 2 planks)(type -saw <amount> )\n\n**Masonry:** the masonry will also be built inside the camp, it also requires planks to be build!, once its build you  get the option to\nmake bricks( 5 stone for 4 bricks.)(type -mason <amount>)\n\n**Smeltery:** the smeltery will also be built inside the camp and requires planks and bricks, when build you can make Iron plates ( 5 metal for 4 iron plates)\n(type -smelt <amount>)\n\nSaw, mason and smelt have a 20 minute cooldown for patreon tier 3 and 4 its -20% and -50%\n\nThere are 3 new recources \nPlanks made from wood\nBricks made from stone\nIron plates made \nfrom metal\n\nThey will have more use in the future but for now gather them!\n\nAdded the buildings to inventory list\nAdded the new recources to the inventory supply list!!\n_ _\n", inline=False)
		em.add_field(name="\n_ _\n**\u27a4** 25 Nov by TheMaksoo".format(ctx.prefix), value="Fixed that knights cant equip maces!", inline=False)
		em.add_field(name="\n_ _\n**\u27a4** 24 Nov by TheMaksoo".format(ctx.prefix), value="Fancy update for patreons!\n\ncooldown reduction is here!\n\nLegendary has 20% cooldown reduction (for gathering)\nMythical has 50% cooldown reduction (for gathering)\n\nFor example\nnormal cooldown 10min\nlegendary cooldown 8min\nMythical cooldown 5min", inline=False)
		await ctx.send(embed=em)





def setup(bot):
	n = updates(bot)
	bot.add_cog(n)