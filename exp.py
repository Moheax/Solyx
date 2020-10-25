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



class exp(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

# - - - HP stuff - - - #

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 2, commands.BucketType.user)

	async def exp(self, ctx):

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
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["exp"]["inbattle"]["translation"])
			return
		if userinfo["exp_potions"] > 0:
			gain = random.randint(40, 75)
			userinfo["exp"] = userinfo["exp"] + gain
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				userinfo["exp"] = 0
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			userinfo["exp_potions"] = userinfo["exp_potions"] - 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["exp"]["expused"]["translation"], description="+{} Exp!".format(gain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["exp"]["nopotions"]["translation"], color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def exp_buy(self, ctx, *, amount : int):
		"""Buy a experience potion"""
		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has tried to buy some exppotionss")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo["lvl"] <= 10:
					Sum = amount * 50
		elif userinfo["lvl"] > 10 and userinfo["lvl"] <= 30:
					Sum = amount * 100
		elif userinfo["lvl"] > 30 and userinfo["lvl"] <= 50:
					Sum = amount * 150
		elif userinfo["lvl"] > 50 and userinfo["lvl"] <= 70:
					Sum = amount * 200
		elif userinfo["lvl"] >= 71:
					Sum = amount * 250


		if amount == None:
			amount = 1

		if amount <= 0:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["Exp"]["negative"]["translation"], color=discord.Colour(0xffffff))
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
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["Exp"]["needgold"]["translation"].format(needed, amount), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:   
			userinfo["gold"] = userinfo["gold"] - Sum
			userinfo["exp_potions"] = userinfo["exp_potions"] + int(amount)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["Exp"]["bought"]["translation"].format(amount, Sum), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

def setup(bot):
	c = exp(bot)
	bot.add_cog(c)