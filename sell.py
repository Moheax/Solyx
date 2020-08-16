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
			gain = amount * random.randint(2, 6)
			userinfo["gold"] = userinfo["gold"] + gain
			userinfo["wood"] = userinfo["wood"] - amount
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
		if userinfo["wood"] > 0:
			gain = amount * random.randint(2, 6)
			userinfo["gold"] = userinfo["gold"] + gain
			userinfo["wood"] = userinfo["wood"] - amount
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
			gain = amount * random.randint(2, 6)
			userinfo["gold"] = userinfo["gold"] + gain
			userinfo["stone"] = userinfo["stone"] - amount
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
		if userinfo["stone"] > 0:
			gain = amount * random.randint(2, 6)
			userinfo["gold"] = userinfo["gold"] + gain
			userinfo["stone"] = userinfo["stone"] - amount
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
			gain = amount * random.randint(5, 10)
			userinfo["gold"] = userinfo["gold"] + gain
			userinfo["metal"] = userinfo["metal"] - amount
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
		if userinfo["metal"] > 0:
			gain = amount * random.randint(5, 10)
			userinfo["gold"] = userinfo["gold"] + gain
			userinfo["metal"] = userinfo["metal"] - amount
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

	@_sell.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def item(self, ctx, number:int, price:int):
		"""Sell one of your items."""

		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"tried to sell a item")


		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if number not in range(1, 24): # Max
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])
			return

		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["noitem"]["translation"])
			return

		if item["rarity"] == "Basic":
			if price < 1000:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["pricecheck"]["basicmin"]["translation"])
				return
			if price > 5000:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["pricecheck"]["basicmax"]["translation"])
				return
		if item["rarity"] == "Common":
			if price < 1000:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["pricecheck"]["commonmin"]["translation"])
				return
			if price > 10000:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["pricecheck"]["commonmax"]["translation"])
				return
		if item["rarity"] == "Rare":
			if price < 5000:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["pricecheck"]["raremin"]["translation"])
				return
			if price > 50000:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["pricecheck"]["raremax"]["translation"])
				return
		if item["rarity"] == "Legendary":
			if price < 10000:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["pricecheck"]["legendarymin"]["translation"])
				return
			if price > 500000:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["pricecheck"]["legendarymax"]["translation"])
				return
		if item["rarity"] == "Mythical":
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["pricecheck"]["mythical"]["translation"])
				return

		try:
			marketinfo = db.market.find_one({ "_id": "{}".format(user.id) })
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["alreadylisted"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["alreadylisted"]["description"]["translation"], color=discord.Colour(0xffffff))
			em.add_field(name="Item info:", value=fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["alreadylisted"]["value"]["translation"].format(marketinfo["refinement"], marketinfo["name"], marketinfo["rarity"], marketinfo["price"]), inline=False)
			em.set_footer(text=fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["alreadylisted"]["footer"]["translation"])
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
			if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await self._create_item(user.id, item["name"], item["rarity"], item["stats_min"], item["stats_max"], item["refinement"], price, item["type"], item["image"], item["description"])
				em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["listed"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["listed"]["description"]["translation"].format(item["refinement"], item["name"], item["rarity"], price), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
					return
				except:
					try:
						msg = fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["listed"]["title"]["translation"]
						msg += "\n"
						msg += fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["listed"]["description"]["translation"].format(item["refinement"], item["name"], item["rarity"], price)
						await ctx.send(msg)
						return
					except:
						return

			else:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["notselling"]["translation"])
					return
				except:
					return

		except:
			pass

		userinfo["inventory"].remove(item)
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		await self._create_item(user.id, item["name"], item["rarity"], item["stats_min"], item["stats_max"], item["refinement"], price, item["type"], item["image"], item["description"])
		em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["listed"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["listed"]["description"]["translation"].format(item["refinement"], item["name"], item["rarity"], price), color=discord.Colour(0xffffff))
		try:
			await ctx.send(embed=em)
		except:
			try:
				msg = fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["listed"]["title"]["translation"]
				msg += "\n"
				msg += fileIO(f"data/languages/EN.json", "load")["market"]["sell"]["listed"]["description"]["translation"].format(item["refinement"], item["name"], item["rarity"], price)
				await ctx.send(msg)
			except:
				pass

def setup(bot):
	n = sell(bot)
	bot.add_cog(n)