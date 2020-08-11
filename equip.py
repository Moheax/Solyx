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

		user = ctx.message.author

		print(user.name+"#"+user.discriminator,"Has tried to equip something")

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

	@_equip.command(name="weapon", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _equip_weapon(self, ctx, number:int):


		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if number not in range(1, 21): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["noiteminslot"]["translation"])
			return

		type = item["type"]

		swordable = ["Knight", "Paladin", "Samurai"]
		bowable = ["Archer", "Ranger", "Assassin"]
		staffable = ["Mage", "Elementalist", "Necromancer", "Ranger"]
		maceable = ["Paladin", "Rogue", "Samurai"]
		daggerable = ["Thief", "Mesmer", "Rogue"]
		gunable = ["Assassin", "Necromancer", "Mesmer"]

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

		userinfo["inventory"].append(userinfo["equip"])
		userinfo["equip"] = "None"
		userinfo["equip"] = item
		userinfo["inventory"].remove(item)
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["equip"]["equipped"]["translation"], description="{}".format(item["name"]), color=discord.Colour(0xffffff))
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
		"""[Work in progress]"""
		languageinfo = db.guilds.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		try:
			await ctx.send("<:Solyx:560809141766193152> | Armor is currently being worked on. Please try again later.")
			return
		except:
			return
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		if number not in range(1, 21): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No item in this slot...**")
			return

		type = item["type"]

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

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def reforge(self, ctx, number:int):
	

		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		if number not in range(1, 21): # Max
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])
			return
		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["noiteminslot"]["translation"])
			return

		cost = 8000

		em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["refinement"], item["type"], item["stats_min"], item["stats_max"], cost), color=discord.Colour(0xffffff))
		if not item["image"] == "None":
			em.set_thumbnail(url=item["image"])
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

		answer1 = await self.check_answer(ctx, ["yes", "y", "Yes", "Y", "ja", "Ja", "j", "J"])

		if not int(userinfo["gold"]) >= int(cost):
			neededgold = int(cost) - int(userinfo["gold"])
			await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
			return

		if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

			refinementlist = ["Normal", "Fine", "Keen", "Mythic", "Shiny", "Superior", "Vivid", "Deadly", "Heroic", "Ominous", "Strange", "Unreal"]
			refinementlist.remove(item["refinement"])
			newrefinement = randchoice(refinementlist)

			newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": item["stats_min"], "stats_max": item["stats_max"], "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
			userinfo["gold"] = userinfo["gold"] - cost
			userinfo["inventory"].remove(item)
			userinfo["inventory"].append(newitem)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

			em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
			if not item["image"] == "None":
				em.set_thumbnail(url=item["image"])
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send("<:Solyx:560809141766193152> | Item reforged!")
					return
				except:
					return

		else:
			try:
				await ctx.send("<:Solyx:560809141766193152> | Not reforging item.")
			except:
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