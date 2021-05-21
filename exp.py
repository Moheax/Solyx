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
from cogs.levelup import _level_up_check_user


class exp(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

# - - - HP stuff - - - #

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def exp(self, ctx, amount: int):

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


		if userinfo["role"] == "Player":
			if amount == 1:
				times = 1

			if amount == 2 and userinfo["lvl"] >= 100:
				times = 2

			if amount == 2 and not userinfo["lvl"] >= 100:
				em = discord.Embed(description="Reach level 100+ to use 2 Exp potions!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount == 3 and userinfo["lvl"] >= 200:
				times = 3

			if amount == 3 and not userinfo["lvl"] >= 200:
				em = discord.Embed(description="Reach level 200+ to open 3 Exp potions!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount >= 4:
				em = discord.Embed(description="You cant open more then 3 Exp potions!\n Become a patreon to use more exp potions!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["role"] == "patreon2":

			times = amount

			if amount >= 4:
				em = discord.Embed(description="You cant open more then 3 Exp potions!\n Become a higher tier patreon use more exp potions!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["role"] == "patreon3":

			times = amount

			if amount >= 5:
				em = discord.Embed(description="You cant open more then 4 Exp potions!\n Become a higher tier patreon use more exp potions!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return


		if userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":

			times = amount 
		
			
			if amount >= 6:
				em = discord.Embed(description="You cant open more then 5 Exp potions!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return






		if userinfo["exp_potions"] >= amount:

			gain = 0
			for i in range(amount):
				gain = gain + random.randint(40, 75)		
			userinfo["exp"] = userinfo["exp"] + gain
			await _level_up_check_user(self, ctx, user)
				
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			userinfo["exp_potions"] = userinfo["exp_potions"] - amount
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