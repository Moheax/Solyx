import discord
from discord.ext import commands

import datetime
import asyncio
import random
from random import choice as randchoice
from time import time

from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import userdata, titledata, raiddata, battledata, guilddata

class checkin(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

 # GUILD BOOST NEED TO BE ADDED REST WORKS

	@commands.command(pass_context=True, no_pm=True, aliases=["login", "daily"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def checkin(self, ctx):


		channel = ctx.message.channel
		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

		

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+user.name+"#"+user.discriminator,"Has checked in")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		#GUILD BOOST
		guild = ctx.message.guild


		if userinfo["role"] == "Subscriber":
			goldget = random.randint(150, 300) + (random.randint(150, 300)) / 50
		elif userinfo["role"] == "Donator":
			goldget = random.randint(120, 240) + (random.randint(120, 240)) / 50
		else:
			goldget = random.randint(100, 200) + (random.randint(100, 200)) / 50

		curr_time = time()
		delta = float(curr_time) - float(userinfo["daily_block"])
		# calulate time left
		seconds = 86400 - delta
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)

		if seconds <= 0:
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["checkin"]["success"]["title"]["translation"], description="<:Gold:639484869809930251> +{}".format(int(goldget)), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send("+{}<:Gold:639484869809930251>".format(int(goldget)))
				except:
					return

			userinfo["gold"] += int(goldget)
			userinfo["daily_block"] = curr_time
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

			try:
				mission = "Check-in 10 times"
				await self._guild_mission_check(user, guild, mission, 1)
			except:
				pass

			return

		else:
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["checkin"]["failed"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["checkin"]["failed"]["description"]["translation"].format(int(h), int(m), int(s)), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				msg = fileIO(f"data/languages/EN.json", "load")["rpg"]["checkin"]["failed"]["title"]["translation"]
				msg += "\n"
				msg += fileIO(f"data/languages/EN.json", "load")["rpg"]["checkin"]["failed"]["description"]["translation"].format(int(h), int(m), int(s))
				await ctx.send(msg)

def setup(bot):
	c = checkin(bot)
	bot.add_cog(c)