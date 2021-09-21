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
from cogs.levelup import _level_up_check_user
from cogs.quests import _quest_check

class traps(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.group(name="traps", aliases=["trap"], pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _traps(self, ctx):
		"""Traps stuff"""
		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
			
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


	@_traps.group(name="build", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _build(self, ctx):
		"""Build a trap!"""
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to build a trap!")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		cost = 0
		wood = 0
		stone = 0
		metal = 0
		planks = 0
		bricks = 0
		iron_plates = 0
		title = ""
		list = ""
		build_description = ""

		if userinfo["trap"] == 0:
			userinfo["trap1"] = 10
			cost = 1000
			wood = 50
			stone = 25
			metal = 5
			
			title = "Do you want to built your first trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n\n Type yes to built!".format(cost, wood, stone, metal)
			build_description += "You have succesfully build your first trap!\n"
			
		if userinfo["trap"] == 1:	
			userinfo["trap2"] = 10
			cost = 1250
			wood = 75
			stone = 50
			metal = 10
			planks = 5
			
			title = "Do you want to built your second trap?"
			description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks)
			build_description += "You have succesfully build your second trap!\n"

		if userinfo["trap"] == 2:
			userinfo["trap3"] = 10
			cost = 1500
			wood = 100
			stone = 75
			metal = 25
			planks = 10
			bricks = 5

			title = "Do you want to built your 3rd trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks)
			build_description += "You have succesfully build your 3rd trap!\n"
		
		if userinfo["trap"] == 3:
			userinfo["trap4"] = 10
			cost = 1750
			wood = 125
			stone = 100
			metal = 75
			planks = 25
			bricks = 10
			iron_plates = 5

			title = "Do you want to built your 4th trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates)
			build_description += "You have succesfully build your 4th trap!\n"

		if userinfo["trap"] == 4:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 100:
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\n Reach level 100+ to make 5 traps\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			userinfo["trap5"] = 10
			cost = 2000	
			wood = 150
			stone = 125
			metal = 100
			planks = 50
			bricks = 25
			iron_plates = 10

			title = "Do you want to built your 5th trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates)
			build_description += "You have succesfully build your 5th trap!\n"

		if userinfo["trap"] == 5:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 200:
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\n Reach level 200+ to make 7 traps\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			userinfo["trap6"] = 10
			cost = 2250	
			wood = 150
			stone = 125
			metal = 100
			planks = 60
			bricks = 40
			iron_plates = 20

			title = "Do you want to built your 7th trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates)
			build_description += "You have succesfully build your 7th trap!\n"

		if userinfo["trap"] == 6:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 200:
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\n Reach level 200+ to make 7 traps\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			userinfo["trap7"] = 10
			cost = 2500	
			wood = 175
			stone = 150
			metal = 125
			planks = 80
			bricks = 60
			iron_plates = 40

			title = "Do you want to built your 7th trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates)
			build_description += "You have succesfully build your 7th trap!\n"

		if userinfo["trap"] == 7:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			if userinfo["role"] == "patreon1":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			userinfo["trap8"] = 10
			cost = 2750	
			wood = 200
			stone = 170
			metal = 140
			planks = 100
			bricks = 80
			iron_plates = 60

			title = "Do you want to built your 8th trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates)
			build_description += "You have succesfully build your 8th trap!\n"

		if userinfo["trap"] == 8:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			if userinfo["role"] == "patreon1":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			userinfo["trap9"] = 10
			cost = 3000
			wood = 230
			stone = 200
			metal = 170
			planks = 120
			bricks = 100
			iron_plates = 80

			title = "Do you want to built your 9th trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates)
			build_description += "You have succesfully build your 9th trap!\n"

		if userinfo["trap"] == 9:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			if userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			userinfo["trap10"] = 10
			cost = 3100
			wood = 260
			stone = 230
			metal = 200
			planks = 140
			bricks = 120
			iron_plates = 100

			title = "Do you want to built your 10th trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates)
			build_description += "You have succesfully build your 10th trap!\n"

		if userinfo["trap"] == 10:		
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			if userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			userinfo["trap11"] = 10
			cost = 3200
			wood = 280
			stone = 260
			metal = 230
			planks = 150
			bricks = 130
			iron_plates = 110

			title = "Do you want to built your 11th trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates)
			build_description += "You have succesfully build your 11th trap!\n"

		if userinfo["trap"] == 11:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			if  userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			userinfo["trap12"] = 10
			cost = 3300
			wood = 300
			stone = 290
			metal = 260
			planks = 160
			bricks = 140
			iron_plates = 120

			title = "Do you want to built your 12th trap?" 
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates)
			build_description += "You have succesfully build your 12th trap!\n"

		if userinfo["trap"] == 12:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			if  userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			userinfo["trap13"] = 10
			cost = 3400
			wood = 310
			stone = 300
			metal = 270
			planks = 170
			bricks = 150
			iron_plates = 130

			title = "Do you want to built your last trap?"
			description = "This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates)
			build_description += "You have succesfully build your last trap!\n"

		em = discord.Embed(title=title, description=description, color=discord.Colour(0xffffff))
		await ctx.send(embed=em)

		answer1 = await self.check_answer(ctx, ["yes", "y", "Yes", "Y", "ja", "Ja", "j", "J"])

		if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":
			
			if userinfo["gold"] <= cost:
				neededgold = cost - userinfo["gold"]
				list += "<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold)

			if userinfo["wood"] <= wood:
				neededwood = wood - userinfo["wood"]
				list += "<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood)

			if userinfo["stone"] <= stone:
				neededstone = stone - userinfo["stone"]
				list += "<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone)
				
			if userinfo["metal"] <= metal:
				neededmetal = metal - userinfo["metal"]
				list += "<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal)

			if userinfo["planks"] <= planks:
				neededmetal = planks - userinfo["planks"]
				list += "<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededmetal)

			if userinfo["bricks"] <= bricks:
				neededbricks = bricks - userinfo["bricks"]
				list += "<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks)

			if userinfo["iron_plates"] <= iron_plates:
				neededironplates = iron_plates - int(userinfo["iron_plates"])
				list += "<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates)

			try:	
				if list != "":
					em = discord.Embed(title="Not enough recouces!", description=list, color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
					return
			except Exception as e:
				print(e)

			userinfo["gold"] = userinfo["gold"] - cost
			userinfo["wood"] = userinfo["wood"] - wood
			userinfo["stone"] = userinfo["stone"] - stone
			userinfo["metal"] = userinfo["metal"] - metal
			userinfo["planks"] = userinfo["planks"] - planks
			userinfo["bricks"] = userinfo["bricks"] - bricks
			userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
			userinfo["trap"] += 1
						
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

			build_description += "You can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix)

			try:
				em = discord.Embed(title="Trap build!", description=build_description, color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			except Exception as e:
				print(e)
		

	@_traps.group(name="check", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _check(self, ctx):
		"""Check your traps!"""

		
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
		guild = ctx.guild
		channel = ctx.message.channel
		user = ctx.message.author
		now = datetime.datetime.now()
		current_time = now.strftime("%H:%M:%S")
		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has check their traps")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["trap"] == 0:
			em = discord.Embed(title="No traps!", description="Build your first trap with {}trap build".format(ctx.prefix), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["trap_block"])

		cooldowntime = 3600
		if userinfo["role"] == "patreon3":
			cooldowntime = 2880
		if userinfo["role"] == "patreon4":
			cooldowntime = 1800

		list1 = ""
		footer = ""
		title = ""
		if delta >= cooldowntime and delta > 0:
			
			if userinfo["trap"] >= 1 and userinfo["trap1"] == 0:
				list1 += "Trap 1 is broken!\n"
			if userinfo["trap"] >= 2 and  userinfo["trap2"] == 0:
				list1 += "Trap 2 is broken!\n"
			if userinfo["trap"] >= 3 and  userinfo["trap3"] == 0:
				list1 += "Trap 3 is broken!\n"
			if userinfo["trap"] >= 4 and  userinfo["trap4"] == 0:
				list1 += "Trap 4 is broken!\n"
			if userinfo["trap"] >= 5 and  userinfo["trap5"] == 0:
				list1 += "Trap 5 is broken!\n"
			if userinfo["trap"] >= 6 and  userinfo["trap6"] == 0:
				list1 += "Trap 6 is broken!\n"
			if userinfo["trap"] >= 7 and  userinfo["trap7"] == 0:
				list1 += "Trap 7 is broken!\n"
			if userinfo["trap"] >= 8 and  userinfo["trap8"] == 0:
				list1 += "Trap 8 is broken!\n"
			if userinfo["trap"] >= 9 and  userinfo["trap9"] == 0:
				list1 += "Trap 9 is broken!\n"
			if userinfo["trap"] >= 10 and  userinfo["trap10"] == 0:
				list1 += "Trap 10 is broken!\n"
			if userinfo["trap"] >= 11 and  userinfo["trap11"] == 0:
				list1 += "Trap 11 is broken!\n"
			if userinfo["trap"] >= 12 and  userinfo["trap12"] == 0:
				list1 += "Trap 12 is broken!\n"
			if userinfo["trap"] >= 13 and  userinfo["trap13"] == 0:
				list1 += "Trap 13 is broken!\n"
			if not list1:
				pass
			else:
				title += "{}'s Broken Traps".format(userinfo["name"])
				footer += "Fix your broken trap(s) with {}trap repair".format(ctx.prefix)
			try:
				em = discord.Embed(title=title, description=list1 , color=discord.Colour(0xffffff))
				em.set_footer(text=footer)
				await ctx.send(embed=em)
			except:
				pass
			await asyncio.sleep(1)

			guild = ctx.guild
			guildinfo = db.servers.find_one({ "_id": guild.id })
			effectiveguildbonus = guildinfo["bonus"]


			trap1 = 0	
			trap1difficulty = 0
			trap1enemygold = 0
			trap1xpgain = 0

			trap2 = 0
			trap2difficulty = 0
			trap2enemygold = 0
			trap2xpgain = 0

			trap3 = 0
			trap3difficulty = 0
			trap3enemygold = 0
			trap3xpgain = 0

			trap4 = 0
			trap4difficulty = 0
			trap4enemygold = 0
			trap4xpgain = 0

			trap5 = 0
			trap5difficulty = 0
			trap5enemygold = 0
			trap5xpgain = 0

			trap6 = 0
			trap6difficulty = 0
			trap6enemygold = 0
			trap6xpgain = 0

			trap7 = 0
			trap7difficulty = 0
			trap7enemygold = 0
			trap7xpgain = 0

			trap8 = 0
			trap8difficulty = 0
			trap8enemygold = 0
			trap8xpgain = 0
			trap9 = 0
			trap9difficulty = 0
			trap9enemygold = 0
			trap9xpgain = 0

			trap10 = 0
			trap10difficulty = 0
			trap10enemygold = 0
			trap10xpgain = 0

			trap11 = 0
			trap11difficulty = 0
			trap11enemygold = 0
			trap11xpgain = 0

			trap12 = 0
			trap12difficulty = 0
			trap12enemygold = 0
			trap12xpgain = 0

			trap13 = 0
			trap13difficulty = 0
			trap13enemygold = 0
			trap13xpgain = 0

			debi_list = []
			difficulty = [] 
			diff = []
			debi_gold = []	
			debi_xp = []
			for i in range(userinfo["trap"]):
				chance = random.randint(1, 100)
				if userinfo["location"] == "Golden Temple":
					if chance >= 90:
						debi_list.append("Fire Golem")
						debi_gold.append(random.randint(25, 50) + (effectiveguildbonus))
						debi_xp.append(random.randint(20, 40))
					elif chance <= 90 and chance >= 60:
						debi_list.append("Wyvern")
						debi_gold.append(random.randint(15, 35) + (effectiveguildbonus))
						debi_xp.append(random.randint(10, 30))
					elif chance <= 60 and chance >= 0:
						debi_list.append(randchoice(["Rachi", "Debin", "Oofer"]))
						debi_gold.append(random.randint(10, 30) + (effectiveguildbonus))
						debi_xp.append(random.randint(5, 25))
				
				elif userinfo["location"] == "Saker Keep":
					if chance >= 90:
						debi_list.append("The Corrupted")
						debi_gold.append(random.randint(35, 55) + (effectiveguildbonus))
						debi_xp.append(random.randint(30, 50))
					elif chance <= 90 and chance >= 60:
						debi_list.append("Souleater")
						debi_gold.append(random.randint(25, 45) + (effectiveguildbonus))
						debi_xp.append(random.randint(20, 40))
					elif chance <= 60 and chance >= 0:
						debi_list.append(randchoice(["Draugr", "Stalker"]))
						debi_gold.append(random.randint(20, 40) + (effectiveguildbonus))
						debi_xp.append(random.randint(15, 35))
				
				elif userinfo["location"] == "The Forest":
					if chance >= 90:
						debi_list.append("Phantasm")
						debi_gold.append(random.randint(45, 65) + (effectiveguildbonus))
						debi_xp.append(random.randint(40, 60))
					elif chance <= 90 and chance >= 60:
						debi_list.append("Zombie")
						debi_gold.append(random.randint(35, 55) + (effectiveguildbonus))
						debi_xp.append(random.randint(30, 50))
					elif chance <= 60 and chance >= 0:
						debi_list.append(randchoice(["Wolf", "Goblin"]))
						debi_gold.append(random.randint(30, 50) + (effectiveguildbonus))
						debi_xp.append(random.randint(25, 45))
			
				elif userinfo["location"] == "Ebony Mountains":
					if chance >= 90:
						debi_list.append("The Accursed")
						debi_gold.append(random.randint(55, 75) + (effectiveguildbonus))
						debi_xp.append(random.randint(50, 70))
					elif chance <= 90 and chance >= 60:
						debi_list.append("Ebony Guardian")
						debi_gold.append(random.randint(45, 65) + (effectiveguildbonus))
						debi_xp.append(random.randint(40, 60))
					elif chance <= 60 and chance >= 0:
						debi_list.append(randchoice(["Elder Dragon", "Hades"]))
						debi_gold.append(random.randint(40, 60) + (effectiveguildbonus))
						debi_xp.append(random.randint(35, 55))

				elif userinfo["location"] == "Township of Arkina":
					if chance >= 90:
						debi_list.append("The Nameless King")
						debi_gold.append(random.randint(65, 85) + (effectiveguildbonus))
						debi_xp.append(random.randint(60, 80))
					elif chance <= 90 and chance >= 60:
						debi_list.append("Harpy")
						debi_gold.append(random.randint(55, 75) + (effectiveguildbonus))
						debi_xp.append(random.randint(50, 70))
					elif chance <= 60 and chance >= 0:
						debi_list.append(randchoice(["Ettin", "Dormammu"]))
						debi_gold.append(random.randint(50, 70) + (effectiveguildbonus))
						debi_xp.append(random.randint(45, 65))
					
				elif userinfo["location"] == "Zulanthu":
					if chance >= 90:
						debi_list.append("The Venomous")
						debi_gold.append(random.randint(75, 95) + (effectiveguildbonus))
						debi_xp.append(random.randint(70, 90))
					elif chance <= 90 and chance >= 60:
						debi_list.append("Largos")
						debi_gold.append(random.randint(65, 85) + (effectiveguildbonus))
						debi_xp.append(random.randint(60, 80))
					elif chance <= 60 and chance >= 0:
						debi_list.append(randchoice(["Saurian", "Deathclaw"]))
						debi_gold.append(random.randint(60, 80) + (effectiveguildbonus))
						debi_xp.append(random.randint(55, 75))
					
				elif userinfo["location"] == "Lost City":
					if chance >= 90:
						debi_list.append("Death Knight")
						debi_gold.append(random.randint(85, 105) + (effectiveguildbonus))
						debi_xp.append(random.randint(80, 100))

					elif chance <= 90 and chance >= 60:
						debi_list.append("Giant")
						debi_gold.append(random.randint(75, 95) + (effectiveguildbonus))
						debi_xp.append(random.randint(70, 90))
					elif chance <= 60 and chance >= 0:
						debi_list.append(randchoice(["Skeleton", "Lizardmen"]))
						debi_gold.append(random.randint(70, 90) + (effectiveguildbonus))
						debi_xp.append(random.randint(65, 85))

				elif userinfo["location"] == "Drenheim":
					if chance >= 90:
						debi_list.append("Frost Dragon")
						debi_gold.append(random.randint(95, 115) + (effectiveguildbonus))
						debi_xp.append(random.randint(90, 110))
					elif chance <= 90 and chance >= 60:
						debi_list.append("Frost Orc")
						debi_gold.append(random.randint(85, 105) + (effectiveguildbonus))
						debi_xp.append(random.randint(80, 100))
					elif chance <= 60 and chance >= 0:
						debi_list.append(randchoice(["Ice Wolf", "Frost Goblin"]))
						debi_gold.append(random.randint(80, 100) + (effectiveguildbonus))
						debi_xp.append(random.randint(75, 95))

				Difficulty = random.randint(1, 100)

				userinfo["enemydifficulty"] = "Common"
				if Difficulty >= 99:
					difficulty.append("<:Mythical:573784881386225694> ") 
					diff.append("Mythical")

				elif Difficulty <= 99 and Difficulty >= 90:
					difficulty.append("<:Legendary:639425368167809065> ")
					diff.append("Legendary")

				elif Difficulty <= 90 and Difficulty >= 70:
					difficulty.append("<:Rare:573784880815538186> ")
					diff.append("Rare")

				elif Difficulty <= 70 and Difficulty >= 50:
					difficulty.append("<:Uncommon:641361853817159685> ")
					diff.append("Uncommon")

				elif Difficulty <= 50 and Difficulty >= 0:
					difficulty.append("<:Common:573784881012932618> ")
					diff.append("Common")

				if diff[i] == "Uncommon":									
					debi_gold[i] = (int((debi_gold[i] / 100) * 120))					
					debi_xp[i] = (int((debi_xp[i] / 100) * 120))

				if diff[i] == "Rare":
					debi_gold[i] = (int((debi_gold[i] / 100) * 130))					
					debi_xp[i] = (int((debi_xp[i] / 100) * 130))

				if diff[i] == "Legendary":					
					debi_gold[i] = (int((debi_gold[i] / 100) * 140))					
					debi_xp[i] = (int((debi_xp[i] / 100) * 140))	

				if diff[i] == "Mythical":					
					debi_gold[i] = (int((debi_gold[i] / 100) * 150))					
					debi_xp[i] = (int((debi_xp[i] / 100) * 150))

				print("Trap {} is: {} {} {} {} {}".format(i, debi_list[i], debi_gold[i], debi_xp[i], diff[i], difficulty[i]))

				
			try:
				trap1 = debi_list[0]
				trap1difficulty = difficulty[0]
				trap1enemygold = debi_gold[0]
				trap1xpgain = debi_xp[0]

				trap2 = debi_list[1]
				trap2difficulty = difficulty[1]
				trap2enemygold = debi_gold[1]
				trap2xpgain = debi_xp[1]

				trap3 = debi_list[2]
				trap3difficulty = difficulty[2]
				trap3enemygold = debi_gold[2]
				trap3xpgain = debi_xp[2]

				trap4 = debi_list[3]
				trap4difficulty = difficulty[3]
				trap4enemygold = debi_gold[3]
				trap4xpgain = debi_xp[3]

				trap5 = debi_list[4]
				trap5difficulty = difficulty[4]
				trap5enemygold = debi_gold[4]
				trap5xpgain = debi_xp[4]

				trap6 = debi_list[5]
				trap6difficulty = difficulty[5]
				trap6enemygold = debi_gold[5]
				trap6xpgain = debi_xp[5]

				trap7 = debi_list[6]
				trap7difficulty = difficulty[6]
				trap7enemygold = debi_gold[6]
				trap7xpgain = debi_xp[6]

				trap8 = debi_list[7]
				trap8difficulty = difficulty[7]
				trap8enemygold = debi_gold[7]
				trap8xpgain = debi_xp[7]

				trap9 = debi_list[8]
				trap9difficulty = difficulty[8]
				trap9enemygold = debi_gold[8]
				trap9xpgain = debi_xp[8]

				trap10 = debi_list[9]
				trap10difficulty = difficulty[9]
				trap10enemygold = debi_gold[9]
				trap10xpgain = debi_xp[9]

				trap11 = debi_list[10]
				trap11difficulty = difficulty[10]
				trap11enemygold = debi_gold[10]
				trap11xpgain = debi_xp[10]

				trap12 = debi_list[11]
				trap12difficulty = difficulty[11]
				trap12enemygold = debi_gold[11]
				trap12xpgain = debi_xp[11]

				trap13 = debi_list[12]
				trap13difficulty = difficulty[12]
				trap13enemygold = debi_gold[12]
				trap13xpgain = debi_xp[12]

			except:
				pass

			

			list = ""
			list1 = ""
			list2 = ""
			list3 = ""
			list4 = ""
			list5 = ""

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["trap1"] >= 0 and userinfo["trap"] >= 1:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list += "**Trap 1**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap1difficulty, trap1, int(trap1enemygold), int(trap1xpgain))

				elif chance <= 19 and chance >=6:
					userinfo["trap1"] -= 1

					if userinfo["trap1"] == 0:
						list2 += "**Trap 1**\n Has Broken.\n_ _\n"
						trap1enemygold = 0
						trap1xpgain = 0
						userinfo["trap1"] = 0
					else:
						list1 += "**Trap 1**\n Has failed.\n_ _\n"
						trap1enemygold = 0
						trap1xpgain = 0 

				elif chance <= 5 :
					list2 += "**Trap 1**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					userinfo["trap1"] = 0
					trap1enemygold = 0
					trap1xpgain = 0

					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")

				pass

			if userinfo["trap2"] >= 0 and userinfo["trap"] >= 2:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list += "**Trap 2**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap2difficulty, trap2, int(trap2enemygold), int(trap2xpgain))
				if chance <= 19 and chance >= 6:
					userinfo["trap2"] -= 1
					if userinfo["trap2"] == 0:
						list2 += "**Trap 2**\n Has Broken.\n_ _\n"
						trap2enemygold = 0
						trap2xpgain = 0 
					else:
						list1 += "**Trap 2**\n Has failed.\n_ _\n"
						trap2enemygold = 0
						trap2xpgain = 0 
				if chance <= 5 :
					list2 += "**Trap 2**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					userinfo["trap2"] = 0
					trap2enemygold = 0
					trap2xpgain = 0
				pass
			if userinfo["trap3"] >= 0 and userinfo["trap"] >= 3:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list += "**Trap 3**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap3difficulty, trap3, int(trap3enemygold), int(trap3xpgain))
				if chance <= 19 and chance >= 6:
					userinfo["trap3"] -= 1
					if userinfo["trap3"] == 0:
						list2 += "**Trap 3**\n Has Broken.\n_ _\n"
						trap3enemygold = 0
						trap3xpgain = 0 
					else:
						list1 += "**Trap 3**\n Has failed.\n_ _\n"
						trap3enemygold = 0
						trap3xpgain = 0 
				if chance <= 5 :
					list2 += "**Trap 3**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					userinfo["trap3"] = 0
					trap3enemygold = 0
					trap3xpgain = 0
				pass
			if userinfo["trap4"] >= 0 and userinfo["trap"] >= 4:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list += "**Trap 4**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap4difficulty, trap4, int(trap4enemygold), int(trap4xpgain))
				if chance <= 19 and chance >= 6:
					userinfo["trap4"] -= 1
					if userinfo["trap4"] == 0:
						list2 += "**Trap 4**\n Has Broken.\n_ _\n"
						trap4enemygold = 0
						trap4xpgain = 0 
					else:
						list1 += "**Trap 4**\n Has failed.\n_ _\n"
						trap4enemygold = 0
						trap4xpgain = 0 
				if chance <= 5 :
					list2 += "**Trap 4**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					userinfo["trap4"] = 0
					trap4enemygold = 0
					trap4xpgain = 0
				pass
			if userinfo["trap5"] >= 0 and userinfo["trap"] >= 5:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list += "**Trap 5**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap5difficulty, trap5, int(trap5enemygold), int(trap5xpgain))
				if chance <= 19 and chance >= 6:
					userinfo["trap5"] -= 1
					if userinfo["trap5"] == 0:
						list2 += "**Trap 5 **\n Has Broken.\n_ _\n"
						trap5enemygold = 0
						trap5xpgain = 0 
					else:
						list1 += "**Trap 5**\n Has failed.\n_ _\n"
						trap5enemygold = 0
						trap5xpgain = 0 
				if chance <= 5 :
					list2 += "**Trap 5**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					userinfo["trap5"] == 0
					trap5enemygold = 0
					trap5xpgain = 0
				pass
			if userinfo["trap6"] >= 0 and userinfo["trap"] >= 6:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list += "**Trap 6**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap6difficulty, trap6, int(trap6enemygold), int(trap6xpgain))
				if chance <= 19 and chance >= 6:
					userinfo["trap6"] -= 1
					if userinfo["trap6"] == 0:
						list2 += "**Trap 6**\n Has Broken.\n_ _\n"
						trap6enemygold = 0
						trap6xpgain = 0 
					else:
						list1 += "**Trap 6**\n Has failed.\n_ _\n"
						trap6enemygold = 0
						trap6xpgain = 0 
				if chance <= 5 :
					list2 += "**Trap 6**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					userinfo["trap6"] = 0
					trap6enemygold = 0
					trap6xpgain = 0
				pass
			if userinfo["trap7"] >= 0 and userinfo["trap"] >= 7:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list += "**Trap 7**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap7difficulty, trap7, int(trap7enemygold), int(trap7xpgain))
				if chance <= 19 and chance >= 6:
					userinfo["trap7"] -= 1
					if userinfo["trap7"] == 0:
						list2 += "**Trap 7**\n Has Broken.\n_ _\n"
						trap7enemygold = 0
						trap7xpgain = 0 
					else:
						list1 += "**Trap 7**\n Has failed.\n_ _\n"
						trap7enemygold = 0
						trap7xpgain = 0 
				if chance <= 5 :
					list2 += "**Trap 7**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					userinfo["trap7"] = 0
					trap7enemygold = 0
					trap7xpgain = 0
				pass
			if userinfo["trap8"] >= 0 and userinfo["trap"] >= 8:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list3 += "**Trap 8**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap8difficulty, trap8, int(trap8enemygold), int(trap8xpgain))
				if chance <= 19 and chance >= 6:
					userinfo["trap8"] -= 1
					if userinfo["trap8"] == 0:
						list5 += "**Trap 8**\n Has Broken.\n_ _\n"
						trap8enemygold = 0
						trap8xpgain = 0 
					else:
						list4 += "**Trap 8**\n Has failed.\n_ _\n"
						trap8enemygold = 0
						trap8xpgain = 0 
				if chance <= 5 :
					list5 += "**Trap 8**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					userinfo["trap8"] = 0
					trap8enemygold = 0
					trap8xpgain = 0
				pass
			if userinfo["trap9"] >= 0 and userinfo["trap"] >= 9:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list3 += "**Trap 9**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap9difficulty, trap9, int(trap9enemygold), int(trap9xpgain))
				if chance <= 19 and chance >= 6:
					userinfo["trap9"] -= 1
					if userinfo["trap9"] == 0:
						list5 += "**Trap 9**\n Has Broken.\n_ _\n"
						trap9enemygold = 0
						trap9xpgain = 0 
					else:
						list4 += "**Trap 9**\n Has failed.\n_ _\n"
						trap9enemygold = 0
						trap9xpgain = 0 
				if chance <= 5 :
					list5 += "**Trap 9**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					userinfo["trap9"] = 0
					trap9enemygold = 0
					trap9xpgain = 0
				pass
			if userinfo["trap10"] >= 0 and userinfo["trap"] >= 10:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list3 += "**Trap 10**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap10difficulty, trap10, int(trap10enemygold), int(trap10xpgain))
				if chance <= 19 and chance >= 6:
					userinfo["trap10"] -= 1
					if userinfo["trap10"] == 0:
						list5 += "**Trap 10**\n Has Broken.\n_ _\n"
						trap10enemygold = 0
						trap10xpgain = 0 
					else:
						list4 += "**Trap 10**\n Has failed.\n_ _\n"
						trap10enemygold = 0
						trap10xpgain = 0 
				if chance <= 5 :
					list5 += "**Trap 10**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					userinfo["trap10"] = 0
					trap10enemygold = 0
					trap10xpgain = 0
				pass
			if userinfo["trap11"] >= 0 and userinfo["trap"] >= 11:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list3 += "**Trap 11**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap11difficulty, trap11, int(trap11enemygold), int(trap11xpgain))
				if chance <= 19 and chance >= 6:
					userinfo["trap11"] -= 1
					if userinfo["trap11"] == 0:
						list5 += "**Trap 11**\n Has Broken.\n_ _\n"
						trap11enemygold = 0
						trap11xpgain = 0 
					else:
						list4 += "**Trap 11**\n Has failed.\n_ _\n"
						trap11enemygold = 0
						trap11xpgain = 0 
				if chance <= 5 :
					list5 += "**Trap 11**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					userinfo["trap11"] = 0
					trap11enemygold = 0
					trap11xpgain = 0
				pass
			if userinfo["trap12"] >= 0 and userinfo["trap"] >= 12:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list3 += "**Trap 12**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap12difficulty, trap12, int(trap12enemygold), int(trap12xpgain))
				if chance <= 19 and chance >= 6:	
					userinfo["trap12"] -= 1
					if userinfo["trap12"] == 0:
						list5 += "**Trap 12**\n Has Broken.\n_ _\n"
						trap12enemygold = 0
						trap12xpgain = 0
					else:
						list4 += "**Trap 12**\n Has failed.\n_ _\n"
						trap12enemygold = 0
						trap12xpgain = 0
				if chance <= 5 :
					list5 += "**Trap 12**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <=5:
						await ctx.send("Your trap has been broken by a bear!")
					trap13enemygold = 0
					trap13xpgain = 0
					userinfo["trap12"] = 0
				pass
			if userinfo["trap13"] >= 0 and userinfo["trap"] >= 13:
				chance = random.randint(1, 100)
				if chance >= 20:
					userinfo["TrapKills"] = userinfo["TrapKills"] + 1
					list3 += "**Trap 13**\n{} **{}**\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**\n_ _\n".format(trap13difficulty, trap13, int(trap13enemygold), int(trap13xpgain))
				if chance <= 19 and chance >= 6:					
					userinfo["trap13"] -= 1
					if userinfo["trap13"] == 0:
						list5 += "**Trap 13**\n Has Broken.\n_ _\n"

						trap13enemygold = 0
						trap13xpgain = 0
					else:
						list4 += "**Trap 13**\n Has failed.\n_ _\n"
						trap13enemygold = 0
						trap13xpgain = 0 
				if chance <= 5 :
					list5 += "**Trap 13**\n Has Broken.\n_ _\n"
					chance = random.randint(1, 100)
					if chance <= 5:
						await ctx.send("Your trap has been broken by a bear!")
					trap13enemygold = 0
					trap13xpgain = 0
					userinfo["trap13"] = 0
				pass

			#userinfo["trap_block"] = curr_time
			#db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)


			list += "_ _\n"
			list1 += "_ _\n"
			list2 += "_ _\n"
			list3 += "_ _\n"
			list4 += "_ _\n"
			list5 += "_ _\n"

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		
			em = discord.Embed(color=discord.Colour(0xffffff))
			em.set_author(name="{}'s Traps".format(userinfo["name"]), icon_url=user.avatar_url)
			try:
				em.add_field(name="Successful Traps", value=list)
			except Exception as e: 
				print(e)
				pass
			try:
				em.add_field(name="Failed Traps", value=list1)
			except Exception as e: 
				print(e)
				pass
			try:
				em.add_field(name="Broken Traps", value=list2)
			except Exception as e: 
				print(e)
				pass
			
			try:
				if userinfo["toggle"][0]["traps"] == False:
					await ctx.send(embed=em)
				if userinfo["toggle"][0]["traps"] == True:
					pass
			except:
				await ctx.send(embed=em)
				pass
			

			if not list3 == "_ _\n":
				em2 = discord.Embed(color=discord.Colour(0xffffff))
				em2.set_author(name="{}'s Traps 2nd page".format(userinfo["name"]), icon_url=user.avatar_url)
				try:
					em2.add_field(name="Successful Traps", value=list3)
				except Exception as e: 
					print(e)
					pass
				try:
					em2.add_field(name="Failed Traps", value=list4)
				except Exception as e: 
					print(e)
					pass
				try:
					em2.add_field(name="Broken Traps", value=list5)
				except Exception as e: 
					print(e)
					pass
			
				try:
					if userinfo["toggle"][0]["traps"] == False:
						await ctx.send(embed=em2)
					if userinfo["toggle"][0]["traps"] == True:
						pass
				except:
					await ctx.send(embed=em2)
					pass
			else:
				pass

			totalgold = int(trap1enemygold) + int(trap2enemygold) +  int(trap3enemygold) +  int(trap4enemygold) +  int(trap5enemygold) +  int(trap6enemygold) +  int(trap7enemygold) +  int(trap8enemygold) +  int(trap9enemygold) +  int(trap10enemygold) +  int(trap11enemygold) +  int(trap12enemygold) +  int(trap13enemygold)
			totalexp = int(trap1xpgain) + int(trap2xpgain) +  int(trap3xpgain) +  int(trap4xpgain) +  int(trap5xpgain) +  int(trap6xpgain) +  int(trap7xpgain) +  int(trap8xpgain) +  int(trap9xpgain) +  int(trap10xpgain) +  int(trap11xpgain) +  int(trap12xpgain) +  int(trap13xpgain)

			em = discord.Embed(color=discord.Colour(0xffffff))
			em.set_author(name="{}'s total rewards".format(userinfo["name"]), icon_url=user.avatar_url)
			try:
				em.add_field(name="You have earned!", value="\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**".format(totalgold, totalexp))
			except Exception as e: 
				print(e)
				pass
		
			await ctx.send(embed=em)

			userinfo["gold"] += totalgold
			userinfo["exp"] += totalexp
			userinfo["trap_block"] = curr_time
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

			await _level_up_check_user(self, ctx, user)
			
		else:
			# calulate time left
			seconds = cooldowntime - delta
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			em = discord.Embed(title=":hourglass: You can't check your traps yet!\n", description="" + str(round(m)) + " Minutes and " + str(round(s)) + " seconds", color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				except:
					return

	@_traps.group(name="repair", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _repair(self, ctx):
		"""Repair broken traps!"""

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to repair a trap!")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		user = ctx.author
		userinfo = db.users.find_one({ "_id": user.id })
		amount = 0
		if userinfo["trap"] >= 1 and userinfo["trap1"] <= 0:
			amount += 1
		if userinfo["trap"] >= 2 and  userinfo["trap2"] <= 0:
			amount += 1
		if userinfo["trap"] >= 3 and  userinfo["trap3"] <= 0:
			amount += 1
		if userinfo["trap"] >= 4 and  userinfo["trap4"] <= 0:
			amount += 1
		if userinfo["trap"] >= 5 and  userinfo["trap5"] <= 0:
			amount += 1
		if userinfo["trap"] >= 6 and  userinfo["trap6"] <= 0:
			amount += 1
		if userinfo["trap"] >= 7 and  userinfo["trap7"] <= 0:
			amount += 1
		if userinfo["trap"] >= 8 and  userinfo["trap8"] <= 0:
			amount += 1
		if userinfo["trap"] >= 9 and  userinfo["trap9"] <= 0:
			amount += 1
		if userinfo["trap"] >= 10 and  userinfo["trap10"] <= 0:
			amount += 1
		if userinfo["trap"] >= 11 and  userinfo["trap11"] <= 0:
			amount += 1
		if userinfo["trap"] >= 12 and  userinfo["trap12"] <= 0:
			amount += 1
		if userinfo["trap"] >= 13 and  userinfo["trap13"] <= 0:
			amount += 1

		try:

			if amount == 0:
				em = discord.Embed(title="Want to repair your traps?", description="but you have no broken traps!?", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
					return
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			cost = 100 * amount
			wood = 5 * amount
			stone = 5 * amount
			metal = 2 * amount


			em = discord.Embed(title="Want to repair your traps?", description="You have {} broken traps\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n\n Type yes to build!".format(amount, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to repair your traps!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to repair your traps!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to repair your traps!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to repair your traps!**".format(neededmetal))
					return


				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				if userinfo["trap"] >= 1 and userinfo["trap1"] <= 0:
					userinfo["trap1"] = 10
				if userinfo["trap"] >= 2 and  userinfo["trap2"] <= 0:
					userinfo["trap2"] = 10
				if userinfo["trap"] >= 3 and  userinfo["trap3"] <= 0:
					userinfo["trap3"] = 10
				if userinfo["trap"] >= 4 and  userinfo["trap4"] <= 0:
					userinfo["trap4"] = 10
				if userinfo["trap"] >= 5 and  userinfo["trap5"] <= 0:
					userinfo["trap5"] = 10
				if userinfo["trap"] >= 6 and  userinfo["trap6"] <= 0:
					userinfo["trap6"] = 10
				if userinfo["trap"] >= 7 and  userinfo["trap7"] <= 0:
					userinfo["trap7"] = 10
				if userinfo["trap"] >= 8 and  userinfo["trap8"] <= 0:
					userinfo["trap8"] = 10
				if userinfo["trap"] >= 9 and  userinfo["trap9"] <= 0:
					userinfo["trap9"] = 10
				if userinfo["trap"] >= 10 and  userinfo["trap10"] <= 0:
					userinfo["trap10"] = 10
				if userinfo["trap"] >= 11 and  userinfo["trap11"] <= 0:
					userinfo["trap11"] = 10
				if userinfo["trap"] >= 12 and  userinfo["trap12"] <= 0:
					userinfo["trap12"] = 10
				if userinfo["trap"] >= 13 and  userinfo["trap13"] <= 0:
					userinfo["trap13"] = 10

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Traps repaired!", description="You have succesfully repaired all your traps!".format(ctx.prefix), color=discord.Colour(0xffffff))
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


	
	@_traps.group(name="status", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _status(self, ctx):
		"""check your traps status"""
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has chec trap status!")

		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if userinfo["trap1"] <= 0:
			trap1durability = 0
		else:
			trap1durability = userinfo["trap1"]

		if userinfo["trap2"] <= 0:
			trap2durability = 0
		else:
			trap2durability = userinfo["trap2"]

		if userinfo["trap3"] <= 0:
			trap3durability = 0
		else:
			trap3durability = userinfo["trap3"]

		if userinfo["trap4"] <= 0:
			trap4durability = 0
		else:
			trap4durability = userinfo["trap4"]

		if userinfo["trap5"] <= 0:
			trap5durability = 0
		else:
			trap5durability = userinfo["trap5"]

		if userinfo["trap6"] <= 0:
			trap6durability = 0
		else:
			trap6durability = userinfo["trap6"]

		if userinfo["trap7"] <= 0:
			trap7durability = 0
		else:
			trap7durability = userinfo["trap7"]

		if userinfo["trap8"] <= 0:
			trap8durability = 0
		else:
			trap8durability = userinfo["trap8"]

		if userinfo["trap9"] <= 0:
			trap9durability = 0
		else:
			trap9durability = userinfo["trap9"]

		if userinfo["trap10"] <= 0:
			trap10durability = 0
		else:
			trap10durability = userinfo["trap10"]

		if userinfo["trap11"] <= 0:
			trap11durability = 0
		else:
			trap11durability = userinfo["trap11"]

		if userinfo["trap12"] <= 0:
			trap12durability = 0
		else:
			trap12durability = userinfo["trap12"]

		if userinfo["trap13"] <= 0:
			trap13durability = 0
		else:
			trap13durability = userinfo["trap13"]

		

		em = discord.Embed(color=discord.Colour(0xffffff))
		em.set_author(name="{}'s Traps Durability".format(userinfo["name"]), icon_url=user.avatar_url)
		try:
			if userinfo["trap"] >= 1:
				if userinfo["trap1"] <= 0:
					em.add_field(name="Trap 1", value="**Broken!**")
				else:
					em.add_field(name="Trap 1", value="{} / 10".format(trap1durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 2:
				if userinfo["trap2"] <= 0:
					em.add_field(name="Trap 2",  value="**Broken!**")
				else:
					em.add_field(name="Trap 2", value="{} / 10".format(trap2durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 3:
				if userinfo["trap3"] <= 0:
					em.add_field(name="Trap 3",  value="**Broken!**")
				else:
					em.add_field(name="Trap 3", value="{} / 10".format(trap3durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 4:
				if userinfo["trap4"] <= 0:
					em.add_field(name="Trap 4",  value="**Broken!**")
				else:
					em.add_field(name="Trap 4", value="{} / 10".format(trap4durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 5:
				if userinfo["trap5"] <= 0:
					em.add_field(name="Trap 5",  value="**Broken!**")
				else:
					em.add_field(name="Trap 5", value="{} / 10".format(trap5durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 6:
				if userinfo["trap6"] <= 0:
					em.add_field(name="Trap 6",  value="**Broken!**")
				else:
					em.add_field(name="Trap 6", value="{} / 10".format(trap6durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 7:
				if userinfo["trap7"] <= 0:
					em.add_field(name="Trap 7",  value="**Broken!**")
				else:
					em.add_field(name="Trap 7", value="{} / 10".format(trap7durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 8:
				if userinfo["trap8"] <= 0:
					em.add_field(name="Trap 8",  value="**Broken!**")
				else:
					em.add_field(name="Trap 8", value="{} / 10".format(trap8durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 9:
				if userinfo["trap9"] <= 0:
					em.add_field(name="Trap 9",  value="**Broken!**")
				else:
					em.add_field(name="Trap 9", value="{} / 10".format(trap9durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 10:
				if userinfo["trap10"] <= 0:
					em.add_field(name="Trap 10",  value="**Broken!**")
				else:
					em.add_field(name="Trap 10", value="{} / 10".format(trap10durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 11:
				if userinfo["trap11"] <= 0:
					em.add_field(name="Trap 11",  value="**Broken!**")
				else:
					em.add_field(name="Trap 11", value="{} / 10".format(trap11durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 12:
				if userinfo["trap12"] <= 0:
					em.add_field(name="Trap 12", value="**Broken!**")
				else:
					em.add_field(name="Trap 12", value="{} / 10".format(trap12durability))
		except:
			pass
		try:
			if userinfo["trap"] >= 13:
				if userinfo["trap13"] <= 0:
					em.add_field(name="Trap 13",  value="**Broken!**")
				else:
					em.add_field(name="Trap 13", value="{} / 10".format(trap13durability))
		except:
			pass
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
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
	n = traps(bot)
	bot.add_cog(n)