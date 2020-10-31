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



class health(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

# - - - HP stuff - - - #

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def heal(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has healed")


		battleinfo = db.battles.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		if battleinfo["battle_active"] == "True":
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["heal"]["inbattle"]["translation"])
			return
		if userinfo["health"] == 100:
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["heal"]["fullhp"]["translation"])
			return
		if userinfo["hp_potions"] > 0:

			if userinfo["questname"] == "Health acquisition" and  userinfo["questpart"] == 1:
				userinfo["questprogress"] = userinfo["questprogress"] + 1
				userinfo["questpart"] = userinfo["questpart"] + 1
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
				if userinfo["questprogress"] >= 1:
					await ctx.send("Quest Updated!")

			gain = random.randint(25, 55)
			userinfo["health"] = userinfo["health"] + gain
			if userinfo["health"] > 100:
				userinfo["health"] = 100
			userinfo["hp_potions"] = userinfo["hp_potions"] - 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["heal"]["healed"]["translation"], description="+{} HP".format(gain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["heal"]["nopotions"]["translation"], color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	@commands.group(pass_context=True, aliases=["hp"], no_pm=True, invoke_without_command=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def health(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has checked their health")


		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		em = discord.Embed(description=":heart: {}".format(userinfo["health"]), color=discord.Colour(0xffffff))
		em.set_author(name=fileIO(f"data/languages/EN.json", "load")["rpg"]["health"]["author"]["translation"].format(userinfo["name"]), icon_url=user.avatar_url)
		em.set_footer(text=fileIO(f"data/languages/EN.json", "load")["rpg"]["health"]["footer"]["translation"].format(ctx.prefix))
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

	@health.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def buy(self, ctx, *, amount : int):
		
		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has tried to buy some healthpods")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo["lvl"] <= 10:
					Sum = amount * 5
		elif userinfo["lvl"] > 10 and userinfo["lvl"] <= 30:
					Sum = amount * 10
		elif userinfo["lvl"] > 30 and userinfo["lvl"] <= 50:
					Sum = amount * 15
		elif userinfo["lvl"] > 50 and userinfo["lvl"] <= 70:
					Sum = amount * 20
		elif userinfo["lvl"] >= 71:
					Sum = amount * 25

		if amount == None:
			amount = 1

		if amount <= 0:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["health"]["negative"]["translation"], color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			return

		if userinfo["gold"] < Sum:
			needed = Sum - userinfo["gold"]
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["health"]["needgold"]["translation"].format(needed, amount), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			if userinfo["questname"] == "Health acquisition" and  userinfo["questpart"] == 0:
				userinfo["questprogress"] = userinfo["questprogress"] + amount
				userinfo["questpart"] = userinfo["questpart"] + 1
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
				if userinfo["questprogress"] >= 5:
					await ctx.send("Quest Updated!")
				pass

			userinfo["gold"] = userinfo["gold"] - Sum
			userinfo["hp_potions"] = userinfo["hp_potions"] + int(amount)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["health"]["bought"]["translation"].format(amount, Sum), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

def setup(bot):
	c = health(bot)
	bot.add_cog(c)