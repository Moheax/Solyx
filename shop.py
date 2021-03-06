import discord
import platform, asyncio, string, operator, textwrap
import os, re, aiohttp
import time
import json
import random
import math
import logging
import datetime
from discord.ext import commands
from discord.utils import find
from utils.dataIO import fileIO
from utils import checks
from utils.chat_formatting import pagify
from random import choice as randchoice
from utils.db import db
from utils.defaults import userdata, titledata
try:
	import scipy
	import scipy.misc
	import scipy.cluster
except:
	pass
from cogs.quests import _quest_check

#         weapons_list = ["hp","Hp", "Calcite Staff", "Glyphic Bow", "Abaddon Dagger", "Sclerite Sword", "Iron Greatsword", "Rusted Short Sword", "Staff of Milos", "Obsidian Longbow", "Verdant Bow", "Oblivion", "Reinforced Crossbow", "Etched Long Bow", "Mithril Sword", "Spiked Mace", "Curved Dagger", "Tomb of Water", "Rusted Crossbow", "Makeshift Short Bow", "Iron Mace", "Iron Claws", "Concealed Blade", "Tomb of Fire", "Scroll of Blizzards"]

class shop(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	async def check_answer(self, ctx, valid_options):
		def pred(m):
			return m.author == ctx.author and m.channel == ctx.channel
		answer = await self.bot.wait_for('message', check=pred)

		if answer.content.lower() in valid_options:
			return answer.content
		elif answer.content in valid_options:
			return answer.content
		elif answer.content.upper() in valid_options:
			return answer.content
		else:
			return #await self.check_answer(ctx, valid_options)  //  This could keep a check loop going

	async def check_answer_other_user(self, ctx, user, valid_options):
		def pred(m):
			return m.author == user and m.channel == ctx.channel
		answer = await self.bot.wait_for('message', check=pred)

		if answer.content.lower() in valid_options:
			return answer.content
		elif answer.content in valid_options:
			return answer.content
		elif answer.content.upper() in valid_options:
			return answer.content
		else:
			return #await self.check_answer(ctx, valid_options)  //  This could keep a check loop going



	@commands.group(name="shop", pass_context=True, no_pm=True)
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def shop(self, ctx):
		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color
		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=guildcolor)
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			
			try:
				await ctx.send(embed=embed)
			except:
				return
		return
		

	@shop.command(name="buy", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def buy(self, ctx, *, item):

		"""| -shop buy <item Name>"""


		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Bought something from the shop!")

		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

		bow = ["Archer", "Ranger", "Assassin", "Night Assassin", "Skilled Ranger"]
		sword = ["Paladin", "Samurai", "Knight", "Master Samurai", "Grand Paladin"]
		dagger = ["Thief", "Mesmer", "Rogue", "High rogue", "Adept Mesmer"]
		staff = ["Mage", "Elementalist", "Necromancer", "Developed Necromancer", "Adequate Elementalist", "Ranger","Skilled Ranger"]
		light = ["Mesmer", "Assassin", "Thief", "Archer", "Adept Mesmer", "Night Assassin"]
		medium = ["Samurai", "Mage", "Necromancer", "Rogue", "High rogue", "Developed Necromancer", "Master Samurai"]
		heavy = ["Paladin", "Knight", "Elementalist", "Ranger", "Adequate Elementalist", "Grand Paladin", "Skilled Ranger"]

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
		if len(userinfo["inventory"]) >= 25:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["general"]["fullinv"]["translation"], color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		if not len(userinfo["inventory"]) >= 25:
			if item == "Sclerite Sword" or item == "sclerite sword":
				itemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Iron Greatsword" or item == "iron greatsword":
				itemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Abaddon Dagger" or item == "abaddon dagger":
				itemobj = {"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Rusted Short Sword" or item == "rusted short sword":
				itemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Verdant Bow" or item == "verdant bow":
				itemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Obsidian Longbow" or item == "obsidian longbow":
				itemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Etched Longbow" or item == "etched longbow" or item == "Etched Long Bow" or item == "etched long bow":
				itemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Mithril Sword" or item == "mithril sword":
				itemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Spiked Mace" or item == "spiked mace":
				itemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Curved Dagger" or item == "curved dagger":
				itemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Tomb of Water" or item == "tomb of water":
				itemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Makeshift Shortbow" or item == "makeshift shortbow":
				itemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Iron Mace" or item == "iron mace":
				itemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Iron Claws" or item == "iron claws":
				itemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Concealed Blade" or item == "concealed blade":
				itemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Tomb of Fire" or item == "tomb of fire":
				itemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Scroll of Blizzards" or item == "scroll of blizzards":
				itemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Glyphic Bow" or item == "glyphic bow":
				itemobj = {"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Reinforced Crossbow" or item == "reinforced crossbow":
				itemobj = {"name": "Reinforced Crossbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Oblivion" or item == "oblivion":
				itemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Staff of Milos" or item == "staff of milos":
				itemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Calcite Staff" or item == "calcite staff":
				itemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)



	# - - - - - Armor - - - - -

			elif item == "Leather Armor" or item == "leather armor":
				itemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "price": 1000, "description": "?!", "image": "None"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Banded Armor" or item == "banded armor":
				itemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "price": 1000, "description": "?!", "image": "None"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Wolf Fur" or item == "wolf fur":
				itemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "price": 2300, "description": "?!", "image": "None"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Pit Fighter Armor" or item == "pit fighter armor":
				itemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "price": 1000, "description": "?!", "image": "None"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Chainmail Armor" or item == "chainmail armor":
				itemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "price": 1000, "description": "?!", "image": "None"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Enchanted Steel Armor" or item == "enchanted steel armor":
				itemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "price": 2300, "description": "?!", "image": "None"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Barbaric Armor" or item == "barbaric armor":
				itemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "price": 1000, "description": "?!", "image": "None"}
				cost = 2000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Branded Metal Armor" or item == "branded metal armor":
				itemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "price": 2300, "description": "?!", "image": "None"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)

			elif item == "Iron Armor" or item == "iron armor":
				itemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "price": 2300, "description": "?!", "image": "None"}
				cost = 7000
				value = cost - userinfo["gold"]
				if userinfo["gold"] < cost:
					em = discord.Embed(description="You need {} more gold to buy this item.".format(value), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				else:
					userinfo["gold"] = userinfo["gold"] - cost
					userinfo["inventory"].append(itemobj)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					em = discord.Embed(description="You bought the item for {} gold.".format(cost), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
			

			

			

	@shop.command(name="sell", pass_context=True)
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def sell(self, ctx, *args:int):
		"""| -shop sell <number>"""


		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Sold something in the shop!")

		
		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
	
		amount = len(args)
		if not amount:
			em = discord.Embed(title= "how to use",description="{}shop sell <number> or {}shop sell <number1> <number2>\n{}shop sell 1 2 3\nyou can't type 1 4 2 this will sell unwanted items.\nPatreons can sell up to 5 items".format(ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if userinfo["role"] == "Player":			

			if amount == 2 and not userinfo["lvl"] >= 100:
				em = discord.Embed(description="Reach level 100+ to sell 2 items in shop!\nOr become a patreon to sell more items in shop.", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount == 3 and not userinfo["lvl"] >= 200:
				em = discord.Embed(description="Reach level 200+ to sell 3 items in shop!\nOr become a patreon to sell more items in shop.", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount >= 4:
				em = discord.Embed(description="You cant sell more then 3 items in shop.\n Become a patreon to sell more items in shop.", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["role"] == "patreon2":

			if amount >= 4:
				em = discord.Embed(description="You cant sell more then 3 items in shop.\n Become a higher tier patreon to sell more items in shop.", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["role"] == "patreon3":

			if amount >= 5:
				em = discord.Embed(description="You cant sell more then 4 items in shop.\n Become a higher tier patreon to sell more items in shop.", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return


		if userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
			
			if amount >= 6:
				em = discord.Embed(description="You cant sell more then 5 items in shop.", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		number = 1
		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["noiteminslot"]["translation"])
			return
		amount = 1
		
			
		list = "You sold\n\n"
		for x in args:
			
			number -= amount
			number += x
			
			
			if number not in range(1, 26): # Max
				return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])

			try:
				item = userinfo["inventory"][number-1]
			except:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["noiteminslot"]["translation"])
				return
			number -= x

		
			itemname = item["name"]
			itemrarity = item["rarity"]

			if itemname == "Sclerite Sword":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Iron Greatsword" :
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Abaddon Dagger":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Rusted Short Sword":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Verdant Bow":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Obsidian Longbow":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Etched Longbow":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Reinforced Crossbow":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Mithril Sword":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Spiked Mace":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Curved Dagger":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Tomb of Water":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Makeshift Shortbow":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Iron Mace":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Iron Claws":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Concealed Blade":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Tomb of Fire":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Scroll of Blizzards":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Glyphic Bow":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Oblivion":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Staff of Milos":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Calcite Staff":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Starter Bow":
				cost = 200		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Starter Sword":
				cost = 200		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Starter Staff":
				cost = 200		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Starter Dagger":
				cost = 200		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Excalibur":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return
			elif itemname == "Twilight":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return

			elif itemname == "Devil's Kiss":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return

			elif itemname == "Hawkeye":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return

			elif itemname == "Solarflare":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return

			elif itemname == "Thunderguard":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return

			elif itemname == "Doomblade":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return

			elif itemname == "Deathraze":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return

			elif itemname == "Soulreaper":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return

	# - - - - - Armor - - - - -

			elif itemname == "Leather Armor":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Banded Armor":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Wolf Fur":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Pit Fighter Armor":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Chainmail Armor":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Enchanted Steel Armor":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Barbaric Armor":
				cost = 400		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Branded Metal Armor":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)

			elif itemname == "Iron Armor":
				cost = 700		
				userinfo["gold"] = userinfo["gold"] + cost
				userinfo["inventory"].remove(item)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				list += "{} for {} gold.\n".format(itemname, cost)
				

			elif itemname == "Nightstalker Mantle":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return

			elif itemname == "Bane Of The Goblin Lord":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return
						
			elif itemname == "Hephaestus Armor":
				try:
					em = discord.Embed(description="**Are you sure you want to Sell {}?\nThis is a legendary item!**".format(item["name"]), color=discord.Colour(0xffffff))
					em.set_footer(text="Type yes to sell it to the shopkeeper!")
					await ctx.send(embed=em)
				except:
					pass
				answer = await self.check_answer(ctx, ["yes", "Yes", "y", "Y", "ja", "Ja", "j", "J"])
				if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "Ja" or answer == "ja" or answer == "J" or answer == "j":		
					cost = 1100
					
					userinfo["gold"] = userinfo["gold"] + cost
					userinfo["inventory"].remove(item)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					list += "{} for {} gold.\n".format(itemname, cost)
				else:
					try:
						em = discord.Embed(description="**You declined to sell {}.**".format(itemname), color=discord.Colour(0xffffff))
						await ctx.send(embed=em)
						return
					except:
						return

		em = discord.Embed(description=list, color=discord.Colour(0xffffff))
		await ctx.send(embed=em)

			

			
				
		
		

	@shop.command(name="weapons", pass_context=True)
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def _items_weapons(self, ctx):
		"""Take a look at buyable weapons!"""

		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })


		Class = userinfo["class"]
		if Class == "Mage" or Class == "Elementalist" or Class == "Necromancer" or Class == "Developed Necromancer" or Class == "Adequate Elementalist":
			em = discord.Embed(title="Weapon list for the {} class".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
			em.add_field(name="Calcite Staff <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Staff of Milos <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Tomb of Fire <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Scroll of Blizzards <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Oblivion <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Tomb of Water <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Thunderguard <:Legendary:639425368167809065>", value="Not buyable")
			em.add_field(name="Solarflare <:Legendary:639425368167809065>", value="Not buyable")
			await ctx.send(embed=em)
		elif Class == "Paladin" or Class == "Samurai" or Class == "Knight" or Class == "Master Samurai" or Class == "Grand Paladin":
			em = discord.Embed(title="Weapon list for the {} class".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
			em.add_field(name="Sclerite Sword <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Iron Greatsword <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Iron Mace <:Rare:573784880815538186>", value="2,000 gold")
			em.add_field(name="Mithril Sword <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Spiked Mace <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Excalibur <:Legendary:639425368167809065>", value="Not buyable")
			em.add_field(name="Twilight <:Legendary:639425368167809065>", value="Not buyable")
			await ctx.send(embed=em)
		elif Class == "Thief" or Class == "Mesmer" or Class == "Rogue" or Class == "High Rogue" or Class == "Adept Mesmer":
			em = discord.Embed(title="Weapon list for the {} class".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
			em.add_field(name="Abaddon Dagger <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Rusted Short Sword <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Concealed Blade <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Iron Claws <:Rare:573784880815538186>", value="2,000 gold")
			em.add_field(name="Curved Dagger <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Deathraze <:Legendary:639425368167809065>", value="Not buyable")
			em.add_field(name="Doomblade <:Legendary:639425368167809065>", value="Not buyable")
			em.add_field(name="Soulreaper <:Legendary:639425368167809065>", value="Not buyable")
			await ctx.send(embed=em)
		elif Class == "Archer" or Class == "Ranger" or Class == "Assassin" or Class == "Night Assassin" or Class == "Skilled Ranger":
			em = discord.Embed(title="Weapon list for the {} class".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
			em.add_field(name="Glyphic Bow <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Obsidian Longbow <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Rusted Crossbow <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Makeshift Short Bow <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Verdant Bow <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Reinforced Crossbow <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Etched Long Bow <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Hawkeye <:Legendary:639425368167809065>", value="Not buyable")
			em.add_field(name="Devil's Kiss <:Legendary:639425368167809065>", value="Not buyable")
			await ctx.send(embed=em)
		else:
			em = discord.Embed(description="Sorry, your class is not supported!", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)

	@shop.command(name="armor", pass_context=True)
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def _items_armor(self, ctx):

		"""Take a look at buyable armor"""
		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

		Class = userinfo["class"]

		if Class == "Mesmer" or Class == "Assassin" or Class == "Thief" or Class == "Archer" or Class == "Gladiator" or Class == "Mage" or Class == "Necromancer" or Class == "Rogue"or  Class == "Paladin" or Class == "Knight" or Class == "Elementalist" or Class == "Ranger" or Class == "Night Assassin" or Class == "Skilled Ranger" or Class == "High Rogue" or Class == "Adept Mesmer" or Class == "Master Samurai" or Class == "Grand Paladin" or Class == "Developed Necromancer" or Class == "Adequate Elementalist":
			em = discord.Embed(title="Armor list for the {} class ".format(Class), description="Common:<:Common:573784881012932618> Rare:<:Rare:573784880815538186> Legendary:<:Legendary:639425368167809065> Mythical:<:Mythical:573784881386225694>", color=discord.Colour(0xffffff))
			em.add_field(name="Leather Armor <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Banded Armor <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Barbaric Armor <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Chainmail Armor <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Pit Fighter Armor <:Common:573784881012932618>", value="2,000 gold")
			em.add_field(name="Wolf Fur <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Enchanted Steel Armor <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Branded Metal Armor <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Iron Armor <:Rare:573784880815538186>", value="7,000 gold")
			em.add_field(name="Bane Of The Goblin Lord <:Legendary:639425368167809065>", value="Not buyable")
			em.add_field(name="Nightstalker Mantle <:Legendary:639425368167809065>", value="Not buyable")
			em.add_field(name="Hephaestus Armor <:Legendary:639425368167809065>", value="Not buyable")
			await ctx.send(embed=em)
		else:
			em = discord.Embed(description="Sorry, your class is not supported!", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)

def setup(bot):
	n = shop(bot)
	bot.add_cog(n)