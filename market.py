#from cogs.utils.chat_formatting import pagify

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
import math
from utils import checks
import os, re, aiohttp
import platform
import string
import operator
import textwrap



class market(commands.Cog): 
	def __init__(self, bot):
		self.bot = bot

	async def check_answer(self, ctx, valid_options):

		answer = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)

		if answer.content.lower() in valid_options:
			return answer.content

		elif answer.content in valid_options:
			return answer.content

		elif answer.content.upper() in valid_options:
			return answer.content

		else:
			return #await self.check_answer(ctx, valid_options)  //  This could keep a check loop going

	@commands.group(pass_context = True, aliases=["auction"], no_pm=True, invoke_without_command=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def market(self, ctx, *options):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"checked market listings")

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		auctioninfo = db.market.find_one({ "_id": user.id })
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		items = []
		for item in db.market.find({}):
			try:
				items.append((item["name"], item["type"], item["rarity"], item["stats_min"], item["stats_max"], item["refinement"], item["price"], item["_id"], item["description"], item["image"]))
			except:
				pass
		sorted_list = sorted(items, key=operator.itemgetter(1), reverse=True)
		# multiple page support
		page = 1
		per_page = 10
		pages = math.ceil(len(sorted_list)/per_page)
		for option in options:
			if str(option).isdigit():
				if page >= 1 and int(option) <= pages:
					page = int(str(option))
				else:
					await ctx.send("<:Solyx:560809141766193152> **| Not a valid page number.**")
					return
				break

		msg = ""
		rank = 1 + per_page*(page-1)
		start_index = per_page*page - per_page
		end_index = per_page*page

		print("Market items: {}".format(len(sorted_list)))

		for itemx in sorted_list[start_index:end_index]:
			if itemx[2] == "mythical" or itemx[2] == "Mythical":
				rarityy = "<:Mythical:573784881386225694>"
			elif itemx[2] == "legendary" or itemx[2] == "Legendary":
				rarityy = "<:Legendary:639425368167809065>"
			elif itemx[2] == "rare" or itemx[2] == "Rare":
				rarityy = "<:Rare:573784880815538186>"
			elif itemx[2] == "uncommon" or itemx[2] == "Uncommon":
				rarityy = "<:Uncommon:641361853817159685>"
			elif itemx[2] == "common" or itemx[2] == "Common":
				rarityy = "<:Common:573784881012932618>"
			elif itemx[2] == "basic" or itemx[2] == "Basic":
				rarityy = "<:Basic:641362343338442762>"

			msg += '{}**{} {}** ({}-{}) <:Gold:639484869809930251>{} ID: `{}`\n'.format(rarityy, itemx[5], itemx[0], itemx[3], itemx[4], itemx[6], itemx[7])
			rank += 1
		
		em = discord.Embed(description=msg, colour=discord.Colour(0xffffff))
		em.set_author(name="Solyx Market", icon_url = self.bot.user.avatar_url)
		em.add_field(name="<:ShieldBug:649157223905492992>", value="Market is currently bugged, buying items and items dont always show up.", inline=False)
