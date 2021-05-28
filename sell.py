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

from cogs.quests import _quest_check


class sell(commands.Cog): 
	def __init__(self, bot):
		self.bot = bot



# - - - Sell - - - SELL ITEM NEED WORK

	@commands.group(name="sell", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _sell(self, ctx):

		user = ctx.message.author



		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=(0xffffff))
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			
			try:
				await ctx.send(embed=embed)
			except:
				return
		return	

	@_sell.group(name="wood", pass_context=True, invoke_without_command=True)
	async def sell_wood(self, ctx, amount: int):
		"""Sell an amount of wood or 'all'"""

		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

						
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"tried to sell some wood")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		if amount < 0:
			await ctx.send("?")
			return
		if userinfo["wood"] > 0 and userinfo["wood"] >= amount:
			if userinfo["questname"] == "Wood Trader I":
				userinfo["questprogress"] += amount
				db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
				if userinfo["questprogress"] >= 10:
					await _quest_check(self, ctx, user, userinfo)
				pass
			

			gain = amount * random.randint(2, 6)
			userinfo["gold"] += gain
			userinfo["wood"] -= amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["wood"]["sold"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["wood"]["sold"]["description"]["translation"].format(amount, gain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["wood"]["notenough"]["translation"], color=discord.Colour(0xff0000))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	@sell_wood.command(name="all", pass_context=True, no_pm=True)
	async def sell_all_wood(self, ctx):

		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

						
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"tried to sell all wood")

		amount = userinfo["wood"]
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		if amount < 0:
			await ctx.send("?")
			return
		if userinfo["wood"] > 0 and userinfo["wood"] >= amount:

			if userinfo["questname"] == "Wood Trader I":
				userinfo["questprogress"] += amount
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
				if userinfo["questprogress"] >= 10:
					await _quest_check(self, ctx, user, userinfo)
				pass

			gain = amount * random.randint(2, 6)
			userinfo["gold"] += gain
			userinfo["wood"] -= amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["wood"]["sold"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["wood"]["sold"]["description"]["translation"].format(amount, gain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["wood"]["notenough"]["translation"], color=discord.Colour(0xff0000))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	@_sell.group(name="stone", pass_context=True, invoke_without_command=True)
	async def sell_stone(self, ctx, amount: int):
		"""Sell an amount of stone or 'all'"""


		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

						
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"tried to sell some stone")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		if amount < 0:
			await ctx.send("?")
			return
		if userinfo["stone"] > 0 and userinfo["stone"] >= amount:
			if userinfo["questname"] == "Stone Trader I":
				userinfo["questprogress"] += amount
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				if userinfo["questprogress"] >= 10:
					await _quest_check(self, ctx, user, userinfo)
				pass

			gain = amount * random.randint(2, 6)
			userinfo["gold"] += gain
			userinfo["stone"] -= amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["stone"]["sold"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["stone"]["sold"]["description"]["translation"].format(amount, gain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["stone"]["notenough"]["translation"], color=discord.Colour(0xff0000))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return


	@sell_stone.command(name="all", pass_context=True, no_pm=True)
	async def sell_all_stone(self, ctx):


		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"tried to sell all stone")

		amount = userinfo["stone"]
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		if amount < 0:
			await ctx.send("?")
			return
		if userinfo["stone"] > 0 and userinfo["stone"] >= amount:

			if userinfo["questname"] == "Stone Trader I":
				userinfo["questprogress"] += amount
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
				if userinfo["questprogress"] >= 10:
					await _quest_check(self, ctx, user)

				pass

			gain = amount * random.randint(2, 6)
			userinfo["gold"] += gain
			userinfo["stone"] -= amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["stone"]["sold"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["stone"]["sold"]["description"]["translation"].format(amount, gain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["stone"]["notenough"]["translation"], color=discord.Colour(0xff0000))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return


	@_sell.group(name="metal", pass_context=True, invoke_without_command=True)
	async def sell_metal(self, ctx, amount: int):
		"""Sell an amount of metal or 'all'"""

		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"tried to sell some metal")


		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		if amount < 0:
			await ctx.send("?")
			return
		if userinfo["metal"] > 0 and userinfo["metal"] >= amount:

			if userinfo["questname"] == "Metal Trader I":
				userinfo["questprogress"] += amount
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
				if userinfo["questprogress"] >= 5:
					await _quest_check(self, ctx, user, userinfo)
				pass

			gain = amount * random.randint(5, 10)
			userinfo["gold"] += gain
			userinfo["metal"] -= amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["metal"]["sold"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["metal"]["sold"]["description"]["translation"].format(amount, gain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["metal"]["notenough"]["translation"], color=discord.Colour(0xff0000))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	@sell_metal.command(name="all", pass_context=True, no_pm=True)
	async def sell_all_metal(self, ctx):

		guild = ctx.guild

		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

						
		guild = ctx.guild

		channel = ctx.message.channel


		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"tried to sell all metal")


		amount = userinfo["metal"]
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		if amount < 0:
			await ctx.send("?")
			return
		if userinfo["metal"] > 0 and userinfo["metal"] >= amount:

			if userinfo["questname"] == "Metal Trader I":
				userinfo["questprogress"] += amount
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
				if userinfo["questprogress"] >= 5:
					await _quest_check(self, ctx, user, userinfo)
				pass

			gain = amount * random.randint(5, 10)
			userinfo["gold"] += gain
			userinfo["metal"] -= amount
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["metal"]["sold"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["metal"]["sold"]["description"]["translation"].format(amount, gain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["sell"]["metal"]["notenough"]["translation"], color=discord.Colour(0xff0000))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	
def setup(bot):
	n = sell(bot)
	bot.add_cog(n)