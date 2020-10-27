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

		swordable = ["Knight", "Paladin", "Samurai"]
		bowable = ["Archer", "Ranger", "Assassin"]
		staffable = ["Mage", "Elementalist", "Necromancer", "Ranger"]
		maceable = ["Paladin", "Rogue", "Samurai"]
		daggerable = ["Thief", "Mesmer", "Rogue"]
		gunable = ["Assassin", "Necromancer", "Mesmer"]
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

		if number not in range(1, 24): # Max
			return await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])


		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No item in this slot...**")
			return

		type = item["type"]

		if type == "armor":
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