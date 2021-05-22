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
		em.add_field(name="\n_ _\n**\u27a4** V2.338".format(ctx.prefix), value="Fighting of Solyx has now been rewritten and leveling up is a separate file, thus fighting should be faster and in upcoming updates you wont need to fight to get certain level checks.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** V2.337".format(ctx.prefix), value="Battles are curerently unavailable due to rewriting of fighting",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** V2.336".format(ctx.prefix), value="Fixed monster statistics visuals, Voting error popup has been fixed!.",inline=False)	
		em.add_field(name="\n_ _\n**\u27a4** V2.335".format(ctx.prefix), value="Party Extra info, a normal party can have 3 extra members that is 4 including you, tier 1 and 2 Patreon can have 5 total tier 3 and 4 Patreon can have 6 total, normal player gets 10% shared gold, tier 1: 15%, tier 2: 20%, tier 3: 25%, tier 4 30% shared gold&exp. the rewards for party message now says the total shared gold	to all members (that is normal player + tier 2 Patreon  + tier 4 Patreon)for example",inline=False)	
	
		

		await ctx.send(embed=em)


	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def add(self, ctx):
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


def setup(bot):
	n = updates(bot)
	bot.add_cog(n)