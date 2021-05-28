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
from utils.checks import staff, developer, owner
from cogs.quests import _quest_check


class equip(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

# - - - Equip - - - # ARMOR NEED TO BE ADDED

	@commands.group(name="equip", pass_context=True, no_pm=True)
	@commands.cooldown(2, 5, commands.BucketType.user)
	
	async def _equip(self, ctx):
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
	
	@_equip.command(name="neck",aliases=["necklace"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(developer)
	async def _equip_neck(self, ctx, number:int):
		"""Equip something for your neck!"""


		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip armor!")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		if number not in range(1, 26): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No item in this slot...**")
			return

		type = item["type"]


		if type == "neck":
			if userinfo["neck"] == "None":
				userinfo["neck"] = item
				userinfo["inventory"].remove(item)
			else:
				userinfo["inventory"].append(userinfo["neck"])
				userinfo["neck"] = "None"
				userinfo["neck"] = item
				userinfo["inventory"].remove(item)

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Necklace Equipped:", description="{}".format(item["name"]), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantarmorequip"]["translation"], color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

	@_equip.command(name="head", aliases=["helmet"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(developer)
	async def _equip_head(self, ctx, number:int):
		"""Equip something for your head!"""


		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip armor!")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		if number not in range(1, 26): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No item in this slot...**")
			return

		type = item["type"]


		if type == "head":
			if userinfo["head"] == "None":
				userinfo["head"] = item
				userinfo["inventory"].remove(item)
			else:
				userinfo["inventory"].append(userinfo["head"])
				userinfo["head"] = "None"
				userinfo["head"] = item
				userinfo["inventory"].remove(item)

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Helmet Equipped:", description="{}".format(item["name"]), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantarmorequip"]["translation"], color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

	
	@_equip.command(name="body",  aliases=["chest", "chestplate"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(developer)
	async def _equip_body(self, ctx, number:int):
		"""Equip a shirt!"""


		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip armor!")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		if number not in range(1, 26): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No item in this slot...**")
			return

		type = item["type"]


		if type == "body":
			if userinfo["body"] == "None":
				userinfo["body"] = item
				userinfo["inventory"].remove(item)
			else:
				userinfo["inventory"].append(userinfo["body"])
				userinfo["body"] = "None"
				userinfo["body"] = item
				userinfo["inventory"].remove(item)

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Body armor equipped:", description="{}".format(item["name"]), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantarmorequip"]["translation"], color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return
		

	@_equip.command(name="legs", aliases=["leggings", "pants"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(developer)
	async def _equip_legs(self, ctx, number:int):
		"""Equip something on your legs!"""


		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip armor!")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		if number not in range(1, 26): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No item in this slot...**")
			return

		type = item["type"]


		if type == "legs":
			if userinfo["legs"] == "None":
				userinfo["legs"] = item
				userinfo["inventory"].remove(item)
			else:
				userinfo["inventory"].append(userinfo["legs"])
				userinfo["legs"] = "None"
				userinfo["legs"] = item
				userinfo["inventory"].remove(item)

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Legs equipped:", description="{}".format(item["name"]), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantarmorequip"]["translation"], color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		
	@_equip.command(name="feet", aliases=["boots", "shoes"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(developer)
	async def _equip_feet(self, ctx, number:int):
		"""Equip feet!"""


		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip armor!")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		if number not in range(1, 26): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No item in this slot...**")
			return

		type = item["type"]


		if type == "feet":
			if userinfo["feet"] == "None":
				userinfo["feet"] = item
				userinfo["inventory"].remove(item)
			else:
				userinfo["inventory"].append(userinfo["feet"])
				userinfo["feet"] = "None"
				userinfo["feet"] = item
				userinfo["inventory"].remove(item)

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Shoes Equipped:", description="{}".format(item["name"]), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantarmorequip"]["translation"], color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return
	
	@_equip.command(name="finger", aliases=["ring", "hand"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(developer)
	async def _equip_finger(self, ctx, number:int):
		"""Equip a ring on your finger!"""


		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip armor!")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		if number not in range(1, 26): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No item in this slot...**")
			return

		type = item["type"]


		if type == "finger":
			if userinfo["finger"] == "None":
				userinfo["finger"] = item
				userinfo["inventory"].remove(item)
			else:
				userinfo["inventory"].append(userinfo["finger"])
				userinfo["finger"] = "None"
				userinfo["finger"] = item
				userinfo["inventory"].remove(item)

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Ring Equipped:", description="{}".format(item["name"]), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantarmorequip"]["translation"], color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return


	@_equip.command(name="weapon", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _equip_weapon(self, ctx, number:int):
		"""Equip a weapon compatible with your class!"""
		user = ctx.message.author

		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip a weapon!")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if number not in range(1, 26): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["noiteminslot"]["translation"])
			return

		type = item["type"]

		swordable = ["Knight", "Paladin", "Samurai","Master Samurai", "Grand Paladin"]
		bowable = ["Archer", "Ranger", "Assassin", "Night Assassin", "Skilled Ranger"]
		staffable = ["Mage", "Elementalist", "Necromancer", "Ranger", "Developed Necromancer", "Adequate Elementalist","Skilled Ranger"]
		maceable = ["Paladin","Knight", "Rogue", "Samurai", "Master Samurai", "Grand Paladin", "High rogue"]
		daggerable = ["Thief", "Mesmer", "Rogue", "High Rogue", "Adept Mesmer"]
		gunable = ["Assassin", "Necromancer", "Mesmer", "Adept Mesmer"]
		armorable = [""]
		if type == "sword":
			if not userinfo["class"] in swordable:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantsword"]["translation"].format(userinfo["class"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if type == "bow":
			if not userinfo["class"] in bowable:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantbow"]["translation"].format(userinfo["class"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if type == "staff":
			if not userinfo["class"] in staffable:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantstaff"]["translation"].format(userinfo["class"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if type == "mace":
			if not userinfo["class"] in maceable:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantmace"]["translation"].format(userinfo["class"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if type == "dagger":
			if not userinfo["class"] in daggerable:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantdagger"]["translation"].format(userinfo["class"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if type == "gun":
			if not userinfo["class"] in gunable:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantgun"]["translation"].format(userinfo["class"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if type == "armor":
			if not userinfo["class"] in armorable:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantarmor"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

		if userinfo["questname"] == "Equip" :
			userinfo["questprogress"] += 1
			userinfo["questpart"] = userinfo["questpart"] + 1
			message = "\nQuest updated, Now equip armor!"
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			if userinfo["questprogress"] >= 1:
				await _quest_check(self, ctx, user, userinfo)
			pass

		if userinfo["equip"] == "None":
			userinfo["equip"] = item
			userinfo["inventory"].remove(item)
		else:
			userinfo["inventory"].append(userinfo["equip"])
			userinfo["equip"] = "None"
			userinfo["equip"] = item
			userinfo["inventory"].remove(item)
		
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["equipped"]["translation"], description="{}{}".format(item["name"], message), color=discord.Colour(0xffffff))
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

	@_equip.command(name="armor", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _equip_armor(self, ctx, number:int):
		"""Equip any piece of armor!"""


		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip armor!")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		if number not in range(1, 26): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No item in this slot...**")
			return

		type = item["type"]

		
		if userinfo["questname"] == "Equip"and userinfo["questpart"] == 1 :
			userinfo["questprogress"] += 1
			userinfo["questpart"] = userinfo["questpart"] + 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			if userinfo["questprogress"] >= 1:
				await _quest_check(self, ctx, user, userinfo)
			pass

		if type == "armor":
			if userinfo["wearing"] == "None":
				userinfo["wearing"] = item
				userinfo["inventory"].remove(item)
			else:
				userinfo["inventory"].append(userinfo["wearing"])
				userinfo["wearing"] = "None"
				userinfo["wearing"] = item
				userinfo["inventory"].remove(item)

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title="Item Equipped:", description="{}".format(item["name"]), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["cantarmorequip"]["translation"], color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

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

def setup(bot):
	c = equip(bot)
	bot.add_cog(c)