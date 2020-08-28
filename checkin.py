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

		user = ctx.message.author

		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has checked in")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		#GUILD BOOST
		guild = ctx.message.guild


	
		if userinfo["role"] == "Donator":
			goldget = random.randint(360, 600)
			hpget = random.randint(3, 5)
			lbget = random.randint(5, 9)
			keyget = random.randint(5, 9)
		elif userinfo["role"] == "Subscriber":
			goldget = random.randint(450, 750)
			hpget = random.randint(6, 9)
			lbget = random.randint(7, 12)
			keyget = random.randint(7, 12)
		else:
			goldget = random.randint(200, 400)
			hpget = random.randint(2, 5)
			lbget = random.randint(3, 5)
			keyget = random.randint(3, 5)

		curr_time = time()
		delta = float(curr_time) - float(userinfo["daily_block"])
		# calulate time left
		seconds = 86400 - delta
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)

		if seconds <= 0:
			  
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["checkin"]["success"]["title"]["translation"], description="\n<:Gold:639484869809930251> **{}**\n<:HealingPotion:573577125064605706> **{}**\n<:Crate:639425690072252426> **{}**\n<:Key:573780034355986432> **{}**".format(goldget, hpget, lbget, keyget), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send("+{}<:Gold:639484869809930251>".format(int(goldget)))
				except:
					return


			userinfo["lootbag"] = userinfo["lootbag"] + lbget
			userinfo["keys"] = userinfo["keys"] + lbget
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpget
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