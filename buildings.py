import discord
import random
import time
import datetime
from discord.ext import commands
import asyncio
from random import choice as randchoice
from discord import Permissions
from utils.checks import staff, developer, owner
# from cogs.economy import NoAccount
from utils.db import db
from utils.dataIO import fileIO

class building(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.group(name="build", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _build(self, ctx):
		author = ctx.message.author
		authorinfo = db.users.find_one({ "_id": author.id })
	

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


	@_build.group(name="camp", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _camp(self, ctx):
		"""Required to build crafting stations"""
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to build a camp!")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if userinfo["camp"] == "True":
			em = discord.Embed(title="Already built!", description="You already have a camp built!", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		try:
			cost = 10000
			wood = 150
			stone = 100
			metal = 50

			em = discord.Embed(title="Want to build a camp?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n\n Type yes to build!".format(cost, wood, stone, metal), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

			answer1 = await self.check_answer(ctx, ["yes", "y", "Yes", "Y", "ja", "Ja", "j", "J"])

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your camp!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your camp!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your camp!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your camp!**".format(neededmetal))
					return

				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				userinfo["camp"] = "True"

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Camp build!", description="You have succesfully built your camp!\nstart building craft stations!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
		except:
			return


	@_build.group(name="sawmill", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _sawmill(self, ctx):
		"""Needed to make planks!"""
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to build a camp!")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if userinfo["camp"] == "False":
			em = discord.Embed(title="No camp!", description="Build a camp first with {}build camp".format(ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if userinfo["sawmill"] == "True":
			em = discord.Embed(title="Already built!", description="You already have a sawmill built!", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)

		try:
			cost = 10000
			wood = 250
			stone = 150
			metal = 100

			em = discord.Embed(title="Want to build a sawmill?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n\n Type yes to build!".format(cost, wood, stone, metal), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

			answer1 = await self.check_answer(ctx, ["yes", "y", "Yes", "Y", "ja", "Ja", "j", "J"])

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your sawmill!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your sawmill!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your sawmill!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your sawmill!**".format(neededmetal))
					return

				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				userinfo["sawmill"] = "True"

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="sawmill build!", description="You have succesfully built your sawmill!\nstart making planks out of wood!\ntype {}saw <amount>\n3 wood = 2 planks!".format(ctx.prefix), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
		except:
			return

		
	@_build.group(name="masonry", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _masonry(self, ctx):
		"""Needed to make bricks!"""
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to build a camp!")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		
		if userinfo["camp"] == "False":
			em = discord.Embed(title="No camp!", description="Build a camp first with {}build camp".format(ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if userinfo["masonry"] == "True":
			em = discord.Embed(title="Already built!", description="You already have a masonry build!", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return
		try:
			cost = 10000
			wood = 150
			stone = 250
			metal = 100
			planks = 50

			em = discord.Embed(title="Want to build a masonry?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n\n Type yes to build!".format(cost, wood, stone, metal, planks), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

			answer1 = await self.check_answer(ctx, ["yes", "y", "Yes", "Y", "ja", "Ja", "j", "J"])

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your masonry!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your masonry!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your masonry!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your masonry!**".format(neededmetal))
					return

				if not int(userinfo["planks"]) >= int(planks):
					neededmetal = int(planks) - int(userinfo["planks"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your masonry!**".format(neededmetal))
					return

				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				userinfo["planks"] = userinfo["planks"] - planks
				userinfo["masonry"] = "True"

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="masonry build!", description="You have succesfully built your masonry!\nstart making bricks out of stone!\ntype {}mason <amount>\n5 stone = 4 bricks!".format(ctx.prefix), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
		except:
			return

		
	@_build.group(name="smeltery", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _smeltery(self, ctx):
		"""Needed to make iron plates!"""
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to build a camp!")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if userinfo["camp"] == "False":
			em = discord.Embed(title="No camp!", description="Build a camp first with {}build camp".format(ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if userinfo["smeltery"] == "True":
			em = discord.Embed(title="Already built!", description="You already have a smeltery build!", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return
		try:
			cost = 10000
			wood = 150
			stone = 100
			metal = 150
			planks = 75
			bricks = 100

			em = discord.Embed(title="Want to build a smeltery?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n\n Type yes to build!".format(cost, wood, stone, metal, planks, bricks), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

			answer1 = await self.check_answer(ctx, ["yes", "y", "Yes", "Y", "ja", "Ja", "j", "J"])

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your smeltery!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your smeltery!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your smeltery!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your smeltery!**".format(neededmetal))
					return

				if not int(userinfo["planks"]) >= int(planks):
					neededmetal = int(planks) - int(userinfo["planks"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your smeltery!**".format(neededmetal))
					return

				if not int(userinfo["bricks"]) >= int(bricks):
					neededmetal = int(bricks) - int(userinfo["bricks"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your smeltery!**".format(neededmetal))
					return

				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				userinfo["planks"] = userinfo["planks"] - planks
				userinfo["bricks"] = userinfo["bricks"] - bricks
				userinfo["smeltery"] = "True"

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="smeltery build!", description="You have succesfully built your smeltery!\nstart making iron plates out of metal!\ntype {}smelt <amount>\n5 metal = 4 iron plates!".format(ctx.prefix), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
		except:
			return

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def camp(self, ctx):
		
	
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has checked their camp")

		userinfo = db.users.find_one({ "_id": user.id })

		if userinfo["camp"] == "False":
			em = discord.Embed(title="No camp!", description="Build a camp first with {}build camp".format(ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if userinfo["camp"] == "True":
			em = discord.Embed(color=discord.Colour(0xffffff))
			em.set_author(name="{}'s TEST Camp".format(userinfo["name"]), icon_url=user.avatar_url)
			em.set_image(url="https://cdn.discordapp.com/attachments/780992951694131251/781240037634474065/CampbyMaxie.png")
			em.set_footer(text="No work stations yet!")
			await ctx.send(embed=em)

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
	n = building(bot)
	bot.add_cog(n)