#		em.add_field(name="Number		   Item\n", value=msg)
		em.set_footer(text="Page {}/{} | Use {}market buy [id] to buy an item!".format(page, pages, ctx.prefix))
		await ctx.send(embed = em)

	@market.command(pass_context = True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def sell(self, ctx, number:int, price:int):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"sold a item to the market")

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if number not in range(1, 24): # Max
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["itemnotexist"]["translation"])
			return

		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["noitem"]["translation"])
			return

		if item["rarity"] == "Basic":
			if price < 1000:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["pricecheck"]["basicmin"]["translation"])
				return
			if price > 5000:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["pricecheck"]["basicmax"]["translation"])
				return
		if item["rarity"] == "Common":
			if price < 1000:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["pricecheck"]["commonmin"]["translation"])
				return
			if price > 10000:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["pricecheck"]["commonmax"]["translation"])
				return
		if item["rarity"] == "Rare":
			if price < 5000:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["pricecheck"]["raremin"]["translation"])
				return
			if price > 50000:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["pricecheck"]["raremax"]["translation"])
				return
		if item["rarity"] == "Legendary":
			if price < 10000:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["pricecheck"]["legendarymin"]["translation"])
				return
			if price > 500000:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["pricecheck"]["legendarymax"]["translation"])
				return
		if item["rarity"] == "Mythical":
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["pricecheck"]["mythical"]["translation"])
				return

		try:
			marketinfo = db.market.find_one({ "_id": "{}".format(user.id) })
			em = discord.Embed(title=fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["alreadylisted"]["title"]["translation"], description=fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["alreadylisted"]["description"]["translation"], color=discord.Colour(0xffffff))
			em.add_field(name="Item info:", value=fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["alreadylisted"]["value"]["translation"].format(marketinfo["refinement"], marketinfo["name"], marketinfo["rarity"], marketinfo["price"]), inline=False)
			em.set_footer(text=fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["alreadylisted"]["footer"]["translation"])
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
			if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":
				db.market.remove({"_id": "{}".format(user.id)}, 1)
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await self._create_item(user.id, item["name"], item["rarity"], item["stats_min"], item["stats_max"], item["refinement"], price, item["type"], item["image"], item["description"])
				em = discord.Embed(title=fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["listed"]["title"]["translation"], description=fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["listed"]["description"]["translation"].format(item["refinement"], item["name"], item["rarity"], price), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
					return
				except:
					try:
						msg = fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["listed"]["title"]["translation"]
						msg += "\n"
						msg += fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["listed"]["description"]["translation"].format(item["refinement"], item["name"], item["rarity"], price)
						await ctx.send(msg)
						return
					except:
						return

			else:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["notselling"]["translation"])
					return
				except:
					return

		except:
			pass

		userinfo["inventory"].remove(item)
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		await self._create_item(user.id, item["name"], item["rarity"], item["stats_min"], item["stats_max"], item["refinement"], price, item["type"], item["image"], item["description"])
		em = discord.Embed(title=fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["listed"]["title"]["translation"], description=fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["listed"]["description"]["translation"].format(item["refinement"], item["name"], item["rarity"], price), color=discord.Colour(0xffffff))
		try:
			await ctx.send(embed=em)
		except:
			try:
				msg = fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["listed"]["title"]["translation"]
				msg += "\n"
				msg += fileIO(f"data/languages/{language}.json", "load")["market"]["sell"]["listed"]["description"]["translation"].format(item["refinement"], item["name"], item["rarity"], price)
				await ctx.send(msg)
			except:
				pass

	@market.command(pass_context = True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def buy(self, ctx, idmarket:int):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Bought a item from the market")


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
		idmarket = int
		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if len(userinfo["inventory"]) >= 24:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["fullinv"]["translation"])
			except:
				return
			return

		marketinfo = db.market.find_one({ "marketid": idmarket})
		print(marketinfo["price"])

		existcheck = db.market.count_documents({"_id": idmarket})
		

		if str(idmarket) == str(user.id):
			await ctx.send("<:Solyx:560809141766193152> **| You can't buy your own items!**")
			return

		if not userinfo["gold"] >= marketinfo["price"]:
			neededgold = marketinfo["price"] - userinfo["gold"]
			await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to buy this item!**".format(neededgold))
			return

		itemobj = {"name": marketinfo["name"], "type": marketinfo["type"], "rarity": marketinfo["rarity"], "stats_min": marketinfo["stats_min"], "stats_max": marketinfo["stats_max"], "refinement": marketinfo["refinement"], "description": marketinfo["description"], "image": marketinfo["image"]}
		userinfo["inventory"].append(itemobj)
		userinfo["gold"] = userinfo["gold"] - marketinfo["price"]
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		sellerinfo = db.users.find_one({ "_id": "{}".format(id) })
		sellerinfo["gold"] = sellerinfo["gold"] + marketinfo["price"]
		db.users.replace_one({ "_id": "{}".format(id) }, sellerinfo, upsert=True)

		"""maxamt = db.market.count()
		if number not in range(1, str(maxamt)): # Max
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["itemnotexist"]["translation"])
			return"""

		em = discord.Embed(title="Item bought:", description="{} {} ({}) for {} <:Gold:639484869809930251>".format(marketinfo["refinement"], marketinfo["name"], marketinfo["rarity"], marketinfo["price"]), color=discord.Colour(0xffffff))

		if not marketinfo["image"] == "None":
			em.set_thumbnail(url=marketinfo["image"])
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send("{} {} ({}) for {} <:Gold:639484869809930251>".format(marketinfo["refinement"], marketinfo["name"], marketinfo["rarity"], marketinfo["price"]))
			except:
				pass

		try:
			em = discord.Embed(description="{} {} ({}) for {} <:Gold:639484869809930251>".format(marketinfo["refinement"], marketinfo["name"], marketinfo["rarity"], marketinfo["price"]), color=discord.Colour(0xffffff))
			em.set_author(name="Item Sold", icon_url="https://i.imgur.com/p1Clibi.png")
			if not marketinfo["image"] == "None":
				em.set_thumbnail(url=marketinfo["image"])
			await self.bot.send_message(discord.User(id=marketinfo["_id"]), embed=em)
		except:
			pass

		db.market.remove({"_id": "{}".format(id)}, 1)

	@commands.group(name="buy", pass_context=True, no_pm=True)
	async def normal_buy(self, ctx):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return

		server = ctx.guild
		channel = ctx.channel
		servercolor = ctx.author.color

		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=servercolor)
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			
			try:
				await ctx.send(embed=embed)
			except:
				return
		return


	@normal_buy.command(pass_context = True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def item(self, ctx, id:int):
		"""Buy an item from the market"""

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"bought a item from the market")
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if len(userinfo["inventory"]) >= 24:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["fullinv"]["translation"])
			except:
				return
			return

		marketinfo = db.market.find_one({ "_id": "{}".format(id)})

		existcheck = db.market.count_documents({"_id": "{}".format(id)})


		if str(id) == str(user.id):
			await ctx.send("<:Solyx:560809141766193152> **| You can't buy your own items!**")
			return

		if not int(userinfo["gold"]) >= int(marketinfo["price"]):
			neededgold = int(marketinfo["price"]) - int(userinfo["gold"])
			await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to buy this item!**".format(neededgold))
			return

		itemobj = {"name": marketinfo["name"], "type": marketinfo["type"], "rarity": marketinfo["rarity"], "stats_min": marketinfo["stats_min"], "stats_max": marketinfo["stats_max"], "refinement": marketinfo["refinement"], "description": marketinfo["description"], "image": marketinfo["image"]}
		userinfo["inventory"].append(itemobj)
		userinfo["gold"] = userinfo["gold"] - int(marketinfo["price"])
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		sellerinfo = db.users.find_one({ "_id": "{}".format(id) })
		sellerinfo["gold"] = sellerinfo["gold"] + int(marketinfo["price"])
		db.users.replace_one({ "_id": "{}".format(id) }, sellerinfo, upsert=True)

		"""maxamt = db.market.count()
		if number not in range(1, str(maxamt)): # Max
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["itemnotexist"]["translation"])
			return"""

		em = discord.Embed(title="Item bought:", description="{} {} ({}) for {} <:Gold:639484869809930251>".format(marketinfo["refinement"], marketinfo["name"], marketinfo["rarity"], marketinfo["price"]), color=discord.Colour(0xffffff))

		if not marketinfo["image"] == "None":
			em.set_thumbnail(url=marketinfo["image"])
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send("{} {} ({}) for {} <:Gold:639484869809930251>".format(marketinfo["refinement"], marketinfo["name"], marketinfo["rarity"], marketinfo["price"]))
			except:
				pass

		try:
			em = discord.Embed(description="{} {} ({}) for {} <:Gold:639484869809930251>".format(marketinfo["refinement"], marketinfo["name"], marketinfo["rarity"], marketinfo["price"]), color=discord.Colour(0xffffff))
			em.set_author(name="Item Sold", icon_url="https://i.imgur.com/p1Clibi.png")
			if not marketinfo["image"] == "None":
				em.set_thumbnail(url=marketinfo["image"])
			await self.bot.send_message(discord.User(id=marketinfo["_id"]), embed=em)
		except:
			pass

		db.market.remove({"_id": "{}".format(id)}, 1)

	@normal_buy.command(pass_context=True, no_pm=True, aliases=["healingpotion", "healingpotions", "hps"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def hp(self, ctx, *, amount : int):
		"""Buy a healing potion"""
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


	# handles market item creation
	async def _create_item(self, userid, itemname, rarity, stats_min, stats_max, refinement, price, type, image, description):
		try:
			iteminfo = db.market.find_one({'_id':userid})
			if not iteminfo:
				new_account = {
					"_id" : userid,
					"name": itemname,
					"rarity": rarity,
					"stats_min": stats_min,
					"stats_max": stats_max,
					"refinement": refinement,
					"price": price,
					"type": type,
					"image": image,
					"description": description
				}
				db.market.insert_one(new_account)

			iteminfo = db.market.find_one({'_id':userid})
		except AttributeError as e:
			pass

def setup(bot):
	n = market(bot)
	bot.add_cog(n)