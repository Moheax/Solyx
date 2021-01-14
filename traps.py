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

		if userinfo["trap"] == 0:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 1000
					wood = 50
					stone = 25
					metal = 5

					em = discord.Embed(title="Do you want to built your first trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n\n Type yes to built!".format(cost, wood, stone, metal), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["trap"] = 1
						userinfo["trap1"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your first trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return

		
		if userinfo["trap"] == 1:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 1250
					wood = 75
					stone = 50
					metal = 10
					planks = 5

					em = discord.Embed(title="Do you want to built your second trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededmetal = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededmetal))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["trap"] = 2
						userinfo["trap2"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your second trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return

		if userinfo["trap"] == 2:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 1500
					wood = 100
					stone = 75
					metal = 25
					planks = 10
					bricks = 5

					em = discord.Embed(title="Do you want to built your 3rd trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["trap"] = 3
						userinfo["trap3"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your 3rd trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return


		if userinfo["trap"] == 3:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 1750
					wood = 125
					stone = 100
					metal = 75
					planks = 25
					bricks = 10
					iron_plates = 5

					em = discord.Embed(title="Do you want to built your 4th trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							neededironplates = int(briron_platesicks) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
						userinfo["trap"] = 4
						userinfo["trap4"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your 4th trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return


		if userinfo["trap"] == 4:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 100:
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\n Reach level 100+ to make 5 traps\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 100 or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 2000	
					wood = 150
					stone = 125
					metal = 100
					planks = 50
					bricks = 25
					iron_plates = 10

					em = discord.Embed(title="Do you want to built your 5th trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							neededironplates = int(briron_platesicks) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
						userinfo["trap"] = 5
						userinfo["trap5"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your 5th trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return


		if userinfo["trap"] == 5:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 200:
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\n Reach level 200+ to make 7 traps\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 2250	
					wood = 150
					stone = 125
					metal = 100
					planks = 60
					bricks = 40
					iron_plates = 20

					em = discord.Embed(title="Do you want to built your 6th trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							neededironplates = int(briron_platesicks) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
						userinfo["trap"] = 6
						userinfo["trap6"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your 6th trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return


		if userinfo["trap"] == 6:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 200:
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\n Reach level 200+ to make 7 traps\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 2500	
					wood = 175
					stone = 150
					metal = 125
					planks = 80
					bricks = 60
					iron_plates = 40

					em = discord.Embed(title="Do you want to built your 7th trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							neededironplates = int(briron_platesicks) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
						userinfo["trap"] = 7
						userinfo["trap7"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your 7th trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return


				
		if userinfo["trap"] == 7:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if  userinfo["role"] == "patreon1":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 2750	
					wood = 200
					stone = 170
					metal = 140
					planks = 100
					bricks = 80
					iron_plates = 60

					em = discord.Embed(title="Do you want to built your 8th trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							neededironplates = int(briron_platesicks) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
						userinfo["trap"] = 8
						userinfo["trap8"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your 8th trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return

		
		if userinfo["trap"] == 8:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if  userinfo["role"] == "patreon1":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 3000
					wood = 230
					stone = 200
					metal = 170
					planks = 120
					bricks = 100
					iron_plates = 80

					em = discord.Embed(title="Do you want to built your 9th trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							neededironplates = int(briron_platesicks) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
						userinfo["trap"] = 9
						userinfo["trap9"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your 9th trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return


		
		if userinfo["trap"] == 9:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if  userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 3100
					wood = 260
					stone = 230
					metal = 200
					planks = 140
					bricks = 120
					iron_plates = 100

					em = discord.Embed(title="Do you want to built your 10th trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							neededironplates = int(briron_platesicks) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
						userinfo["trap"] = 10
						userinfo["trap10"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your 10th trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return


		
		if userinfo["trap"] == 10:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if  userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 3200
					wood = 280
					stone = 260
					metal = 230
					planks = 150
					bricks = 130
					iron_plates = 110

					em = discord.Embed(title="Do you want to built your 11th trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							neededironplates = int(briron_platesicks) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
						userinfo["trap"] = 11
						userinfo["trap11"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your 11th trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return


		
		if userinfo["trap"] == 11:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if  userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 3300
					wood = 300
					stone = 290
					metal = 260
					planks = 160
					bricks = 140
					iron_plates = 120

					em = discord.Embed(title="Do you want to built your 12th trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							neededironplates = int(briron_platesicks) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
						userinfo["trap"] = 12
						userinfo["trap12"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your 12th trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return

			
		if userinfo["trap"] == 12:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200 :
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if  userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3":
				em = discord.Embed(title="Trap Limit reached!", description="You have reached your maximum amount of traps.\nBecome a higher tier patreon to make more traps!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if userinfo["role"] == "patreon3" or userinfo["role"] == "Developer":
				try:
					cost = 3400
					wood = 310
					stone = 300
					metal = 270
					planks = 170
					bricks = 150
					iron_plates = 130

					em = discord.Embed(title="Do you want to built your last trap?", description="This will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to built!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to build your trap!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to build your trap!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to build your trap!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to build your trap!**".format(neededmetal))
							return

						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more planks to build your trap!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to build your trap!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							neededironplates = int(briron_platesicks) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to build your trap!**".format(neededironplates))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
						userinfo["trap"] = 13
						userinfo["trap13"] = 10

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Trap build!", description="You have succesfully build your last trap!\nYou can check your trap every hour to see if it caught a monster.\ncertain patreon tiers have shorter cooldowns!\ntraps can fail or break you would need to replace them, this will be a lot cheaper than building one. \n{}wiki traps for more info.".format(ctx.prefix), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							return
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return
				except:
					return


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

		chopped = random.randint(1, 5)
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


		if delta >= cooldowntime and delta > 0:
			
			if userinfo["trap"] >= 1 and userinfo["trap1"] == 0:
				em = discord.Embed(title="Trap 1 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 2 and  userinfo["trap2"] == 0:
				em = discord.Embed(title="Trap 2 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 3 and  userinfo["trap3"] == 0:
				em = discord.Embed(title="Trap 3 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 4 and  userinfo["trap4"] == 0:
				em = discord.Embed(title="Trap 4 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 5 and  userinfo["trap5"] == 0:
				em = discord.Embed(title="Trap 5 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 6 and  userinfo["trap6"] == 0:
				em = discord.Embed(title="Trap 6 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 7 and  userinfo["trap7"] == 0:
				em = discord.Embed(title="Trap 7 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 8 and  userinfo["trap8"] == 0:
				em = discord.Embed(title="Trap 8 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 9 and  userinfo["trap9"] == 0:
				em = discord.Embed(title="Trap 9 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 10 and  userinfo["trap10"] == 0:
				em = discord.Embed(title="Trap 10 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 11 and  userinfo["trap11"] == 0:
				em = discord.Embed(title="Trap 11 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 12 and  userinfo["trap12"] == 0:
				em = discord.Embed(title="Trap 12 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			if userinfo["trap"] >= 13 and  userinfo["trap13"] == 0:
				em = discord.Embed(title="Trap 13 is broken!", description="Fix your broken trap with {}trap repair".format(ctx.prefix), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)

			await asyncio.sleep(1)
			try:
				if userinfo["trap"] >= 1:	
					if userinfo["location"] == "Golden Temple":
						chance = random.randint(1, 100)

						if chance >= 90:
							debi = randchoice(["Fire Golem"])
						elif chance <= 90 and chance >= 60:
							debi = randchoice(["Wyvern"])
						elif chance <= 60 and chance >= 0:
							debi = randchoice(["Rachi", "Debin", "Oofer"])

						Difficulty = random.randint(1, 100)

						userinfo["enemydifficulty"] = "Common"
						if Difficulty >= 99:
							difficulty = "<:Mythical:573784881386225694> " 
							diff ="Mythical"

						elif Difficulty <= 99 and Difficulty >= 90:
							difficulty = "<:Legendary:639425368167809065> " 
							diff = "Legendary"

						elif Difficulty <= 90 and Difficulty >= 70:
							difficulty = "<:Rare:573784880815538186>" 
							diff = "Rare"

						elif Difficulty <= 70 and Difficulty >= 50:
							difficulty = "<:Uncommon:641361853817159685>"
							diff = "Uncommon"

						elif Difficulty <= 50 and Difficulty >= 0:
							difficulty = "<:Common:573784881012932618> " 
							diff = "Common"

					elif userinfo["location"] == "Saker Keep":
						chance = random.randint(1, 100)

						if chance >= 90:
							debi = randchoice(["The Corrupted"])
						elif chance <= 90 and chance >= 60:
							debi = randchoice(["Souleater"])
						elif chance <= 60 and chance >= 0:
							debi = randchoice(["Draugr", "Stalker"])

						Difficulty = random.randint(1, 100)

						userinfo["enemydifficulty"] = "Common"
						if Difficulty >= 99:
							difficulty = "<:Mythical:573784881386225694> " 
							diff ="Mythical"

						elif Difficulty <= 99 and Difficulty >= 90:
							difficulty = "<:Legendary:639425368167809065> " 
							diff = "Legendary"

						elif Difficulty <= 90 and Difficulty >= 70:
							difficulty = "<:Rare:573784880815538186>" 
							diff = "Rare"

						elif Difficulty <= 70 and Difficulty >= 50:
							difficulty = "<:Uncommon:641361853817159685>"
							diff = "Uncommon"

						elif Difficulty <= 50 and Difficulty >= 0:
							difficulty = "<:Common:573784881012932618> " 
							diff = "Common"
		
					elif userinfo["location"] == "The Forest":
						chance = random.randint(1, 100)

						if chance >= 90:
							debi = randchoice(["Phantasm"])
						elif chance <= 90 and chance >= 60:
							debi = randchoice(["Zombie"])
						elif chance <= 60 and chance >= 0:
							debi = randchoice(["Wolf", "Goblin"])
						
						Difficulty = random.randint(1, 100)

						userinfo["enemydifficulty"] = "Common"
						if Difficulty >= 99:
							difficulty = "<:Mythical:573784881386225694> " 
							diff ="Mythical"

						elif Difficulty <= 99 and Difficulty >= 90:
							difficulty = "<:Legendary:639425368167809065> " 
							diff = "Legendary"

						elif Difficulty <= 90 and Difficulty >= 70:
							difficulty = "<:Rare:573784880815538186>" 
							diff = "Rare"

						elif Difficulty <= 70 and Difficulty >= 50:
							difficulty = "<:Uncommon:641361853817159685>"
							diff = "Uncommon"

						elif Difficulty <= 50 and Difficulty >= 0:
							difficulty = "<:Common:573784881012932618> " 
							diff = "Common"
				
					elif userinfo["location"] == "Ebony Mountains":
						chance = random.randint(1, 100)

						if chance >= 90:
							debi = randchoice(["The Accursed"])
						elif chance <= 90 and chance >= 60:
							debi = randchoice(["Ebony Guardian"])
						elif chance <= 60 and chance >= 0:
							debi = randchoice(["Elder Dragon", "Hades"])
						
						Difficulty = random.randint(1, 100)

						userinfo["enemydifficulty"] = "Common"
						if Difficulty >= 99:
							difficulty = "<:Mythical:573784881386225694> " 
							diff ="Mythical"

						elif Difficulty <= 99 and Difficulty >= 90:
							difficulty = "<:Legendary:639425368167809065> " 
							diff = "Legendary"

						elif Difficulty <= 90 and Difficulty >= 70:
							difficulty = "<:Rare:573784880815538186>" 
							diff = "Rare"

						elif Difficulty <= 70 and Difficulty >= 50:
							difficulty = "<:Uncommon:641361853817159685>"
							diff = "Uncommon"

						elif Difficulty <= 50 and Difficulty >= 0:
							difficulty = "<:Common:573784881012932618> " 
							diff = "Common"

					elif userinfo["location"] == "Township of Arkina":
						chance = random.randint(1, 100)

						if chance >= 90:
							debi = randchoice(["The Nameless King"])
						elif chance <= 90 and chance >= 60:
							debi = randchoice(["Harpy"])
						elif chance <= 60 and chance >= 0:
							debi = randchoice(["Ettin", "Dormammu"])
						
						Difficulty = random.randint(1, 100)

						userinfo["enemydifficulty"] = "Common"
						if Difficulty >= 99:
							difficulty = "<:Mythical:573784881386225694> " 
							diff ="Mythical"

						elif Difficulty <= 99 and Difficulty >= 90:
							difficulty = "<:Legendary:639425368167809065> " 
							diff = "Legendary"

						elif Difficulty <= 90 and Difficulty >= 70:
							difficulty = "<:Rare:573784880815538186>" 
							diff = "Rare"

						elif Difficulty <= 70 and Difficulty >= 50:
							difficulty = "<:Uncommon:641361853817159685>"
							diff = "Uncommon"

						elif Difficulty <= 50 and Difficulty >= 0:
							difficulty = "<:Common:573784881012932618> " 
							diff = "Common"

					elif userinfo["location"] == "Zulanthu":
						chance = random.randint(1, 100)

						if chance >= 90:
							debi = randchoice(["The Venomous"])
						elif chance <= 90 and chance >= 60:
							debi = randchoice(["Largos"])
						elif chance <= 60 and chance >= 0:
							debi = randchoice(["Saurian", "Deathclaw"])
						
						Difficulty = random.randint(1, 100)

						userinfo["enemydifficulty"] = "Common"
						if Difficulty >= 99:
							difficulty = "<:Mythical:573784881386225694> " 
							diff ="Mythical"

						elif Difficulty <= 99 and Difficulty >= 90:
							difficulty = "<:Legendary:639425368167809065> " 
							diff = "Legendary"

						elif Difficulty <= 90 and Difficulty >= 70:
							difficulty = "<:Rare:573784880815538186>" 
							diff = "Rare"

						elif Difficulty <= 70 and Difficulty >= 50:
							difficulty = "<:Uncommon:641361853817159685>"
							diff = "Uncommon"

						elif Difficulty <= 50 and Difficulty >= 0:
							difficulty = "<:Common:573784881012932618> " 
							diff = "Common"

					elif userinfo["location"] == "Lost City":
						chance = random.randint(1, 100)

						if chance >= 90:
							debi = randchoice(["Death Knight"])
						elif chance <= 90 and chance >= 60:
							debi = randchoice(["Giant"])
						elif chance <= 60 and chance >= 0:
							debi = randchoice(["Skeleton", "Lizardmen"])

						Difficulty = random.randint(1, 100)

						userinfo["enemydifficulty"] = "Common"
						if Difficulty >= 99:
							difficulty = "<:Mythical:573784881386225694> " 
							diff ="Mythical"

						elif Difficulty <= 99 and Difficulty >= 90:
							difficulty = "<:Legendary:639425368167809065> " 
							diff = "Legendary"

						elif Difficulty <= 90 and Difficulty >= 70:
							difficulty = "<:Rare:573784880815538186>" 
							diff = "Rare"

						elif Difficulty <= 70 and Difficulty >= 50:
							difficulty = "<:Uncommon:641361853817159685>"
							diff = "Uncommon"

						elif Difficulty <= 50 and Difficulty >= 0:
							difficulty = "<:Common:573784881012932618> " 
							diff = "Common"
				
					elif userinfo["location"] == "Drenheim":
						print("Pong")
						chance = random.randint(1, 100)

						if chance >= 90:
							debi = randchoice(["Frost Dragon"])
						elif chance <= 90 and chance >= 60:
							debi = randchoice(["Frost Orc"])
						elif chance <= 60 and chance >= 0:
							debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
						Difficulty = random.randint(1, 100)

						userinfo["enemydifficulty"] = "Common"
						if Difficulty >= 99:
							difficulty = "<:Mythical:573784881386225694> " 
							diff ="Mythical"

						elif Difficulty <= 99 and Difficulty >= 90:
							difficulty = "<:Legendary:639425368167809065> " 
							diff = "Legendary"

						elif Difficulty <= 90 and Difficulty >= 70:
							difficulty = "<:Rare:573784880815538186>" 
							diff = "Rare"

						elif Difficulty <= 70 and Difficulty >= 50:
							difficulty = "<:Uncommon:641361853817159685>"
							diff = "Uncommon"

						elif Difficulty <= 50 and Difficulty >= 0:
							difficulty = "<:Common:573784881012932618> " 
							diff = "Common"

					trap1 = debi
					trap1diff = diff
					trap1difficulty = difficulty
			
					if userinfo["trap"] >= 2:
						if userinfo["location"] == "Golden Temple":
							chance = random.randint(1, 100)

							if chance >= 90:
								debi = randchoice(["Fire Golem"])
							elif chance <= 90 and chance >= 60:
								debi = randchoice(["Wyvern"])
							elif chance <= 60 and chance >= 0:
								debi = randchoice(["Rachi", "Debin", "Oofer"])

							Difficulty = random.randint(1, 100)

							userinfo["enemydifficulty"] = "Common"
							if Difficulty >= 99:
								difficulty = "<:Mythical:573784881386225694> " 
								diff ="Mythical"

							elif Difficulty <= 99 and Difficulty >= 90:
								difficulty = "<:Legendary:639425368167809065> " 
								diff = "Legendary"

							elif Difficulty <= 90 and Difficulty >= 70:
								difficulty = "<:Rare:573784880815538186>" 
								diff = "Rare"

							elif Difficulty <= 70 and Difficulty >= 50:
								difficulty = "<:Uncommon:641361853817159685>"
								diff = "Uncommon"

							elif Difficulty <= 50 and Difficulty >= 0:
								difficulty = "<:Common:573784881012932618> " 
								diff = "Common"

						elif userinfo["location"] == "Saker Keep":
							chance = random.randint(1, 100)

							if chance >= 90:
								debi = randchoice(["The Corrupted"])
							elif chance <= 90 and chance >= 60:
								debi = randchoice(["Souleater"])
							elif chance <= 60 and chance >= 0:
								debi = randchoice(["Draugr", "Stalker"])

							Difficulty = random.randint(1, 100)

							userinfo["enemydifficulty"] = "Common"
							if Difficulty >= 99:
								difficulty = "<:Mythical:573784881386225694> " 
								diff ="Mythical"

							elif Difficulty <= 99 and Difficulty >= 90:
								difficulty = "<:Legendary:639425368167809065> " 
								diff = "Legendary"

							elif Difficulty <= 90 and Difficulty >= 70:
								difficulty = "<:Rare:573784880815538186>" 
								diff = "Rare"

							elif Difficulty <= 70 and Difficulty >= 50:
								difficulty = "<:Uncommon:641361853817159685>"
								diff = "Uncommon"

							elif Difficulty <= 50 and Difficulty >= 0:
								difficulty = "<:Common:573784881012932618> " 
								diff = "Common"
		
						elif userinfo["location"] == "The Forest":
							chance = random.randint(1, 100)

							if chance >= 90:
								debi = randchoice(["Phantasm"])
							elif chance <= 90 and chance >= 60:
								debi = randchoice(["Zombie"])
							elif chance <= 60 and chance >= 0:
								debi = randchoice(["Wolf", "Goblin"])
					
							Difficulty = random.randint(1, 100)

							userinfo["enemydifficulty"] = "Common"
							if Difficulty >= 99:
								difficulty = "<:Mythical:573784881386225694> " 
								diff ="Mythical"

							elif Difficulty <= 99 and Difficulty >= 90:
								difficulty = "<:Legendary:639425368167809065> " 
								diff = "Legendary"

							elif Difficulty <= 90 and Difficulty >= 70:
								difficulty = "<:Rare:573784880815538186>" 
								diff = "Rare"

							elif Difficulty <= 70 and Difficulty >= 50:
								difficulty = "<:Uncommon:641361853817159685>"
								diff = "Uncommon"

							elif Difficulty <= 50 and Difficulty >= 0:
								difficulty = "<:Common:573784881012932618> " 
								diff = "Common"
				
						elif userinfo["location"] == "Ebony Mountains":
							chance = random.randint(1, 100)

							if chance >= 90:
								debi = randchoice(["The Accursed"])
							elif chance <= 90 and chance >= 60:
								debi = randchoice(["Ebony Guardian"])
							elif chance <= 60 and chance >= 0:
								debi = randchoice(["Elder Dragon", "Hades"])

							Difficulty = random.randint(1, 100)

							userinfo["enemydifficulty"] = "Common"
							if Difficulty >= 99:
								difficulty = "<:Mythical:573784881386225694> " 
								diff ="Mythical"

							elif Difficulty <= 99 and Difficulty >= 90:
								difficulty = "<:Legendary:639425368167809065> " 
								diff = "Legendary"

							elif Difficulty <= 90 and Difficulty >= 70:
								difficulty = "<:Rare:573784880815538186>" 
								diff = "Rare"

							elif Difficulty <= 70 and Difficulty >= 50:
								difficulty = "<:Uncommon:641361853817159685>"
								diff = "Uncommon"

							elif Difficulty <= 50 and Difficulty >= 0:
								difficulty = "<:Common:573784881012932618> " 
								diff = "Common"

						elif userinfo["location"] == "Township of Arkina":
							chance = random.randint(1, 100)

							if chance >= 90:
								debi = randchoice(["The Nameless King"])
							elif chance <= 90 and chance >= 60:
								debi = randchoice(["Harpy"])
							elif chance <= 60 and chance >= 0:
								debi = randchoice(["Ettin", "Dormammu"])

							Difficulty = random.randint(1, 100)

							userinfo["enemydifficulty"] = "Common"
							if Difficulty >= 99:
								difficulty = "<:Mythical:573784881386225694> " 
								diff ="Mythical"

							elif Difficulty <= 99 and Difficulty >= 90:
								difficulty = "<:Legendary:639425368167809065> " 
								diff = "Legendary"

							elif Difficulty <= 90 and Difficulty >= 70:
								difficulty = "<:Rare:573784880815538186>" 
								diff = "Rare"

							elif Difficulty <= 70 and Difficulty >= 50:
								difficulty = "<:Uncommon:641361853817159685>"
								diff = "Uncommon"

							elif Difficulty <= 50 and Difficulty >= 0:
								difficulty = "<:Common:573784881012932618> " 
								diff = "Common"

						elif userinfo["location"] == "Zulanthu":
							chance = random.randint(1, 100)

							if chance >= 90:
								debi = randchoice(["The Venomous"])
							elif chance <= 90 and chance >= 60:
								debi = randchoice(["Largos"])
							elif chance <= 60 and chance >= 0:
								debi = randchoice(["Saurian", "Deathclaw"])
						
							Difficulty = random.randint(1, 100)

							userinfo["enemydifficulty"] = "Common"
							if Difficulty >= 99:
								difficulty = "<:Mythical:573784881386225694> " 
								diff ="Mythical"

							elif Difficulty <= 99 and Difficulty >= 90:
								difficulty = "<:Legendary:639425368167809065> " 
								diff = "Legendary"

							elif Difficulty <= 90 and Difficulty >= 70:
								difficulty = "<:Rare:573784880815538186>" 
								diff = "Rare"

							elif Difficulty <= 70 and Difficulty >= 50:
								difficulty = "<:Uncommon:641361853817159685>"
								diff = "Uncommon"

							elif Difficulty <= 50 and Difficulty >= 0:
								difficulty = "<:Common:573784881012932618> " 
								diff = "Common"

						elif userinfo["location"] == "Lost City":
							chance = random.randint(1, 100)

							if chance >= 90:
								debi = randchoice(["Death Knight"])
							elif chance <= 90 and chance >= 60:
								debi = randchoice(["Giant"])
							elif chance <= 60 and chance >= 0:
								debi = randchoice(["Skeleton", "Lizardmen"])
						
							Difficulty = random.randint(1, 100)

							userinfo["enemydifficulty"] = "Common"
							if Difficulty >= 99:
								difficulty = "<:Mythical:573784881386225694> " 
								diff ="Mythical"

							elif Difficulty <= 99 and Difficulty >= 90:
								difficulty = "<:Legendary:639425368167809065> " 
								diff = "Legendary"

							elif Difficulty <= 90 and Difficulty >= 70:
								difficulty = "<:Rare:573784880815538186>" 
								diff = "Rare"

							elif Difficulty <= 70 and Difficulty >= 50:
								difficulty = "<:Uncommon:641361853817159685>"
								diff = "Uncommon"

							elif Difficulty <= 50 and Difficulty >= 0:
								difficulty = "<:Common:573784881012932618> " 
								diff = "Common"
				
						elif userinfo["location"] == "Drenheim":
					
							chance = random.randint(1, 100)
					
							if chance >= 90:
								debi = randchoice(["Frost Dragon"])
							elif chance <= 90 and chance >= 60:
								debi = randchoice(["Frost Orc"])
							elif chance <= 60 and chance >= 0:
								debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
							Difficulty = random.randint(1, 100)

							userinfo["enemydifficulty"] = "Common"
							if Difficulty >= 99:
								difficulty = "<:Mythical:573784881386225694> " 
								diff ="Mythical"

							elif Difficulty <= 99 and Difficulty >= 90:
								difficulty = "<:Legendary:639425368167809065> " 
								diff = "Legendary"

							elif Difficulty <= 90 and Difficulty >= 70:
								difficulty = "<:Rare:573784880815538186>" 
								diff = "Rare"

							elif Difficulty <= 70 and Difficulty >= 50:
								difficulty = "<:Uncommon:641361853817159685>"
								diff = "Uncommon"

							elif Difficulty <= 50 and Difficulty >= 0:
								difficulty = "<:Common:573784881012932618> " 
								diff = "Common"

						trap2 = debi
						trap2diff = diff
						trap2difficulty = difficulty

						if userinfo["trap"] >= 3:
							if userinfo["location"] == "Golden Temple":
								chance = random.randint(1, 100)

								if chance >= 90:
									debi = randchoice(["Fire Golem"])
								elif chance <= 90 and chance >= 60:
									debi = randchoice(["Wyvern"])
								elif chance <= 60 and chance >= 0:
									debi = randchoice(["Rachi", "Debin", "Oofer"])

								Difficulty = random.randint(1, 100)

								userinfo["enemydifficulty"] = "Common"
								if Difficulty >= 99:
									difficulty = "<:Mythical:573784881386225694> " 
									diff ="Mythical"

								elif Difficulty <= 99 and Difficulty >= 90:
									difficulty = "<:Legendary:639425368167809065> " 
									diff = "Legendary"

								elif Difficulty <= 90 and Difficulty >= 70:
									difficulty = "<:Rare:573784880815538186>" 
									diff = "Rare"

								elif Difficulty <= 70 and Difficulty >= 50:
									difficulty = "<:Uncommon:641361853817159685>"
									diff = "Uncommon"

								elif Difficulty <= 50 and Difficulty >= 0:
									difficulty = "<:Common:573784881012932618> " 
									diff = "Common"

							elif userinfo["location"] == "Saker Keep":
								chance = random.randint(1, 100)

								if chance >= 90:
									debi = randchoice(["The Corrupted"])
								elif chance <= 90 and chance >= 60:
									debi = randchoice(["Souleater"])
								elif chance <= 60 and chance >= 0:
									debi = randchoice(["Draugr", "Stalker"])

								Difficulty = random.randint(1, 100)

								userinfo["enemydifficulty"] = "Common"
								if Difficulty >= 99:
									difficulty = "<:Mythical:573784881386225694> " 
									diff ="Mythical"

								elif Difficulty <= 99 and Difficulty >= 90:
									difficulty = "<:Legendary:639425368167809065> " 
									diff = "Legendary"

								elif Difficulty <= 90 and Difficulty >= 70:
									difficulty = "<:Rare:573784880815538186>" 
									diff = "Rare"

								elif Difficulty <= 70 and Difficulty >= 50:
									difficulty = "<:Uncommon:641361853817159685>"
									diff = "Uncommon"

								elif Difficulty <= 50 and Difficulty >= 0:
									difficulty = "<:Common:573784881012932618> " 
									diff = "Common"
		
							elif userinfo["location"] == "The Forest":
								chance = random.randint(1, 100)

								if chance >= 90:
									debi = randchoice(["Phantasm"])
								elif chance <= 90 and chance >= 60:
									debi = randchoice(["Zombie"])
								elif chance <= 60 and chance >= 0:
									debi = randchoice(["Wolf", "Goblin"])

								Difficulty = random.randint(1, 100)

								userinfo["enemydifficulty"] = "Common"
								if Difficulty >= 99:
									difficulty = "<:Mythical:573784881386225694> " 
									diff ="Mythical"

								elif Difficulty <= 99 and Difficulty >= 90:
									difficulty = "<:Legendary:639425368167809065> " 
									diff = "Legendary"

								elif Difficulty <= 90 and Difficulty >= 70:
									difficulty = "<:Rare:573784880815538186>" 
									diff = "Rare"

								elif Difficulty <= 70 and Difficulty >= 50:
									difficulty = "<:Uncommon:641361853817159685>"
									diff = "Uncommon"

								elif Difficulty <= 50 and Difficulty >= 0:
									difficulty = "<:Common:573784881012932618> " 
									diff = "Common"
				
							elif userinfo["location"] == "Ebony Mountains":
								chance = random.randint(1, 100)

								if chance >= 90:
									debi = randchoice(["The Accursed"])
								elif chance <= 90 and chance >= 60:
									debi = randchoice(["Ebony Guardian"])
								elif chance <= 60 and chance >= 0:
									debi = randchoice(["Elder Dragon", "Hades"])
								
								Difficulty = random.randint(1, 100)

								userinfo["enemydifficulty"] = "Common"
								if Difficulty >= 99:
									difficulty = "<:Mythical:573784881386225694> " 
									diff ="Mythical"

								elif Difficulty <= 99 and Difficulty >= 90:
									difficulty = "<:Legendary:639425368167809065> " 
									diff = "Legendary"

								elif Difficulty <= 90 and Difficulty >= 70:
									difficulty = "<:Rare:573784880815538186>" 
									diff = "Rare"

								elif Difficulty <= 70 and Difficulty >= 50:
									difficulty = "<:Uncommon:641361853817159685>"
									diff = "Uncommon"

								elif Difficulty <= 50 and Difficulty >= 0:
									difficulty = "<:Common:573784881012932618> " 
									diff = "Common"

							elif userinfo["location"] == "Township of Arkina":
								chance = random.randint(1, 100)

								if chance >= 90:
									debi = randchoice(["The Nameless King"])
								elif chance <= 90 and chance >= 60:
									debi = randchoice(["Harpy"])
								elif chance <= 60 and chance >= 0:
									debi = randchoice(["Ettin", "Dormammu"])

								Difficulty = random.randint(1, 100)

								userinfo["enemydifficulty"] = "Common"
								if Difficulty >= 99:
									difficulty = "<:Mythical:573784881386225694> " 
									diff ="Mythical"

								elif Difficulty <= 99 and Difficulty >= 90:
									difficulty = "<:Legendary:639425368167809065> " 
									diff = "Legendary"

								elif Difficulty <= 90 and Difficulty >= 70:
									difficulty = "<:Rare:573784880815538186>" 
									diff = "Rare"

								elif Difficulty <= 70 and Difficulty >= 50:
									difficulty = "<:Uncommon:641361853817159685>"
									diff = "Uncommon"

								elif Difficulty <= 50 and Difficulty >= 0:
									difficulty = "<:Common:573784881012932618> " 
									diff = "Common"

							elif userinfo["location"] == "Zulanthu":
								chance = random.randint(1, 100)

								if chance >= 90:
									debi = randchoice(["The Venomous"])
								elif chance <= 90 and chance >= 60:
									debi = randchoice(["Largos"])
								elif chance <= 60 and chance >= 0:
									debi = randchoice(["Saurian", "Deathclaw"])

								Difficulty = random.randint(1, 100)

								userinfo["enemydifficulty"] = "Common"
								if Difficulty >= 99:
									difficulty = "<:Mythical:573784881386225694> " 
									diff ="Mythical"

								elif Difficulty <= 99 and Difficulty >= 90:
									difficulty = "<:Legendary:639425368167809065> " 
									diff = "Legendary"

								elif Difficulty <= 90 and Difficulty >= 70:
									difficulty = "<:Rare:573784880815538186>" 
									diff = "Rare"

								elif Difficulty <= 70 and Difficulty >= 50:
									difficulty = "<:Uncommon:641361853817159685>"
									diff = "Uncommon"

								elif Difficulty <= 50 and Difficulty >= 0:
									difficulty = "<:Common:573784881012932618> " 
									diff = "Common"

							elif userinfo["location"] == "Lost City":
								chance = random.randint(1, 100)

								if chance >= 90:
									debi = randchoice(["Death Knight"])
								elif chance <= 90 and chance >= 60:
									debi = randchoice(["Giant"])
								elif chance <= 60 and chance >= 0:
									debi = randchoice(["Skeleton", "Lizardmen"])

								Difficulty = random.randint(1, 100)

								userinfo["enemydifficulty"] = "Common"
								if Difficulty >= 99:
									difficulty = "<:Mythical:573784881386225694> " 
									diff ="Mythical"

								elif Difficulty <= 99 and Difficulty >= 90:
									difficulty = "<:Legendary:639425368167809065> " 
									diff = "Legendary"

								elif Difficulty <= 90 and Difficulty >= 70:
									difficulty = "<:Rare:573784880815538186>" 
									diff = "Rare"

								elif Difficulty <= 70 and Difficulty >= 50:
									difficulty = "<:Uncommon:641361853817159685>"
									diff = "Uncommon"

								elif Difficulty <= 50 and Difficulty >= 0:
									difficulty = "<:Common:573784881012932618> " 
									diff = "Common"
				
							elif userinfo["location"] == "Drenheim":
					
								chance = random.randint(1, 100)

								if chance >= 90:
									debi = randchoice(["Frost Dragon"])
								elif chance <= 90 and chance >= 60:
									debi = randchoice(["Frost Orc"])
								elif chance <= 60 and chance >= 0:
									debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
								Difficulty = random.randint(1, 100)

								userinfo["enemydifficulty"] = "Common"
								if Difficulty >= 99:
									difficulty = "<:Mythical:573784881386225694> " 
									diff ="Mythical"

								elif Difficulty <= 99 and Difficulty >= 90:
									difficulty = "<:Legendary:639425368167809065> " 
									diff = "Legendary"

								elif Difficulty <= 90 and Difficulty >= 70:
									difficulty = "<:Rare:573784880815538186>" 
									diff = "Rare"

								elif Difficulty <= 70 and Difficulty >= 50:
									difficulty = "<:Uncommon:641361853817159685>"
									diff = "Uncommon"

								elif Difficulty <= 50 and Difficulty >= 0:
									difficulty = "<:Common:573784881012932618> " 
									diff = "Common"

							trap3 = debi
							trap3diff = diff
							trap3difficulty = difficulty

							if userinfo["trap"] >= 4:
								if userinfo["location"] == "Golden Temple":
									chance = random.randint(1, 100)

									if chance >= 90:
										debi = randchoice(["Fire Golem"])
									elif chance <= 90 and chance >= 60:
										debi = randchoice(["Wyvern"])
									elif chance <= 60 and chance >= 0:
										debi = randchoice(["Rachi", "Debin", "Oofer"])

									Difficulty = random.randint(1, 100)

									userinfo["enemydifficulty"] = "Common"
									if Difficulty >= 99:
										difficulty = "<:Mythical:573784881386225694> " 
										diff ="Mythical"

									elif Difficulty <= 99 and Difficulty >= 90:
										difficulty = "<:Legendary:639425368167809065> " 
										diff = "Legendary"

									elif Difficulty <= 90 and Difficulty >= 70:
										difficulty = "<:Rare:573784880815538186>" 
										diff = "Rare"

									elif Difficulty <= 70 and Difficulty >= 50:
										difficulty = "<:Uncommon:641361853817159685>"
										diff = "Uncommon"

									elif Difficulty <= 50 and Difficulty >= 0:
										difficulty = "<:Common:573784881012932618> " 
										diff = "Common"

								elif userinfo["location"] == "Saker Keep":
									chance = random.randint(1, 100)

									if chance >= 90:
										debi = randchoice(["The Corrupted"])
									elif chance <= 90 and chance >= 60:
										debi = randchoice(["Souleater"])
									elif chance <= 60 and chance >= 0:
										debi = randchoice(["Draugr", "Stalker"])

									Difficulty = random.randint(1, 100)

									userinfo["enemydifficulty"] = "Common"
									if Difficulty >= 99:
										difficulty = "<:Mythical:573784881386225694> " 
										diff ="Mythical"

									elif Difficulty <= 99 and Difficulty >= 90:
										difficulty = "<:Legendary:639425368167809065> " 
										diff = "Legendary"

									elif Difficulty <= 90 and Difficulty >= 70:
										difficulty = "<:Rare:573784880815538186>" 
										diff = "Rare"

									elif Difficulty <= 70 and Difficulty >= 50:
										difficulty = "<:Uncommon:641361853817159685>"
										diff = "Uncommon"

									elif Difficulty <= 50 and Difficulty >= 0:
										difficulty = "<:Common:573784881012932618> " 
										diff = "Common"
		
								elif userinfo["location"] == "The Forest":
									chance = random.randint(1, 100)

									if chance >= 90:
										debi = randchoice(["Phantasm"])
									elif chance <= 90 and chance >= 60:
										debi = randchoice(["Zombie"])
									elif chance <= 60 and chance >= 0:
										debi = randchoice(["Wolf", "Goblin"])

									Difficulty = random.randint(1, 100)

									userinfo["enemydifficulty"] = "Common"
									if Difficulty >= 99:
										difficulty = "<:Mythical:573784881386225694> " 
										diff ="Mythical"

									elif Difficulty <= 99 and Difficulty >= 90:
										difficulty = "<:Legendary:639425368167809065> " 
										diff = "Legendary"

									elif Difficulty <= 90 and Difficulty >= 70:
										difficulty = "<:Rare:573784880815538186>" 
										diff = "Rare"

									elif Difficulty <= 70 and Difficulty >= 50:
										difficulty = "<:Uncommon:641361853817159685>"
										diff = "Uncommon"

									elif Difficulty <= 50 and Difficulty >= 0:
										difficulty = "<:Common:573784881012932618> " 
										diff = "Common"
				
								elif userinfo["location"] == "Ebony Mountains":
									chance = random.randint(1, 100)

									if chance >= 90:
										debi = randchoice(["The Accursed"])
									elif chance <= 90 and chance >= 60:
										debi = randchoice(["Ebony Guardian"])
									elif chance <= 60 and chance >= 0:
										debi = randchoice(["Elder Dragon", "Hades"])

									Difficulty = random.randint(1, 100)

									userinfo["enemydifficulty"] = "Common"
									if Difficulty >= 99:
										difficulty = "<:Mythical:573784881386225694> " 
										diff ="Mythical"

									elif Difficulty <= 99 and Difficulty >= 90:
										difficulty = "<:Legendary:639425368167809065> " 
										diff = "Legendary"

									elif Difficulty <= 90 and Difficulty >= 70:
										difficulty = "<:Rare:573784880815538186>" 
										diff = "Rare"

									elif Difficulty <= 70 and Difficulty >= 50:
										difficulty = "<:Uncommon:641361853817159685>"
										diff = "Uncommon"

									elif Difficulty <= 50 and Difficulty >= 0:
										difficulty = "<:Common:573784881012932618> " 
										diff = "Common"

								elif userinfo["location"] == "Township of Arkina":
									chance = random.randint(1, 100)

									if chance >= 90:
										debi = randchoice(["The Nameless King"])
									elif chance <= 90 and chance >= 60:
										debi = randchoice(["Harpy"])
									elif chance <= 60 and chance >= 0:
										debi = randchoice(["Ettin", "Dormammu"])

									Difficulty = random.randint(1, 100)

									userinfo["enemydifficulty"] = "Common"
									if Difficulty >= 99:
										difficulty = "<:Mythical:573784881386225694> " 
										diff ="Mythical"

									elif Difficulty <= 99 and Difficulty >= 90:
										difficulty = "<:Legendary:639425368167809065> " 
										diff = "Legendary"

									elif Difficulty <= 90 and Difficulty >= 70:
										difficulty = "<:Rare:573784880815538186>" 
										diff = "Rare"

									elif Difficulty <= 70 and Difficulty >= 50:
										difficulty = "<:Uncommon:641361853817159685>"
										diff = "Uncommon"

									elif Difficulty <= 50 and Difficulty >= 0:
										difficulty = "<:Common:573784881012932618> " 
										diff = "Common"

								elif userinfo["location"] == "Zulanthu":
									chance = random.randint(1, 100)

									if chance >= 90:
										debi = randchoice(["The Venomous"])
									elif chance <= 90 and chance >= 60:
										debi = randchoice(["Largos"])
									elif chance <= 60 and chance >= 0:
										debi = randchoice(["Saurian", "Deathclaw"])

									Difficulty = random.randint(1, 100)

									userinfo["enemydifficulty"] = "Common"
									if Difficulty >= 99:
										difficulty = "<:Mythical:573784881386225694> " 
										diff ="Mythical"

									elif Difficulty <= 99 and Difficulty >= 90:
										difficulty = "<:Legendary:639425368167809065> " 
										diff = "Legendary"

									elif Difficulty <= 90 and Difficulty >= 70:
										difficulty = "<:Rare:573784880815538186>" 
										diff = "Rare"

									elif Difficulty <= 70 and Difficulty >= 50:
										difficulty = "<:Uncommon:641361853817159685>"
										diff = "Uncommon"

									elif Difficulty <= 50 and Difficulty >= 0:
										difficulty = "<:Common:573784881012932618> " 
										diff = "Common"

								elif userinfo["location"] == "Lost City":
									chance = random.randint(1, 100)

									if chance >= 90:
										debi = randchoice(["Death Knight"])
									elif chance <= 90 and chance >= 60:
										debi = randchoice(["Giant"])
									elif chance <= 60 and chance >= 0:
										debi = randchoice(["Skeleton", "Lizardmen"])

									Difficulty = random.randint(1, 100)

									userinfo["enemydifficulty"] = "Common"
									if Difficulty >= 99:
										difficulty = "<:Mythical:573784881386225694> " 
										diff ="Mythical"

									elif Difficulty <= 99 and Difficulty >= 90:
										difficulty = "<:Legendary:639425368167809065> " 
										diff = "Legendary"

									elif Difficulty <= 90 and Difficulty >= 70:
										difficulty = "<:Rare:573784880815538186>" 
										diff = "Rare"

									elif Difficulty <= 70 and Difficulty >= 50:
										difficulty = "<:Uncommon:641361853817159685>"
										diff = "Uncommon"

									elif Difficulty <= 50 and Difficulty >= 0:
										difficulty = "<:Common:573784881012932618> " 
										diff = "Common"
				
								elif userinfo["location"] == "Drenheim":
					
									chance = random.randint(1, 100)
					
									if chance >= 90:
										debi = randchoice(["Frost Dragon"])
									elif chance <= 90 and chance >= 60:
										debi = randchoice(["Frost Orc"])
									elif chance <= 60 and chance >= 0:
										debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
									Difficulty = random.randint(1, 100)

									userinfo["enemydifficulty"] = "Common"
									if Difficulty >= 99:
										difficulty = "<:Mythical:573784881386225694> " 
										diff ="Mythical"

									elif Difficulty <= 99 and Difficulty >= 90:
										difficulty = "<:Legendary:639425368167809065> " 
										diff = "Legendary"

									elif Difficulty <= 90 and Difficulty >= 70:
										difficulty = "<:Rare:573784880815538186>" 
										diff = "Rare"

									elif Difficulty <= 70 and Difficulty >= 50:
										difficulty = "<:Uncommon:641361853817159685>"
										diff = "Uncommon"

									elif Difficulty <= 50 and Difficulty >= 0:
										difficulty = "<:Common:573784881012932618> " 
										diff = "Common"

								trap4 = debi
								trap4diff = diff
								trap4difficulty = difficulty

								if userinfo["trap"] >= 5:
									if userinfo["location"] == "Golden Temple":
										chance = random.randint(1, 100)

										if chance >= 90:
											debi = randchoice(["Fire Golem"])
										elif chance <= 90 and chance >= 60:
											debi = randchoice(["Wyvern"])
										elif chance <= 60 and chance >= 0:
											debi = randchoice(["Rachi", "Debin", "Oofer"])

										Difficulty = random.randint(1, 100)

										userinfo["enemydifficulty"] = "Common"
										if Difficulty >= 99:
											difficulty = "<:Mythical:573784881386225694> " 
											diff ="Mythical"

										elif Difficulty <= 99 and Difficulty >= 90:
											difficulty = "<:Legendary:639425368167809065> " 
											diff = "Legendary"

										elif Difficulty <= 90 and Difficulty >= 70:
											difficulty = "<:Rare:573784880815538186>" 
											diff = "Rare"

										elif Difficulty <= 70 and Difficulty >= 50:
											difficulty = "<:Uncommon:641361853817159685>"
											diff = "Uncommon"

										elif Difficulty <= 50 and Difficulty >= 0:
											difficulty = "<:Common:573784881012932618> " 
											diff = "Common"

									elif userinfo["location"] == "Saker Keep":
										chance = random.randint(1, 100)

										if chance >= 90:
											debi = randchoice(["The Corrupted"])
										elif chance <= 90 and chance >= 60:
											debi = randchoice(["Souleater"])
										elif chance <= 60 and chance >= 0:
											debi = randchoice(["Draugr", "Stalker"])

										Difficulty = random.randint(1, 100)

										userinfo["enemydifficulty"] = "Common"
										if Difficulty >= 99:
											difficulty = "<:Mythical:573784881386225694> " 
											diff ="Mythical"

										elif Difficulty <= 99 and Difficulty >= 90:
											difficulty = "<:Legendary:639425368167809065> " 
											diff = "Legendary"

										elif Difficulty <= 90 and Difficulty >= 70:
											difficulty = "<:Rare:573784880815538186>" 
											diff = "Rare"

										elif Difficulty <= 70 and Difficulty >= 50:
											difficulty = "<:Uncommon:641361853817159685>"
											diff = "Uncommon"

										elif Difficulty <= 50 and Difficulty >= 0:
											difficulty = "<:Common:573784881012932618> " 
											diff = "Common"
		
									elif userinfo["location"] == "The Forest":
										chance = random.randint(1, 100)

										if chance >= 90:
											debi = randchoice(["Phantasm"])
										elif chance <= 90 and chance >= 60:
											debi = randchoice(["Zombie"])
										elif chance <= 60 and chance >= 0:
											debi = randchoice(["Wolf", "Goblin"])
										
										Difficulty = random.randint(1, 100)

										userinfo["enemydifficulty"] = "Common"
										if Difficulty >= 99:
											difficulty = "<:Mythical:573784881386225694> " 
											diff ="Mythical"

										elif Difficulty <= 99 and Difficulty >= 90:
											difficulty = "<:Legendary:639425368167809065> " 
											diff = "Legendary"

										elif Difficulty <= 90 and Difficulty >= 70:
											difficulty = "<:Rare:573784880815538186>" 
											diff = "Rare"

										elif Difficulty <= 70 and Difficulty >= 50:
											difficulty = "<:Uncommon:641361853817159685>"
											diff = "Uncommon"

										elif Difficulty <= 50 and Difficulty >= 0:
											difficulty = "<:Common:573784881012932618> " 
											diff = "Common"
				
									elif userinfo["location"] == "Ebony Mountains":
										chance = random.randint(1, 100)

										if chance >= 90:
											debi = randchoice(["The Accursed"])
										elif chance <= 90 and chance >= 60:
											debi = randchoice(["Ebony Guardian"])
										elif chance <= 60 and chance >= 0:
											debi = randchoice(["Elder Dragon", "Hades"])
										
										Difficulty = random.randint(1, 100)

										userinfo["enemydifficulty"] = "Common"
										if Difficulty >= 99:
											difficulty = "<:Mythical:573784881386225694> " 
											diff ="Mythical"

										elif Difficulty <= 99 and Difficulty >= 90:
											difficulty = "<:Legendary:639425368167809065> " 
											diff = "Legendary"

										elif Difficulty <= 90 and Difficulty >= 70:
											difficulty = "<:Rare:573784880815538186>" 
											diff = "Rare"

										elif Difficulty <= 70 and Difficulty >= 50:
											difficulty = "<:Uncommon:641361853817159685>"
											diff = "Uncommon"

										elif Difficulty <= 50 and Difficulty >= 0:
											difficulty = "<:Common:573784881012932618> " 
											diff = "Common"

									elif userinfo["location"] == "Township of Arkina":
										chance = random.randint(1, 100)

										if chance >= 90:
											debi = randchoice(["The Nameless King"])
										elif chance <= 90 and chance >= 60:
											debi = randchoice(["Harpy"])
										elif chance <= 60 and chance >= 0:
											debi = randchoice(["Ettin", "Dormammu"])
										
										Difficulty = random.randint(1, 100)

										userinfo["enemydifficulty"] = "Common"
										if Difficulty >= 99:
											difficulty = "<:Mythical:573784881386225694> " 
											diff ="Mythical"

										elif Difficulty <= 99 and Difficulty >= 90:
											difficulty = "<:Legendary:639425368167809065> " 
											diff = "Legendary"

										elif Difficulty <= 90 and Difficulty >= 70:
											difficulty = "<:Rare:573784880815538186>" 
											diff = "Rare"

										elif Difficulty <= 70 and Difficulty >= 50:
											difficulty = "<:Uncommon:641361853817159685>"
											diff = "Uncommon"

										elif Difficulty <= 50 and Difficulty >= 0:
											difficulty = "<:Common:573784881012932618> " 
											diff = "Common"

									elif userinfo["location"] == "Zulanthu":
										chance = random.randint(1, 100)

										if chance >= 90:
											debi = randchoice(["The Venomous"])
										elif chance <= 90 and chance >= 60:
											debi = randchoice(["Largos"])
										elif chance <= 60 and chance >= 0:
											debi = randchoice(["Saurian", "Deathclaw"])
										
										Difficulty = random.randint(1, 100)

										userinfo["enemydifficulty"] = "Common"
										if Difficulty >= 99:
											difficulty = "<:Mythical:573784881386225694> " 
											diff ="Mythical"

										elif Difficulty <= 99 and Difficulty >= 90:
											difficulty = "<:Legendary:639425368167809065> " 
											diff = "Legendary"

										elif Difficulty <= 90 and Difficulty >= 70:
											difficulty = "<:Rare:573784880815538186>" 
											diff = "Rare"

										elif Difficulty <= 70 and Difficulty >= 50:
											difficulty = "<:Uncommon:641361853817159685>"
											diff = "Uncommon"

										elif Difficulty <= 50 and Difficulty >= 0:
											difficulty = "<:Common:573784881012932618> " 
											diff = "Common"

									elif userinfo["location"] == "Lost City":
										chance = random.randint(1, 100)

										if chance >= 90:
											debi = randchoice(["Death Knight"])
										elif chance <= 90 and chance >= 60:
											debi = randchoice(["Giant"])
										elif chance <= 60 and chance >= 0:
											debi = randchoice(["Skeleton", "Lizardmen"])
										
										Difficulty = random.randint(1, 100)

										userinfo["enemydifficulty"] = "Common"
										if Difficulty >= 99:
											difficulty = "<:Mythical:573784881386225694> " 
											diff ="Mythical"

										elif Difficulty <= 99 and Difficulty >= 90:
											difficulty = "<:Legendary:639425368167809065> " 
											diff = "Legendary"

										elif Difficulty <= 90 and Difficulty >= 70:
											difficulty = "<:Rare:573784880815538186>" 
											diff = "Rare"

										elif Difficulty <= 70 and Difficulty >= 50:
											difficulty = "<:Uncommon:641361853817159685>"
											diff = "Uncommon"

										elif Difficulty <= 50 and Difficulty >= 0:
											difficulty = "<:Common:573784881012932618> " 
											diff = "Common"
				
									elif userinfo["location"] == "Drenheim":
					
										chance = random.randint(1, 100)

										if chance >= 90:
											debi = randchoice(["Frost Dragon"])
										elif chance <= 90 and chance >= 60:
											debi = randchoice(["Frost Orc"])
										elif chance <= 60 and chance >= 0:
											debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
										Difficulty = random.randint(1, 100)

										userinfo["enemydifficulty"] = "Common"
										if Difficulty >= 99:
											difficulty = "<:Mythical:573784881386225694> " 
											diff ="Mythical"

										elif Difficulty <= 99 and Difficulty >= 90:
											difficulty = "<:Legendary:639425368167809065> " 
											diff = "Legendary"

										elif Difficulty <= 90 and Difficulty >= 70:
											difficulty = "<:Rare:573784880815538186>" 
											diff = "Rare"

										elif Difficulty <= 70 and Difficulty >= 50:
											difficulty = "<:Uncommon:641361853817159685>"
											diff = "Uncommon"

										elif Difficulty <= 50 and Difficulty >= 0:
											difficulty = "<:Common:573784881012932618> " 
											diff = "Common"

									trap5 = debi
									trap5diff = diff
									trap5difficulty = difficulty

									if userinfo["trap"] >= 6:
										if userinfo["location"] == "Golden Temple":
											chance = random.randint(1, 100)

											if chance >= 90:
												debi = randchoice(["Fire Golem"])
											elif chance <= 90 and chance >= 60:
												debi = randchoice(["Wyvern"])
											elif chance <= 60 and chance >= 0:
												debi = randchoice(["Rachi", "Debin", "Oofer"])
											
											Difficulty = random.randint(1, 100)

											userinfo["enemydifficulty"] = "Common"
											if Difficulty >= 99:
												difficulty = "<:Mythical:573784881386225694> " 
												diff ="Mythical"

											elif Difficulty <= 99 and Difficulty >= 90:
												difficulty = "<:Legendary:639425368167809065> " 
												diff = "Legendary"

											elif Difficulty <= 90 and Difficulty >= 70:
												difficulty = "<:Rare:573784880815538186>" 
												diff = "Rare"

											elif Difficulty <= 70 and Difficulty >= 50:
												difficulty = "<:Uncommon:641361853817159685>"
												diff = "Uncommon"

											elif Difficulty <= 50 and Difficulty >= 0:
												difficulty = "<:Common:573784881012932618> " 
												diff = "Common"

										elif userinfo["location"] == "Saker Keep":
											chance = random.randint(1, 100)

											if chance >= 90:
												debi = randchoice(["The Corrupted"])
											elif chance <= 90 and chance >= 60:
												debi = randchoice(["Souleater"])
											elif chance <= 60 and chance >= 0:
												debi = randchoice(["Draugr", "Stalker"])
											
											Difficulty = random.randint(1, 100)

											userinfo["enemydifficulty"] = "Common"
											if Difficulty >= 99:
												difficulty = "<:Mythical:573784881386225694> " 
												diff ="Mythical"

											elif Difficulty <= 99 and Difficulty >= 90:
												difficulty = "<:Legendary:639425368167809065> " 
												diff = "Legendary"

											elif Difficulty <= 90 and Difficulty >= 70:
												difficulty = "<:Rare:573784880815538186>" 
												diff = "Rare"

											elif Difficulty <= 70 and Difficulty >= 50:
												difficulty = "<:Uncommon:641361853817159685>"
												diff = "Uncommon"

											elif Difficulty <= 50 and Difficulty >= 0:
												difficulty = "<:Common:573784881012932618> " 
												diff = "Common"
		
										elif userinfo["location"] == "The Forest":
											chance = random.randint(1, 100)

											if chance >= 90:
												debi = randchoice(["Phantasm"])
											elif chance <= 90 and chance >= 60:
												debi = randchoice(["Zombie"])
											elif chance <= 60 and chance >= 0:
												debi = randchoice(["Wolf", "Goblin"])
											
											Difficulty = random.randint(1, 100)

											userinfo["enemydifficulty"] = "Common"
											if Difficulty >= 99:
												difficulty = "<:Mythical:573784881386225694> " 
												diff ="Mythical"

											elif Difficulty <= 99 and Difficulty >= 90:
												difficulty = "<:Legendary:639425368167809065> " 
												diff = "Legendary"

											elif Difficulty <= 90 and Difficulty >= 70:
												difficulty = "<:Rare:573784880815538186>" 
												diff = "Rare"

											elif Difficulty <= 70 and Difficulty >= 50:
												difficulty = "<:Uncommon:641361853817159685>"
												diff = "Uncommon"

											elif Difficulty <= 50 and Difficulty >= 0:
												difficulty = "<:Common:573784881012932618> " 
												diff = "Common"
				
										elif userinfo["location"] == "Ebony Mountains":
											chance = random.randint(1, 100)

											if chance >= 90:
												debi = randchoice(["The Accursed"])
											elif chance <= 90 and chance >= 60:
												debi = randchoice(["Ebony Guardian"])
											elif chance <= 60 and chance >= 0:
												debi = randchoice(["Elder Dragon", "Hades"])
											
											Difficulty = random.randint(1, 100)

											userinfo["enemydifficulty"] = "Common"
											if Difficulty >= 99:
												difficulty = "<:Mythical:573784881386225694> " 
												diff ="Mythical"

											elif Difficulty <= 99 and Difficulty >= 90:
												difficulty = "<:Legendary:639425368167809065> " 
												diff = "Legendary"

											elif Difficulty <= 90 and Difficulty >= 70:
												difficulty = "<:Rare:573784880815538186>" 
												diff = "Rare"

											elif Difficulty <= 70 and Difficulty >= 50:
												difficulty = "<:Uncommon:641361853817159685>"
												diff = "Uncommon"

											elif Difficulty <= 50 and Difficulty >= 0:
												difficulty = "<:Common:573784881012932618> " 
												diff = "Common"

										elif userinfo["location"] == "Township of Arkina":
											chance = random.randint(1, 100)

											if chance >= 90:
												debi = randchoice(["The Nameless King"])
											elif chance <= 90 and chance >= 60:
												debi = randchoice(["Harpy"])
											elif chance <= 60 and chance >= 0:
												debi = randchoice(["Ettin", "Dormammu"])
											
											Difficulty = random.randint(1, 100)

											userinfo["enemydifficulty"] = "Common"
											if Difficulty >= 99:
												difficulty = "<:Mythical:573784881386225694> " 
												diff ="Mythical"

											elif Difficulty <= 99 and Difficulty >= 90:
												difficulty = "<:Legendary:639425368167809065> " 
												diff = "Legendary"

											elif Difficulty <= 90 and Difficulty >= 70:
												difficulty = "<:Rare:573784880815538186>" 
												diff = "Rare"

											elif Difficulty <= 70 and Difficulty >= 50:
												difficulty = "<:Uncommon:641361853817159685>"
												diff = "Uncommon"

											elif Difficulty <= 50 and Difficulty >= 0:
												difficulty = "<:Common:573784881012932618> " 
												diff = "Common"

										elif userinfo["location"] == "Zulanthu":
											chance = random.randint(1, 100)

											if chance >= 90:
												debi = randchoice(["The Venomous"])
											elif chance <= 90 and chance >= 60:
												debi = randchoice(["Largos"])
											elif chance <= 60 and chance >= 0:
												debi = randchoice(["Saurian", "Deathclaw"])
											
											Difficulty = random.randint(1, 100)

											userinfo["enemydifficulty"] = "Common"
											if Difficulty >= 99:
												difficulty = "<:Mythical:573784881386225694> " 
												diff ="Mythical"

											elif Difficulty <= 99 and Difficulty >= 90:
												difficulty = "<:Legendary:639425368167809065> " 
												diff = "Legendary"

											elif Difficulty <= 90 and Difficulty >= 70:
												difficulty = "<:Rare:573784880815538186>" 
												diff = "Rare"

											elif Difficulty <= 70 and Difficulty >= 50:
												difficulty = "<:Uncommon:641361853817159685>"
												diff = "Uncommon"

											elif Difficulty <= 50 and Difficulty >= 0:
												difficulty = "<:Common:573784881012932618> " 
												diff = "Common"

										elif userinfo["location"] == "Lost City":
											chance = random.randint(1, 100)

											if chance >= 90:
												debi = randchoice(["Death Knight"])
											elif chance <= 90 and chance >= 60:
												debi = randchoice(["Giant"])
											elif chance <= 60 and chance >= 0:
												debi = randchoice(["Skeleton", "Lizardmen"])
											
											Difficulty = random.randint(1, 100)

											userinfo["enemydifficulty"] = "Common"
											if Difficulty >= 99:
												difficulty = "<:Mythical:573784881386225694> " 
												diff ="Mythical"

											elif Difficulty <= 99 and Difficulty >= 90:
												difficulty = "<:Legendary:639425368167809065> " 
												diff = "Legendary"

											elif Difficulty <= 90 and Difficulty >= 70:
												difficulty = "<:Rare:573784880815538186>" 
												diff = "Rare"

											elif Difficulty <= 70 and Difficulty >= 50:
												difficulty = "<:Uncommon:641361853817159685>"
												diff = "Uncommon"

											elif Difficulty <= 50 and Difficulty >= 0:
												difficulty = "<:Common:573784881012932618> " 
												diff = "Common"
				
										elif userinfo["location"] == "Drenheim":
					
											chance = random.randint(1, 100)
					
											if chance >= 90:
												debi = randchoice(["Frost Dragon"])
											elif chance <= 90 and chance >= 60:
												debi = randchoice(["Frost Orc"])
											elif chance <= 60 and chance >= 0:
												debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
											Difficulty = random.randint(1, 100)

											userinfo["enemydifficulty"] = "Common"
											if Difficulty >= 99:
												difficulty = "<:Mythical:573784881386225694> " 
												diff ="Mythical"

											elif Difficulty <= 99 and Difficulty >= 90:
												difficulty = "<:Legendary:639425368167809065> " 
												diff = "Legendary"

											elif Difficulty <= 90 and Difficulty >= 70:
												difficulty = "<:Rare:573784880815538186>" 
												diff = "Rare"

											elif Difficulty <= 70 and Difficulty >= 50:
												difficulty = "<:Uncommon:641361853817159685>"
												diff = "Uncommon"

											elif Difficulty <= 50 and Difficulty >= 0:
												difficulty = "<:Common:573784881012932618> " 
												diff = "Common"

										trap6 = debi
										trap6diff = diff
										trap6difficulty = difficulty

										if userinfo["trap"] >= 7:
											if userinfo["location"] == "Golden Temple":
												chance = random.randint(1, 100)

												if chance >= 90:
													debi = randchoice(["Fire Golem"])
												elif chance <= 90 and chance >= 60:
													debi = randchoice(["Wyvern"])
												elif chance <= 60 and chance >= 0:
													debi = randchoice(["Rachi", "Debin", "Oofer"])
												
												Difficulty = random.randint(1, 100)

												userinfo["enemydifficulty"] = "Common"
												if Difficulty >= 99:
													difficulty = "<:Mythical:573784881386225694> " 
													diff ="Mythical"

												elif Difficulty <= 99 and Difficulty >= 90:
													difficulty = "<:Legendary:639425368167809065> " 
													diff = "Legendary"

												elif Difficulty <= 90 and Difficulty >= 70:
													difficulty = "<:Rare:573784880815538186>" 
													diff = "Rare"

												elif Difficulty <= 70 and Difficulty >= 50:
													difficulty = "<:Uncommon:641361853817159685>"
													diff = "Uncommon"

												elif Difficulty <= 50 and Difficulty >= 0:
													difficulty = "<:Common:573784881012932618> " 
													diff = "Common"

											elif userinfo["location"] == "Saker Keep":
												chance = random.randint(1, 100)

												if chance >= 90:
													debi = randchoice(["The Corrupted"])
												elif chance <= 90 and chance >= 60:
													debi = randchoice(["Souleater"])
												elif chance <= 60 and chance >= 0:
													debi = randchoice(["Draugr", "Stalker"])
												
												Difficulty = random.randint(1, 100)

												userinfo["enemydifficulty"] = "Common"
												if Difficulty >= 99:
													difficulty = "<:Mythical:573784881386225694> " 
													diff ="Mythical"

												elif Difficulty <= 99 and Difficulty >= 90:
													difficulty = "<:Legendary:639425368167809065> " 
													diff = "Legendary"

												elif Difficulty <= 90 and Difficulty >= 70:
													difficulty = "<:Rare:573784880815538186>" 
													diff = "Rare"

												elif Difficulty <= 70 and Difficulty >= 50:
													difficulty = "<:Uncommon:641361853817159685>"
													diff = "Uncommon"

												elif Difficulty <= 50 and Difficulty >= 0:
													difficulty = "<:Common:573784881012932618> " 
													diff = "Common"
		
											elif userinfo["location"] == "The Forest":
												chance = random.randint(1, 100)

												if chance >= 90:
													debi = randchoice(["Phantasm"])
												elif chance <= 90 and chance >= 60:
													debi = randchoice(["Zombie"])
												elif chance <= 60 and chance >= 0:
													debi = randchoice(["Wolf", "Goblin"])
												
												Difficulty = random.randint(1, 100)

												userinfo["enemydifficulty"] = "Common"
												if Difficulty >= 99:
													difficulty = "<:Mythical:573784881386225694> " 
													diff ="Mythical"

												elif Difficulty <= 99 and Difficulty >= 90:
													difficulty = "<:Legendary:639425368167809065> " 
													diff = "Legendary"

												elif Difficulty <= 90 and Difficulty >= 70:
													difficulty = "<:Rare:573784880815538186>" 
													diff = "Rare"

												elif Difficulty <= 70 and Difficulty >= 50:
													difficulty = "<:Uncommon:641361853817159685>"
													diff = "Uncommon"

												elif Difficulty <= 50 and Difficulty >= 0:
													difficulty = "<:Common:573784881012932618> " 
													diff = "Common"
				
											elif userinfo["location"] == "Ebony Mountains":
												chance = random.randint(1, 100)

												if chance >= 90:
													debi = randchoice(["The Accursed"])
												elif chance <= 90 and chance >= 60:
													debi = randchoice(["Ebony Guardian"])
												elif chance <= 60 and chance >= 0:
													debi = randchoice(["Elder Dragon", "Hades"])

												Difficulty = random.randint(1, 100)

												userinfo["enemydifficulty"] = "Common"
												if Difficulty >= 99:
													difficulty = "<:Mythical:573784881386225694> " 
													diff ="Mythical"

												elif Difficulty <= 99 and Difficulty >= 90:
													difficulty = "<:Legendary:639425368167809065> " 
													diff = "Legendary"

												elif Difficulty <= 90 and Difficulty >= 70:
													difficulty = "<:Rare:573784880815538186>" 
													diff = "Rare"

												elif Difficulty <= 70 and Difficulty >= 50:
													difficulty = "<:Uncommon:641361853817159685>"
													diff = "Uncommon"

												elif Difficulty <= 50 and Difficulty >= 0:
													difficulty = "<:Common:573784881012932618> " 
													diff = "Common"

											elif userinfo["location"] == "Township of Arkina":
												chance = random.randint(1, 100)

												if chance >= 90:
													debi = randchoice(["The Nameless King"])
												elif chance <= 90 and chance >= 60:
													debi = randchoice(["Harpy"])
												elif chance <= 60 and chance >= 0:
													debi = randchoice(["Ettin", "Dormammu"])
												
												Difficulty = random.randint(1, 100)

												userinfo["enemydifficulty"] = "Common"
												if Difficulty >= 99:
													difficulty = "<:Mythical:573784881386225694> " 
													diff ="Mythical"

												elif Difficulty <= 99 and Difficulty >= 90:
													difficulty = "<:Legendary:639425368167809065> " 
													diff = "Legendary"

												elif Difficulty <= 90 and Difficulty >= 70:
													difficulty = "<:Rare:573784880815538186>" 
													diff = "Rare"

												elif Difficulty <= 70 and Difficulty >= 50:
													difficulty = "<:Uncommon:641361853817159685>"
													diff = "Uncommon"

												elif Difficulty <= 50 and Difficulty >= 0:
													difficulty = "<:Common:573784881012932618> " 
													diff = "Common"

											elif userinfo["location"] == "Zulanthu":
												chance = random.randint(1, 100)

												if chance >= 90:
													debi = randchoice(["The Venomous"])
												elif chance <= 90 and chance >= 60:
													debi = randchoice(["Largos"])
												elif chance <= 60 and chance >= 0:
													debi = randchoice(["Saurian", "Deathclaw"])
												
												Difficulty = random.randint(1, 100)

												userinfo["enemydifficulty"] = "Common"
												if Difficulty >= 99:
													difficulty = "<:Mythical:573784881386225694> " 
													diff ="Mythical"

												elif Difficulty <= 99 and Difficulty >= 90:
													difficulty = "<:Legendary:639425368167809065> " 
													diff = "Legendary"

												elif Difficulty <= 90 and Difficulty >= 70:
													difficulty = "<:Rare:573784880815538186>" 
													diff = "Rare"

												elif Difficulty <= 70 and Difficulty >= 50:
													difficulty = "<:Uncommon:641361853817159685>"
													diff = "Uncommon"

												elif Difficulty <= 50 and Difficulty >= 0:
													difficulty = "<:Common:573784881012932618> " 
													diff = "Common"

											elif userinfo["location"] == "Lost City":
												chance = random.randint(1, 100)

												if chance >= 90:
													debi = randchoice(["Death Knight"])
												elif chance <= 90 and chance >= 60:
													debi = randchoice(["Giant"])
												elif chance <= 60 and chance >= 0:
													debi = randchoice(["Skeleton", "Lizardmen"])
												
												Difficulty = random.randint(1, 100)

												userinfo["enemydifficulty"] = "Common"
												if Difficulty >= 99:
													difficulty = "<:Mythical:573784881386225694> " 
													diff ="Mythical"

												elif Difficulty <= 99 and Difficulty >= 90:
													difficulty = "<:Legendary:639425368167809065> " 
													diff = "Legendary"

												elif Difficulty <= 90 and Difficulty >= 70:
													difficulty = "<:Rare:573784880815538186>" 
													diff = "Rare"

												elif Difficulty <= 70 and Difficulty >= 50:
													difficulty = "<:Uncommon:641361853817159685>"
													diff = "Uncommon"

												elif Difficulty <= 50 and Difficulty >= 0:
													difficulty = "<:Common:573784881012932618> " 
													diff = "Common"
				
											elif userinfo["location"] == "Drenheim":
					
												chance = random.randint(1, 100)
					
												if chance >= 90:
													debi = randchoice(["Frost Dragon"])
												elif chance <= 90 and chance >= 60:
													debi = randchoice(["Frost Orc"])
												elif chance <= 60 and chance >= 0:
													debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
												Difficulty = random.randint(1, 100)

												userinfo["enemydifficulty"] = "Common"
												if Difficulty >= 99:
													difficulty = "<:Mythical:573784881386225694> " 
													diff ="Mythical"

												elif Difficulty <= 99 and Difficulty >= 90:
													difficulty = "<:Legendary:639425368167809065> " 
													diff = "Legendary"

												elif Difficulty <= 90 and Difficulty >= 70:
													difficulty = "<:Rare:573784880815538186>" 
													diff = "Rare"

												elif Difficulty <= 70 and Difficulty >= 50:
													difficulty = "<:Uncommon:641361853817159685>"
													diff = "Uncommon"

												elif Difficulty <= 50 and Difficulty >= 0:
													difficulty = "<:Common:573784881012932618> " 
													diff = "Common"

											trap7 = debi
											trap7diff = diff
											trap7difficulty = difficulty
										
											if userinfo["trap"] >= 8:
												if userinfo["location"] == "Golden Temple":
													chance = random.randint(1, 100)

													if chance >= 90:
														debi = randchoice(["Fire Golem"])
													elif chance <= 90 and chance >= 60:
														debi = randchoice(["Wyvern"])
													elif chance <= 60 and chance >= 0:
														debi = randchoice(["Rachi", "Debin", "Oofer"])

													Difficulty = random.randint(1, 100)

													userinfo["enemydifficulty"] = "Common"
													if Difficulty >= 99:
														difficulty = "<:Mythical:573784881386225694> " 
														diff ="Mythical"

													elif Difficulty <= 99 and Difficulty >= 90:
														difficulty = "<:Legendary:639425368167809065> " 
														diff = "Legendary"

													elif Difficulty <= 90 and Difficulty >= 70:
														difficulty = "<:Rare:573784880815538186>" 
														diff = "Rare"

													elif Difficulty <= 70 and Difficulty >= 50:
														difficulty = "<:Uncommon:641361853817159685>"
														diff = "Uncommon"

													elif Difficulty <= 50 and Difficulty >= 0:
														difficulty = "<:Common:573784881012932618> " 
														diff = "Common"

												elif userinfo["location"] == "Saker Keep":
													chance = random.randint(1, 100)

													if chance >= 90:
														debi = randchoice(["The Corrupted"])
													elif chance <= 90 and chance >= 60:
														debi = randchoice(["Souleater"])
													elif chance <= 60 and chance >= 0:
														debi = randchoice(["Draugr", "Stalker"])

													Difficulty = random.randint(1, 100)

													userinfo["enemydifficulty"] = "Common"
													if Difficulty >= 99:
														difficulty = "<:Mythical:573784881386225694> " 
														diff ="Mythical"

													elif Difficulty <= 99 and Difficulty >= 90:
														difficulty = "<:Legendary:639425368167809065> " 
														diff = "Legendary"

													elif Difficulty <= 90 and Difficulty >= 70:
														difficulty = "<:Rare:573784880815538186>" 
														diff = "Rare"

													elif Difficulty <= 70 and Difficulty >= 50:
														difficulty = "<:Uncommon:641361853817159685>"
														diff = "Uncommon"

													elif Difficulty <= 50 and Difficulty >= 0:
														difficulty = "<:Common:573784881012932618> " 
														diff = "Common"
		
												elif userinfo["location"] == "The Forest":
													chance = random.randint(1, 100)

													if chance >= 90:
														debi = randchoice(["Phantasm"])
													elif chance <= 90 and chance >= 60:
														debi = randchoice(["Zombie"])
													elif chance <= 60 and chance >= 0:
														debi = randchoice(["Wolf", "Goblin"])

													Difficulty = random.randint(1, 100)

													userinfo["enemydifficulty"] = "Common"
													if Difficulty >= 99:
														difficulty = "<:Mythical:573784881386225694> " 
														diff ="Mythical"

													elif Difficulty <= 99 and Difficulty >= 90:
														difficulty = "<:Legendary:639425368167809065> " 
														diff = "Legendary"

													elif Difficulty <= 90 and Difficulty >= 70:
														difficulty = "<:Rare:573784880815538186>" 
														diff = "Rare"

													elif Difficulty <= 70 and Difficulty >= 50:
														difficulty = "<:Uncommon:641361853817159685>"
														diff = "Uncommon"

													elif Difficulty <= 50 and Difficulty >= 0:
														difficulty = "<:Common:573784881012932618> " 
														diff = "Common"
				
												elif userinfo["location"] == "Ebony Mountains":
													chance = random.randint(1, 100)

													if chance >= 90:
														debi = randchoice(["The Accursed"])
													elif chance <= 90 and chance >= 60:
														debi = randchoice(["Ebony Guardian"])
													elif chance <= 60 and chance >= 0:
														debi = randchoice(["Elder Dragon", "Hades"])

													Difficulty = random.randint(1, 100)

													userinfo["enemydifficulty"] = "Common"
													if Difficulty >= 99:
														difficulty = "<:Mythical:573784881386225694> " 
														diff ="Mythical"

													elif Difficulty <= 99 and Difficulty >= 90:
														difficulty = "<:Legendary:639425368167809065> " 
														diff = "Legendary"

													elif Difficulty <= 90 and Difficulty >= 70:
														difficulty = "<:Rare:573784880815538186>" 
														diff = "Rare"

													elif Difficulty <= 70 and Difficulty >= 50:
														difficulty = "<:Uncommon:641361853817159685>"
														diff = "Uncommon"

													elif Difficulty <= 50 and Difficulty >= 0:
														difficulty = "<:Common:573784881012932618> " 
														diff = "Common"

												elif userinfo["location"] == "Township of Arkina":
													chance = random.randint(1, 100)

													if chance >= 90:
														debi = randchoice(["The Nameless King"])
													elif chance <= 90 and chance >= 60:
														debi = randchoice(["Harpy"])
													elif chance <= 60 and chance >= 0:
														debi = randchoice(["Ettin", "Dormammu"])

													Difficulty = random.randint(1, 100)

													userinfo["enemydifficulty"] = "Common"
													if Difficulty >= 99:
														difficulty = "<:Mythical:573784881386225694> " 
														diff ="Mythical"

													elif Difficulty <= 99 and Difficulty >= 90:
														difficulty = "<:Legendary:639425368167809065> " 
														diff = "Legendary"

													elif Difficulty <= 90 and Difficulty >= 70:
														difficulty = "<:Rare:573784880815538186>" 
														diff = "Rare"

													elif Difficulty <= 70 and Difficulty >= 50:
														difficulty = "<:Uncommon:641361853817159685>"
														diff = "Uncommon"

													elif Difficulty <= 50 and Difficulty >= 0:
														difficulty = "<:Common:573784881012932618> " 
														diff = "Common"

												elif userinfo["location"] == "Zulanthu":
													chance = random.randint(1, 100)

													if chance >= 90:
														debi = randchoice(["The Venomous"])
													elif chance <= 90 and chance >= 60:
														debi = randchoice(["Largos"])
													elif chance <= 60 and chance >= 0:
														debi = randchoice(["Saurian", "Deathclaw"])

													Difficulty = random.randint(1, 100)

													userinfo["enemydifficulty"] = "Common"
													if Difficulty >= 99:
														difficulty = "<:Mythical:573784881386225694> " 
														diff ="Mythical"

													elif Difficulty <= 99 and Difficulty >= 90:
														difficulty = "<:Legendary:639425368167809065> " 
														diff = "Legendary"

													elif Difficulty <= 90 and Difficulty >= 70:
														difficulty = "<:Rare:573784880815538186>" 
														diff = "Rare"

													elif Difficulty <= 70 and Difficulty >= 50:
														difficulty = "<:Uncommon:641361853817159685>"
														diff = "Uncommon"

													elif Difficulty <= 50 and Difficulty >= 0:
														difficulty = "<:Common:573784881012932618> " 
														diff = "Common"

												elif userinfo["location"] == "Lost City":
													chance = random.randint(1, 100)

													if chance >= 90:
														debi = randchoice(["Death Knight"])
													elif chance <= 90 and chance >= 60:
														debi = randchoice(["Giant"])
													elif chance <= 60 and chance >= 0:
														debi = randchoice(["Skeleton", "Lizardmen"])

													Difficulty = random.randint(1, 100)

													userinfo["enemydifficulty"] = "Common"
													if Difficulty >= 99:
														difficulty = "<:Mythical:573784881386225694> " 
														diff ="Mythical"

													elif Difficulty <= 99 and Difficulty >= 90:
														difficulty = "<:Legendary:639425368167809065> " 
														diff = "Legendary"

													elif Difficulty <= 90 and Difficulty >= 70:
														difficulty = "<:Rare:573784880815538186>" 
														diff = "Rare"

													elif Difficulty <= 70 and Difficulty >= 50:
														difficulty = "<:Uncommon:641361853817159685>"
														diff = "Uncommon"

													elif Difficulty <= 50 and Difficulty >= 0:
														difficulty = "<:Common:573784881012932618> " 
														diff = "Common"
				
												elif userinfo["location"] == "Drenheim":
					
													chance = random.randint(1, 100)
					
													if chance >= 90:
														debi = randchoice(["Frost Dragon"])
													elif chance <= 90 and chance >= 60:
														debi = randchoice(["Frost Orc"])
													elif chance <= 60 and chance >= 0:
														debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
													Difficulty = random.randint(1, 100)

													userinfo["enemydifficulty"] = "Common"
													if Difficulty >= 99:
														difficulty = "<:Mythical:573784881386225694> " 
														diff ="Mythical"

													elif Difficulty <= 99 and Difficulty >= 90:
														difficulty = "<:Legendary:639425368167809065> " 
														diff = "Legendary"

													elif Difficulty <= 90 and Difficulty >= 70:
														difficulty = "<:Rare:573784880815538186>" 
														diff = "Rare"

													elif Difficulty <= 70 and Difficulty >= 50:
														difficulty = "<:Uncommon:641361853817159685>"
														diff = "Uncommon"

													elif Difficulty <= 50 and Difficulty >= 0:
														difficulty = "<:Common:573784881012932618> " 
														diff = "Common"

												trap8 = debi
												trap8diff = diff
												trap8difficulty = difficulty

											
												if userinfo["trap"] >= 9:
													if userinfo["location"] == "Golden Temple":
														chance = random.randint(1, 100)

														if chance >= 90:
															debi = randchoice(["Fire Golem"])
														elif chance <= 90 and chance >= 60:
															debi = randchoice(["Wyvern"])
														elif chance <= 60 and chance >= 0:
															debi = randchoice(["Rachi", "Debin", "Oofer"])

														Difficulty = random.randint(1, 100)

														userinfo["enemydifficulty"] = "Common"
														if Difficulty >= 99:
															difficulty = "<:Mythical:573784881386225694> " 
															diff ="Mythical"

														elif Difficulty <= 99 and Difficulty >= 90:
															difficulty = "<:Legendary:639425368167809065> " 
															diff = "Legendary"

														elif Difficulty <= 90 and Difficulty >= 70:
															difficulty = "<:Rare:573784880815538186>" 
															diff = "Rare"

														elif Difficulty <= 70 and Difficulty >= 50:
															difficulty = "<:Uncommon:641361853817159685>"
															diff = "Uncommon"

														elif Difficulty <= 50 and Difficulty >= 0:
															difficulty = "<:Common:573784881012932618> " 
															diff = "Common"

													elif userinfo["location"] == "Saker Keep":
														chance = random.randint(1, 100)

														if chance >= 90:
															debi = randchoice(["The Corrupted"])
														elif chance <= 90 and chance >= 60:
															debi = randchoice(["Souleater"])
														elif chance <= 60 and chance >= 0:
															debi = randchoice(["Draugr", "Stalker"])
														
														Difficulty = random.randint(1, 100)

														userinfo["enemydifficulty"] = "Common"
														if Difficulty >= 99:
															difficulty = "<:Mythical:573784881386225694> " 
															diff ="Mythical"

														elif Difficulty <= 99 and Difficulty >= 90:
															difficulty = "<:Legendary:639425368167809065> " 
															diff = "Legendary"

														elif Difficulty <= 90 and Difficulty >= 70:
															difficulty = "<:Rare:573784880815538186>" 
															diff = "Rare"

														elif Difficulty <= 70 and Difficulty >= 50:
															difficulty = "<:Uncommon:641361853817159685>"
															diff = "Uncommon"

														elif Difficulty <= 50 and Difficulty >= 0:
															difficulty = "<:Common:573784881012932618> " 
															diff = "Common"
		
													elif userinfo["location"] == "The Forest":
														chance = random.randint(1, 100)

														if chance >= 90:
															debi = randchoice(["Phantasm"])
														elif chance <= 90 and chance >= 60:
															debi = randchoice(["Zombie"])
														elif chance <= 60 and chance >= 0:
															debi = randchoice(["Wolf", "Goblin"])
														
														Difficulty = random.randint(1, 100)

														userinfo["enemydifficulty"] = "Common"
														if Difficulty >= 99:
															difficulty = "<:Mythical:573784881386225694> " 
															diff ="Mythical"

														elif Difficulty <= 99 and Difficulty >= 90:
															difficulty = "<:Legendary:639425368167809065> " 
															diff = "Legendary"

														elif Difficulty <= 90 and Difficulty >= 70:
															difficulty = "<:Rare:573784880815538186>" 
															diff = "Rare"

														elif Difficulty <= 70 and Difficulty >= 50:
															difficulty = "<:Uncommon:641361853817159685>"
															diff = "Uncommon"

														elif Difficulty <= 50 and Difficulty >= 0:
															difficulty = "<:Common:573784881012932618> " 
															diff = "Common"
				
													elif userinfo["location"] == "Ebony Mountains":
														chance = random.randint(1, 100)

														if chance >= 90:
															debi = randchoice(["The Accursed"])
														elif chance <= 90 and chance >= 60:
															debi = randchoice(["Ebony Guardian"])
														elif chance <= 60 and chance >= 0:
															debi = randchoice(["Elder Dragon", "Hades"])

														Difficulty = random.randint(1, 100)

														userinfo["enemydifficulty"] = "Common"
														if Difficulty >= 99:
															difficulty = "<:Mythical:573784881386225694> " 
															diff ="Mythical"

														elif Difficulty <= 99 and Difficulty >= 90:
															difficulty = "<:Legendary:639425368167809065> " 
															diff = "Legendary"

														elif Difficulty <= 90 and Difficulty >= 70:
															difficulty = "<:Rare:573784880815538186>" 
															diff = "Rare"

														elif Difficulty <= 70 and Difficulty >= 50:
															difficulty = "<:Uncommon:641361853817159685>"
															diff = "Uncommon"

														elif Difficulty <= 50 and Difficulty >= 0:
															difficulty = "<:Common:573784881012932618> " 
															diff = "Common"

													elif userinfo["location"] == "Township of Arkina":
														chance = random.randint(1, 100)

														if chance >= 90:
															debi = randchoice(["The Nameless King"])
														elif chance <= 90 and chance >= 60:
															debi = randchoice(["Harpy"])
														elif chance <= 60 and chance >= 0:
															debi = randchoice(["Ettin", "Dormammu"])

														Difficulty = random.randint(1, 100)

														userinfo["enemydifficulty"] = "Common"
														if Difficulty >= 99:
															difficulty = "<:Mythical:573784881386225694> " 
															diff ="Mythical"

														elif Difficulty <= 99 and Difficulty >= 90:
															difficulty = "<:Legendary:639425368167809065> " 
															diff = "Legendary"

														elif Difficulty <= 90 and Difficulty >= 70:
															difficulty = "<:Rare:573784880815538186>" 
															diff = "Rare"

														elif Difficulty <= 70 and Difficulty >= 50:
															difficulty = "<:Uncommon:641361853817159685>"
															diff = "Uncommon"

														elif Difficulty <= 50 and Difficulty >= 0:
															difficulty = "<:Common:573784881012932618> " 
															diff = "Common"

													elif userinfo["location"] == "Zulanthu":
														chance = random.randint(1, 100)

														if chance >= 90:
															debi = randchoice(["The Venomous"])
														elif chance <= 90 and chance >= 60:
															debi = randchoice(["Largos"])
														elif chance <= 60 and chance >= 0:
															debi = randchoice(["Saurian", "Deathclaw"])

														Difficulty = random.randint(1, 100)

														userinfo["enemydifficulty"] = "Common"
														if Difficulty >= 99:
															difficulty = "<:Mythical:573784881386225694> " 
															diff ="Mythical"

														elif Difficulty <= 99 and Difficulty >= 90:
															difficulty = "<:Legendary:639425368167809065> " 
															diff = "Legendary"

														elif Difficulty <= 90 and Difficulty >= 70:
															difficulty = "<:Rare:573784880815538186>" 
															diff = "Rare"

														elif Difficulty <= 70 and Difficulty >= 50:
															difficulty = "<:Uncommon:641361853817159685>"
															diff = "Uncommon"

														elif Difficulty <= 50 and Difficulty >= 0:
															difficulty = "<:Common:573784881012932618> " 
															diff = "Common"

													elif userinfo["location"] == "Lost City":
														chance = random.randint(1, 100)

														if chance >= 90:
															debi = randchoice(["Death Knight"])
														elif chance <= 90 and chance >= 60:
															debi = randchoice(["Giant"])
														elif chance <= 60 and chance >= 0:
															debi = randchoice(["Skeleton", "Lizardmen"])

														Difficulty = random.randint(1, 100)

														userinfo["enemydifficulty"] = "Common"
														if Difficulty >= 99:
															difficulty = "<:Mythical:573784881386225694> " 
															diff ="Mythical"

														elif Difficulty <= 99 and Difficulty >= 90:
															difficulty = "<:Legendary:639425368167809065> " 
															diff = "Legendary"

														elif Difficulty <= 90 and Difficulty >= 70:
															difficulty = "<:Rare:573784880815538186>" 
															diff = "Rare"

														elif Difficulty <= 70 and Difficulty >= 50:
															difficulty = "<:Uncommon:641361853817159685>"
															diff = "Uncommon"

														elif Difficulty <= 50 and Difficulty >= 0:
															difficulty = "<:Common:573784881012932618> " 
															diff = "Common"
				
													elif userinfo["location"] == "Drenheim":
					
														chance = random.randint(1, 100)
					
														if chance >= 90:
															debi = randchoice(["Frost Dragon"])
														elif chance <= 90 and chance >= 60:
															debi = randchoice(["Frost Orc"])
														elif chance <= 60 and chance >= 0:
															debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
														Difficulty = random.randint(1, 100)

														userinfo["enemydifficulty"] = "Common"
														if Difficulty >= 99:
															difficulty = "<:Mythical:573784881386225694> " 
															diff ="Mythical"

														elif Difficulty <= 99 and Difficulty >= 90:
															difficulty = "<:Legendary:639425368167809065> " 
															diff = "Legendary"

														elif Difficulty <= 90 and Difficulty >= 70:
															difficulty = "<:Rare:573784880815538186>" 
															diff = "Rare"

														elif Difficulty <= 70 and Difficulty >= 50:
															difficulty = "<:Uncommon:641361853817159685>"
															diff = "Uncommon"

														elif Difficulty <= 50 and Difficulty >= 0:
															difficulty = "<:Common:573784881012932618> " 
															diff = "Common"

													trap9 = debi
													trap9diff = diff
													trap9difficulty = difficulty

													if userinfo["trap"] >= 10:
														if userinfo["location"] == "Golden Temple":
															chance = random.randint(1, 100)

															if chance >= 90:
																debi = randchoice(["Fire Golem"])
															elif chance <= 90 and chance >= 60:
																debi = randchoice(["Wyvern"])
															elif chance <= 60 and chance >= 0:
																debi = randchoice(["Rachi", "Debin", "Oofer"])

															Difficulty = random.randint(1, 100)

															userinfo["enemydifficulty"] = "Common"
															if Difficulty >= 99:
																difficulty = "<:Mythical:573784881386225694> " 
																diff ="Mythical"

															elif Difficulty <= 99 and Difficulty >= 90:
																difficulty = "<:Legendary:639425368167809065> " 
																diff = "Legendary"

															elif Difficulty <= 90 and Difficulty >= 70:
																difficulty = "<:Rare:573784880815538186>" 
																diff = "Rare"

															elif Difficulty <= 70 and Difficulty >= 50:
																difficulty = "<:Uncommon:641361853817159685>"
																diff = "Uncommon"

															elif Difficulty <= 50 and Difficulty >= 0:
																difficulty = "<:Common:573784881012932618> " 
																diff = "Common"

														elif userinfo["location"] == "Saker Keep":
															chance = random.randint(1, 100)

															if chance >= 90:
																debi = randchoice(["The Corrupted"])
															elif chance <= 90 and chance >= 60:
																debi = randchoice(["Souleater"])
															elif chance <= 60 and chance >= 0:
																debi = randchoice(["Draugr", "Stalker"])

															Difficulty = random.randint(1, 100)

															userinfo["enemydifficulty"] = "Common"
															if Difficulty >= 99:
																difficulty = "<:Mythical:573784881386225694> " 
																diff ="Mythical"

															elif Difficulty <= 99 and Difficulty >= 90:
																difficulty = "<:Legendary:639425368167809065> " 
																diff = "Legendary"

															elif Difficulty <= 90 and Difficulty >= 70:
																difficulty = "<:Rare:573784880815538186>" 
																diff = "Rare"

															elif Difficulty <= 70 and Difficulty >= 50:
																difficulty = "<:Uncommon:641361853817159685>"
																diff = "Uncommon"

															elif Difficulty <= 50 and Difficulty >= 0:
																difficulty = "<:Common:573784881012932618> " 
																diff = "Common"
		
														elif userinfo["location"] == "The Forest":
															chance = random.randint(1, 100)

															if chance >= 90:
																debi = randchoice(["Phantasm"])
															elif chance <= 90 and chance >= 60:
																debi = randchoice(["Zombie"])
															elif chance <= 60 and chance >= 0:
																debi = randchoice(["Wolf", "Goblin"])
															
															Difficulty = random.randint(1, 100)

															userinfo["enemydifficulty"] = "Common"
															if Difficulty >= 99:
																difficulty = "<:Mythical:573784881386225694> " 
																diff ="Mythical"

															elif Difficulty <= 99 and Difficulty >= 90:
																difficulty = "<:Legendary:639425368167809065> " 
																diff = "Legendary"

															elif Difficulty <= 90 and Difficulty >= 70:
																difficulty = "<:Rare:573784880815538186>" 
																diff = "Rare"

															elif Difficulty <= 70 and Difficulty >= 50:
																difficulty = "<:Uncommon:641361853817159685>"
																diff = "Uncommon"

															elif Difficulty <= 50 and Difficulty >= 0:
																difficulty = "<:Common:573784881012932618> " 
																diff = "Common"
				
														elif userinfo["location"] == "Ebony Mountains":
															chance = random.randint(1, 100)

															if chance >= 90:
																debi = randchoice(["The Accursed"])
															elif chance <= 90 and chance >= 60:
																debi = randchoice(["Ebony Guardian"])
															elif chance <= 60 and chance >= 0:
																debi = randchoice(["Elder Dragon", "Hades"])

															Difficulty = random.randint(1, 100)

															userinfo["enemydifficulty"] = "Common"
															if Difficulty >= 99:
																difficulty = "<:Mythical:573784881386225694> " 
																diff ="Mythical"

															elif Difficulty <= 99 and Difficulty >= 90:
																difficulty = "<:Legendary:639425368167809065> " 
																diff = "Legendary"

															elif Difficulty <= 90 and Difficulty >= 70:
																difficulty = "<:Rare:573784880815538186>" 
																diff = "Rare"

															elif Difficulty <= 70 and Difficulty >= 50:
																difficulty = "<:Uncommon:641361853817159685>"
																diff = "Uncommon"

															elif Difficulty <= 50 and Difficulty >= 0:
																difficulty = "<:Common:573784881012932618> " 
																diff = "Common"

														elif userinfo["location"] == "Township of Arkina":
															chance = random.randint(1, 100)

															if chance >= 90:
																debi = randchoice(["The Nameless King"])
															elif chance <= 90 and chance >= 60:
																debi = randchoice(["Harpy"])
															elif chance <= 60 and chance >= 0:
																debi = randchoice(["Ettin", "Dormammu"])

															Difficulty = random.randint(1, 100)

															userinfo["enemydifficulty"] = "Common"
															if Difficulty >= 99:
																difficulty = "<:Mythical:573784881386225694> " 
																diff ="Mythical"

															elif Difficulty <= 99 and Difficulty >= 90:
																difficulty = "<:Legendary:639425368167809065> " 
																diff = "Legendary"

															elif Difficulty <= 90 and Difficulty >= 70:
																difficulty = "<:Rare:573784880815538186>" 
																diff = "Rare"

															elif Difficulty <= 70 and Difficulty >= 50:
																difficulty = "<:Uncommon:641361853817159685>"
																diff = "Uncommon"

															elif Difficulty <= 50 and Difficulty >= 0:
																difficulty = "<:Common:573784881012932618> " 
																diff = "Common"

														elif userinfo["location"] == "Zulanthu":
															chance = random.randint(1, 100)

															if chance >= 90:
																debi = randchoice(["The Venomous"])
															elif chance <= 90 and chance >= 60:
																debi = randchoice(["Largos"])
															elif chance <= 60 and chance >= 0:
																debi = randchoice(["Saurian", "Deathclaw"])

															Difficulty = random.randint(1, 100)

															userinfo["enemydifficulty"] = "Common"
															if Difficulty >= 99:
																difficulty = "<:Mythical:573784881386225694> " 
																diff ="Mythical"

															elif Difficulty <= 99 and Difficulty >= 90:
																difficulty = "<:Legendary:639425368167809065> " 
																diff = "Legendary"

															elif Difficulty <= 90 and Difficulty >= 70:
																difficulty = "<:Rare:573784880815538186>" 
																diff = "Rare"

															elif Difficulty <= 70 and Difficulty >= 50:
																difficulty = "<:Uncommon:641361853817159685>"
																diff = "Uncommon"

															elif Difficulty <= 50 and Difficulty >= 0:
																difficulty = "<:Common:573784881012932618> " 
																diff = "Common"

														elif userinfo["location"] == "Lost City":
															chance = random.randint(1, 100)

															if chance >= 90:
																debi = randchoice(["Death Knight"])
															elif chance <= 90 and chance >= 60:
																debi = randchoice(["Giant"])
															elif chance <= 60 and chance >= 0:
																debi = randchoice(["Skeleton", "Lizardmen"])

															Difficulty = random.randint(1, 100)

															userinfo["enemydifficulty"] = "Common"
															if Difficulty >= 99:
																difficulty = "<:Mythical:573784881386225694> " 
																diff ="Mythical"

															elif Difficulty <= 99 and Difficulty >= 90:
																difficulty = "<:Legendary:639425368167809065> " 
																diff = "Legendary"

															elif Difficulty <= 90 and Difficulty >= 70:
																difficulty = "<:Rare:573784880815538186>" 
																diff = "Rare"

															elif Difficulty <= 70 and Difficulty >= 50:
																difficulty = "<:Uncommon:641361853817159685>"
																diff = "Uncommon"

															elif Difficulty <= 50 and Difficulty >= 0:
																difficulty = "<:Common:573784881012932618> " 
																diff = "Common"
				
														elif userinfo["location"] == "Drenheim":
					
															chance = random.randint(1, 100)
					
															if chance >= 90:
																debi = randchoice(["Frost Dragon"])
															elif chance <= 90 and chance >= 60:
																debi = randchoice(["Frost Orc"])
															elif chance <= 60 and chance >= 0:
																debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
															Difficulty = random.randint(1, 100)

															userinfo["enemydifficulty"] = "Common"
															if Difficulty >= 99:
																difficulty = "<:Mythical:573784881386225694> " 
																diff ="Mythical"

															elif Difficulty <= 99 and Difficulty >= 90:
																difficulty = "<:Legendary:639425368167809065> " 
																diff = "Legendary"

															elif Difficulty <= 90 and Difficulty >= 70:
																difficulty = "<:Rare:573784880815538186>" 
																diff = "Rare"

															elif Difficulty <= 70 and Difficulty >= 50:
																difficulty = "<:Uncommon:641361853817159685>"
																diff = "Uncommon"

															elif Difficulty <= 50 and Difficulty >= 0:
																difficulty = "<:Common:573784881012932618> " 
																diff = "Common"

														trap10 = debi
														trap10diff = diff
														trap10difficulty = difficulty
													
														if userinfo["trap"] >= 11:
															if userinfo["location"] == "Golden Temple":
																chance = random.randint(1, 100)

																if chance >= 90:
																	debi = randchoice(["Fire Golem"])
																elif chance <= 90 and chance >= 60:
																	debi = randchoice(["Wyvern"])
																elif chance <= 60 and chance >= 0:
																	debi = randchoice(["Rachi", "Debin", "Oofer"])

																Difficulty = random.randint(1, 100)

																userinfo["enemydifficulty"] = "Common"
																if Difficulty >= 99:
																	difficulty = "<:Mythical:573784881386225694> " 
																	diff ="Mythical"

																elif Difficulty <= 99 and Difficulty >= 90:
																	difficulty = "<:Legendary:639425368167809065> " 
																	diff = "Legendary"

																elif Difficulty <= 90 and Difficulty >= 70:
																	difficulty = "<:Rare:573784880815538186>" 
																	diff = "Rare"

																elif Difficulty <= 70 and Difficulty >= 50:
																	difficulty = "<:Uncommon:641361853817159685>"
																	diff = "Uncommon"

																elif Difficulty <= 50 and Difficulty >= 0:
																	difficulty = "<:Common:573784881012932618> " 
																	diff = "Common"

															elif userinfo["location"] == "Saker Keep":
																chance = random.randint(1, 100)

																if chance >= 90:
																	debi = randchoice(["The Corrupted"])
																elif chance <= 90 and chance >= 60:
																	debi = randchoice(["Souleater"])
																elif chance <= 60 and chance >= 0:
																	debi = randchoice(["Draugr", "Stalker"])

																Difficulty = random.randint(1, 100)

																userinfo["enemydifficulty"] = "Common"
																if Difficulty >= 99:
																	difficulty = "<:Mythical:573784881386225694> " 
																	diff ="Mythical"

																elif Difficulty <= 99 and Difficulty >= 90:
																	difficulty = "<:Legendary:639425368167809065> " 
																	diff = "Legendary"

																elif Difficulty <= 90 and Difficulty >= 70:
																	difficulty = "<:Rare:573784880815538186>" 
																	diff = "Rare"

																elif Difficulty <= 70 and Difficulty >= 50:
																	difficulty = "<:Uncommon:641361853817159685>"
																	diff = "Uncommon"

																elif Difficulty <= 50 and Difficulty >= 0:
																	difficulty = "<:Common:573784881012932618> " 
																	diff = "Common"
		
															elif userinfo["location"] == "The Forest":
																chance = random.randint(1, 100)

																if chance >= 90:
																	debi = randchoice(["Phantasm"])
																elif chance <= 90 and chance >= 60:
																	debi = randchoice(["Zombie"])
																elif chance <= 60 and chance >= 0:
																	debi = randchoice(["Wolf", "Goblin"])

																Difficulty = random.randint(1, 100)

																userinfo["enemydifficulty"] = "Common"
																if Difficulty >= 99:
																	difficulty = "<:Mythical:573784881386225694> " 
																	diff ="Mythical"

																elif Difficulty <= 99 and Difficulty >= 90:
																	difficulty = "<:Legendary:639425368167809065> " 
																	diff = "Legendary"

																elif Difficulty <= 90 and Difficulty >= 70:
																	difficulty = "<:Rare:573784880815538186>" 
																	diff = "Rare"

																elif Difficulty <= 70 and Difficulty >= 50:
																	difficulty = "<:Uncommon:641361853817159685>"
																	diff = "Uncommon"

																elif Difficulty <= 50 and Difficulty >= 0:
																	difficulty = "<:Common:573784881012932618> " 
																	diff = "Common"
				
															elif userinfo["location"] == "Ebony Mountains":
																chance = random.randint(1, 100)

																if chance >= 90:
																	debi = randchoice(["The Accursed"])
																elif chance <= 90 and chance >= 60:
																	debi = randchoice(["Ebony Guardian"])
																elif chance <= 60 and chance >= 0:
																	debi = randchoice(["Elder Dragon", "Hades"])
																
																Difficulty = random.randint(1, 100)

																userinfo["enemydifficulty"] = "Common"
																if Difficulty >= 99:
																	difficulty = "<:Mythical:573784881386225694> " 
																	diff ="Mythical"

																elif Difficulty <= 99 and Difficulty >= 90:
																	difficulty = "<:Legendary:639425368167809065> " 
																	diff = "Legendary"

																elif Difficulty <= 90 and Difficulty >= 70:
																	difficulty = "<:Rare:573784880815538186>" 
																	diff = "Rare"

																elif Difficulty <= 70 and Difficulty >= 50:
																	difficulty = "<:Uncommon:641361853817159685>"
																	diff = "Uncommon"

																elif Difficulty <= 50 and Difficulty >= 0:
																	difficulty = "<:Common:573784881012932618> " 
																	diff = "Common"

															elif userinfo["location"] == "Township of Arkina":
																chance = random.randint(1, 100)

																if chance >= 90:
																	debi = randchoice(["The Nameless King"])
																elif chance <= 90 and chance >= 60:
																	debi = randchoice(["Harpy"])
																elif chance <= 60 and chance >= 0:
																	debi = randchoice(["Ettin", "Dormammu"])
																
																Difficulty = random.randint(1, 100)

																userinfo["enemydifficulty"] = "Common"
																if Difficulty >= 99:
																	difficulty = "<:Mythical:573784881386225694> " 
																	diff ="Mythical"

																elif Difficulty <= 99 and Difficulty >= 90:
																	difficulty = "<:Legendary:639425368167809065> " 
																	diff = "Legendary"

																elif Difficulty <= 90 and Difficulty >= 70:
																	difficulty = "<:Rare:573784880815538186>" 
																	diff = "Rare"

																elif Difficulty <= 70 and Difficulty >= 50:
																	difficulty = "<:Uncommon:641361853817159685>"
																	diff = "Uncommon"

																elif Difficulty <= 50 and Difficulty >= 0:
																	difficulty = "<:Common:573784881012932618> " 
																	diff = "Common"

															elif userinfo["location"] == "Zulanthu":
																chance = random.randint(1, 100)

																if chance >= 90:
																	debi = randchoice(["The Venomous"])
																elif chance <= 90 and chance >= 60:
																	debi = randchoice(["Largos"])
																elif chance <= 60 and chance >= 0:
																	debi = randchoice(["Saurian", "Deathclaw"])

																Difficulty = random.randint(1, 100)

																userinfo["enemydifficulty"] = "Common"
																if Difficulty >= 99:
																	difficulty = "<:Mythical:573784881386225694> " 
																	diff ="Mythical"

																elif Difficulty <= 99 and Difficulty >= 90:
																	difficulty = "<:Legendary:639425368167809065> " 
																	diff = "Legendary"

																elif Difficulty <= 90 and Difficulty >= 70:
																	difficulty = "<:Rare:573784880815538186>" 
																	diff = "Rare"

																elif Difficulty <= 70 and Difficulty >= 50:
																	difficulty = "<:Uncommon:641361853817159685>"
																	diff = "Uncommon"

																elif Difficulty <= 50 and Difficulty >= 0:
																	difficulty = "<:Common:573784881012932618> " 
																	diff = "Common"

															elif userinfo["location"] == "Lost City":
																chance = random.randint(1, 100)

																if chance >= 90:
																	debi = randchoice(["Death Knight"])
																elif chance <= 90 and chance >= 60:
																	debi = randchoice(["Giant"])
																elif chance <= 60 and chance >= 0:
																	debi = randchoice(["Skeleton", "Lizardmen"])

																Difficulty = random.randint(1, 100)

																userinfo["enemydifficulty"] = "Common"
																if Difficulty >= 99:
																	difficulty = "<:Mythical:573784881386225694> " 
																	diff ="Mythical"

																elif Difficulty <= 99 and Difficulty >= 90:
																	difficulty = "<:Legendary:639425368167809065> " 
																	diff = "Legendary"

																elif Difficulty <= 90 and Difficulty >= 70:
																	difficulty = "<:Rare:573784880815538186>" 
																	diff = "Rare"

																elif Difficulty <= 70 and Difficulty >= 50:
																	difficulty = "<:Uncommon:641361853817159685>"
																	diff = "Uncommon"

																elif Difficulty <= 50 and Difficulty >= 0:
																	difficulty = "<:Common:573784881012932618> " 
																	diff = "Common"
															elif userinfo["location"] == "Drenheim":
					
																chance = random.randint(1, 100)
					
																if chance >= 90:
																	debi = randchoice(["Frost Dragon"])
																elif chance <= 90 and chance >= 60:
																	debi = randchoice(["Frost Orc"])
																elif chance <= 60 and chance >= 0:
																	debi = randchoice(["Ice Wolf", "Frost Goblin"])
				
																Difficulty = random.randint(1, 100)

																userinfo["enemydifficulty"] = "Common"
																if Difficulty >= 99:
																	difficulty = "<:Mythical:573784881386225694> " 
																	diff ="Mythical"

																elif Difficulty <= 99 and Difficulty >= 90:
																	difficulty = "<:Legendary:639425368167809065> " 
																	diff = "Legendary"

																elif Difficulty <= 90 and Difficulty >= 70:
																	difficulty = "<:Rare:573784880815538186>" 
																	diff = "Rare"

																elif Difficulty <= 70 and Difficulty >= 50:
																	difficulty = "<:Uncommon:641361853817159685>"
																	diff = "Uncommon"

																elif Difficulty <= 50 and Difficulty >= 0:
																	difficulty = "<:Common:573784881012932618> " 
																	diff = "Common"


															trap11 = debi
															trap11diff = diff
															trap11difficulty = difficulty

														
															if userinfo["trap"] >= 12:
																if userinfo["location"] == "Golden Temple":
																	chance = random.randint(1, 100)

																	if chance >= 90:
																		debi = randchoice(["Fire Golem"])
																	elif chance <= 90 and chance >= 60:
																		debi = randchoice(["Wyvern"])
																	elif chance <= 60 and chance >= 0:
																		debi = randchoice(["Rachi", "Debin", "Oofer"])

																	Difficulty = random.randint(1, 100)

																	userinfo["enemydifficulty"] = "Common"
																	if Difficulty >= 99:
																		difficulty = "<:Mythical:573784881386225694> " 
																		diff ="Mythical"

																	elif Difficulty <= 99 and Difficulty >= 90:
																		difficulty = "<:Legendary:639425368167809065> " 
																		diff = "Legendary"

																	elif Difficulty <= 90 and Difficulty >= 70:
																		difficulty = "<:Rare:573784880815538186>" 
																		diff = "Rare"

																	elif Difficulty <= 70 and Difficulty >= 50:
																		difficulty = "<:Uncommon:641361853817159685>"
																		diff = "Uncommon"

																	elif Difficulty <= 50 and Difficulty >= 0:
																		difficulty = "<:Common:573784881012932618> " 
																		diff = "Common"

																elif userinfo["location"] == "Saker Keep":
																	chance = random.randint(1, 100)

																	if chance >= 90:
																		debi = randchoice(["The Corrupted"])
																	elif chance <= 90 and chance >= 60:
																		debi = randchoice(["Souleater"])
																	elif chance <= 60 and chance >= 0:
																		debi = randchoice(["Draugr", "Stalker"])
																	
																	Difficulty = random.randint(1, 100)

																	userinfo["enemydifficulty"] = "Common"
																	if Difficulty >= 99:
																		difficulty = "<:Mythical:573784881386225694> " 
																		diff ="Mythical"

																	elif Difficulty <= 99 and Difficulty >= 90:
																		difficulty = "<:Legendary:639425368167809065> " 
																		diff = "Legendary"

																	elif Difficulty <= 90 and Difficulty >= 70:
																		difficulty = "<:Rare:573784880815538186>" 
																		diff = "Rare"

																	elif Difficulty <= 70 and Difficulty >= 50:
																		difficulty = "<:Uncommon:641361853817159685>"
																		diff = "Uncommon"

																	elif Difficulty <= 50 and Difficulty >= 0:
																		difficulty = "<:Common:573784881012932618> " 
																		diff = "Common"
		
																elif userinfo["location"] == "The Forest":
																	chance = random.randint(1, 100)

																	if chance >= 90:
																		debi = randchoice(["Phantasm"])
																	elif chance <= 90 and chance >= 60:
																		debi = randchoice(["Zombie"])
																	elif chance <= 60 and chance >= 0:
																		debi = randchoice(["Wolf", "Goblin"])

																	Difficulty = random.randint(1, 100)

																	userinfo["enemydifficulty"] = "Common"
																	if Difficulty >= 99:
																		difficulty = "<:Mythical:573784881386225694> " 
																		diff ="Mythical"

																	elif Difficulty <= 99 and Difficulty >= 90:
																		difficulty = "<:Legendary:639425368167809065> " 
																		diff = "Legendary"

																	elif Difficulty <= 90 and Difficulty >= 70:
																		difficulty = "<:Rare:573784880815538186>" 
																		diff = "Rare"

																	elif Difficulty <= 70 and Difficulty >= 50:
																		difficulty = "<:Uncommon:641361853817159685>"
																		diff = "Uncommon"

																	elif Difficulty <= 50 and Difficulty >= 0:
																		difficulty = "<:Common:573784881012932618> " 
																		diff = "Common"
				
																elif userinfo["location"] == "Ebony Mountains":
																	chance = random.randint(1, 100)

																	if chance >= 90:
																		debi = randchoice(["The Accursed"])
																	elif chance <= 90 and chance >= 60:
																		debi = randchoice(["Ebony Guardian"])
																	elif chance <= 60 and chance >= 0:
																		debi = randchoice(["Elder Dragon", "Hades"])

																	Difficulty = random.randint(1, 100)

																	userinfo["enemydifficulty"] = "Common"
																	if Difficulty >= 99:
																		difficulty = "<:Mythical:573784881386225694> " 
																		diff ="Mythical"

																	elif Difficulty <= 99 and Difficulty >= 90:
																		difficulty = "<:Legendary:639425368167809065> " 
																		diff = "Legendary"

																	elif Difficulty <= 90 and Difficulty >= 70:
																		difficulty = "<:Rare:573784880815538186>" 
																		diff = "Rare"

																	elif Difficulty <= 70 and Difficulty >= 50:
																		difficulty = "<:Uncommon:641361853817159685>"
																		diff = "Uncommon"

																	elif Difficulty <= 50 and Difficulty >= 0:
																		difficulty = "<:Common:573784881012932618> " 
																		diff = "Common"

																elif userinfo["location"] == "Township of Arkina":
																	chance = random.randint(1, 100)

																	if chance >= 90:
																		debi = randchoice(["The Nameless King"])
																	elif chance <= 90 and chance >= 60:
																		debi = randchoice(["Harpy"])
																	elif chance <= 60 and chance >= 0:
																		debi = randchoice(["Ettin", "Dormammu"])

																	Difficulty = random.randint(1, 100)

																	userinfo["enemydifficulty"] = "Common"
																	if Difficulty >= 99:
																		difficulty = "<:Mythical:573784881386225694> " 
																		diff ="Mythical"

																	elif Difficulty <= 99 and Difficulty >= 90:
																		difficulty = "<:Legendary:639425368167809065> " 
																		diff = "Legendary"

																	elif Difficulty <= 90 and Difficulty >= 70:
																		difficulty = "<:Rare:573784880815538186>" 
																		diff = "Rare"

																	elif Difficulty <= 70 and Difficulty >= 50:
																		difficulty = "<:Uncommon:641361853817159685>"
																		diff = "Uncommon"

																	elif Difficulty <= 50 and Difficulty >= 0:
																		difficulty = "<:Common:573784881012932618> " 
																		diff = "Common"

																elif userinfo["location"] == "Zulanthu":
																	chance = random.randint(1, 100)

																	if chance >= 90:
																		debi = randchoice(["The Venomous"])
																	elif chance <= 90 and chance >= 60:
																		debi = randchoice(["Largos"])
																	elif chance <= 60 and chance >= 0:
																		debi = randchoice(["Saurian", "Deathclaw"])

																	Difficulty = random.randint(1, 100)

																	userinfo["enemydifficulty"] = "Common"
																	if Difficulty >= 99:
																		difficulty = "<:Mythical:573784881386225694> " 
																		diff ="Mythical"

																	elif Difficulty <= 99 and Difficulty >= 90:
																		difficulty = "<:Legendary:639425368167809065> " 
																		diff = "Legendary"

																	elif Difficulty <= 90 and Difficulty >= 70:
																		difficulty = "<:Rare:573784880815538186>" 
																		diff = "Rare"

																	elif Difficulty <= 70 and Difficulty >= 50:
																		difficulty = "<:Uncommon:641361853817159685>"
																		diff = "Uncommon"

																	elif Difficulty <= 50 and Difficulty >= 0:
																		difficulty = "<:Common:573784881012932618> " 
																		diff = "Common"

																elif userinfo["location"] == "Lost City":
																	chance = random.randint(1, 100)

																	if chance >= 90:
																		debi = randchoice(["Death Knight"])
																	elif chance <= 90 and chance >= 60:
																		debi = randchoice(["Giant"])
																	elif chance <= 60 and chance >= 0:
																		debi = randchoice(["Skeleton", "Lizardmen"])

																	Difficulty = random.randint(1, 100)

																	userinfo["enemydifficulty"] = "Common"
																	if Difficulty >= 99:
																		difficulty = "<:Mythical:573784881386225694> " 
																		diff ="Mythical"

																	elif Difficulty <= 99 and Difficulty >= 90:
																		difficulty = "<:Legendary:639425368167809065> " 
																		diff = "Legendary"

																	elif Difficulty <= 90 and Difficulty >= 70:
																		difficulty = "<:Rare:573784880815538186>" 
																		diff = "Rare"

																	elif Difficulty <= 70 and Difficulty >= 50:
																		difficulty = "<:Uncommon:641361853817159685>"
																		diff = "Uncommon"

																	elif Difficulty <= 50 and Difficulty >= 0:
																		difficulty = "<:Common:573784881012932618> " 
																		diff = "Common"
				
																elif userinfo["location"] == "Drenheim":
					
																	chance = random.randint(1, 100)
					
																	if chance >= 90:
																		debi = randchoice(["Frost Dragon"])
																	elif chance <= 90 and chance >= 60:
																		debi = randchoice(["Frost Orc"])
																	elif chance <= 60 and chance >= 0:
																		debi = randchoice(["Ice Wolf", "Frost Goblin"])
					
																	Difficulty = random.randint(1, 100)

																	userinfo["enemydifficulty"] = "Common"
																	if Difficulty >= 99:
																		difficulty = "<:Mythical:573784881386225694> " 
																		diff ="Mythical"

																	elif Difficulty <= 99 and Difficulty >= 90:
																		difficulty = "<:Legendary:639425368167809065> " 
																		diff = "Legendary"

																	elif Difficulty <= 90 and Difficulty >= 70:
																		difficulty = "<:Rare:573784880815538186>" 
																		diff = "Rare"

																	elif Difficulty <= 70 and Difficulty >= 50:
																		difficulty = "<:Uncommon:641361853817159685>"
																		diff = "Uncommon"

																	elif Difficulty <= 50 and Difficulty >= 0:
																		difficulty = "<:Common:573784881012932618> " 
																		diff = "Common"	

																trap12 = debi
																trap12diff = diff
																trap12difficulty = difficulty
																
																if userinfo["trap"] >= 13:
																	if userinfo["location"] == "Golden Temple":
																		chance = random.randint(1, 100)

																		if chance >= 90:
																			debi = randchoice(["Fire Golem"])
																		elif chance <= 90 and chance >= 60:
																			debi = randchoice(["Wyvern"])
																		elif chance <= 60 and chance >= 0:
																			debi = randchoice(["Rachi", "Debin", "Oofer"])
	
																		Difficulty = random.randint(1, 100)

																		userinfo["enemydifficulty"] = "Common"
																		if Difficulty >= 99:
																			difficulty = "<:Mythical:573784881386225694> " 
																			diff ="Mythical"

																		elif Difficulty <= 99 and Difficulty >= 90:
																			difficulty = "<:Legendary:639425368167809065> " 
																			diff = "Legendary"

																		elif Difficulty <= 90 and Difficulty >= 70:
																			difficulty = "<:Rare:573784880815538186>" 
																			diff = "Rare"

																		elif Difficulty <= 70 and Difficulty >= 50:
																			difficulty = "<:Uncommon:641361853817159685>"
																			diff = "Uncommon"

																		elif Difficulty <= 50 and Difficulty >= 0:
																			difficulty = "<:Common:573784881012932618> " 
																			diff = "Common"	

																	elif userinfo["location"] == "Saker Keep":
																		chance = random.randint(1, 100)

																		if chance >= 90:
																			debi = randchoice(["The Corrupted"])
																		elif chance <= 90 and chance >= 60:
																			debi = randchoice(["Souleater"])
																		elif chance <= 60 and chance >= 0:
																			debi = randchoice(["Draugr", "Stalker"])
																			
																		Difficulty = random.randint(1, 100)

																		userinfo["enemydifficulty"] = "Common"
																		if Difficulty >= 99:
																			difficulty = "<:Mythical:573784881386225694> " 
																			diff ="Mythical"

																		elif Difficulty <= 99 and Difficulty >= 90:
																			difficulty = "<:Legendary:639425368167809065> " 
																			diff = "Legendary"

																		elif Difficulty <= 90 and Difficulty >= 70:
																			difficulty = "<:Rare:573784880815538186>" 
																			diff = "Rare"

																		elif Difficulty <= 70 and Difficulty >= 50:
																			difficulty = "<:Uncommon:641361853817159685>"
																			diff = "Uncommon"

																		elif Difficulty <= 50 and Difficulty >= 0:
																			difficulty = "<:Common:573784881012932618> " 
																			diff = "Common"	
		
																	elif userinfo["location"] == "The Forest":
																		chance = random.randint(1, 100)

																		if chance >= 90:
																			debi = randchoice(["Phantasm"])
																		elif chance <= 90 and chance >= 60:
																			debi = randchoice(["Zombie"])
																		elif chance <= 60 and chance >= 0:
																			debi = randchoice(["Wolf", "Goblin"])
																			
																		Difficulty = random.randint(1, 100)

																		userinfo["enemydifficulty"] = "Common"
																		if Difficulty >= 99:
																			difficulty = "<:Mythical:573784881386225694> " 
																			diff ="Mythical"

																		elif Difficulty <= 99 and Difficulty >= 90:
																			difficulty = "<:Legendary:639425368167809065> " 
																			diff = "Legendary"

																		elif Difficulty <= 90 and Difficulty >= 70:
																			difficulty = "<:Rare:573784880815538186>" 
																			diff = "Rare"

																		elif Difficulty <= 70 and Difficulty >= 50:
																			difficulty = "<:Uncommon:641361853817159685>"
																			diff = "Uncommon"

																		elif Difficulty <= 50 and Difficulty >= 0:
																			difficulty = "<:Common:573784881012932618> " 
																			diff = "Common"	
				
																	elif userinfo["location"] == "Ebony Mountains":
																		chance = random.randint(1, 100)

																		if chance >= 90:
																			debi = randchoice(["The Accursed"])
																		elif chance <= 90 and chance >= 60:
																			debi = randchoice(["Ebony Guardian"])
																		elif chance <= 60 and chance >= 0:
																			debi = randchoice(["Elder Dragon", "Hades"])
																			
																		Difficulty = random.randint(1, 100)

																		userinfo["enemydifficulty"] = "Common"
																		if Difficulty >= 99:
																			difficulty = "<:Mythical:573784881386225694> " 
																			diff ="Mythical"

																		elif Difficulty <= 99 and Difficulty >= 90:
																			difficulty = "<:Legendary:639425368167809065> " 
																			diff = "Legendary"

																		elif Difficulty <= 90 and Difficulty >= 70:
																			difficulty = "<:Rare:573784880815538186>" 
																			diff = "Rare"

																		elif Difficulty <= 70 and Difficulty >= 50:
																			difficulty = "<:Uncommon:641361853817159685>"
																			diff = "Uncommon"

																		elif Difficulty <= 50 and Difficulty >= 0:
																			difficulty = "<:Common:573784881012932618> " 
																			diff = "Common"	

																	elif userinfo["location"] == "Township of Arkina":
																		chance = random.randint(1, 100)

																		if chance >= 90:
																			debi = randchoice(["The Nameless King"])
																		elif chance <= 90 and chance >= 60:
																			debi = randchoice(["Harpy"])
																		elif chance <= 60 and chance >= 0:
																			debi = randchoice(["Ettin", "Dormammu"])
																			
																		Difficulty = random.randint(1, 100)

																		userinfo["enemydifficulty"] = "Common"
																		if Difficulty >= 99:
																			difficulty = "<:Mythical:573784881386225694> " 
																			diff ="Mythical"

																		elif Difficulty <= 99 and Difficulty >= 90:
																			difficulty = "<:Legendary:639425368167809065> " 
																			diff = "Legendary"

																		elif Difficulty <= 90 and Difficulty >= 70:
																			difficulty = "<:Rare:573784880815538186>" 
																			diff = "Rare"

																		elif Difficulty <= 70 and Difficulty >= 50:
																			difficulty = "<:Uncommon:641361853817159685>"
																			diff = "Uncommon"

																		elif Difficulty <= 50 and Difficulty >= 0:
																			difficulty = "<:Common:573784881012932618> " 
																			diff = "Common"	

																	elif userinfo["location"] == "Zulanthu":
																		chance = random.randint(1, 100)

																		if chance >= 90:
																			debi = randchoice(["The Venomous"])
																		elif chance <= 90 and chance >= 60:
																			debi = randchoice(["Largos"])
																		elif chance <= 60 and chance >= 0:
																			debi = randchoice(["Saurian", "Deathclaw"])
																			
																		Difficulty = random.randint(1, 100)

																		userinfo["enemydifficulty"] = "Common"
																		if Difficulty >= 99:
																			difficulty = "<:Mythical:573784881386225694> " 
																			diff ="Mythical"

																		elif Difficulty <= 99 and Difficulty >= 90:
																			difficulty = "<:Legendary:639425368167809065> " 
																			diff = "Legendary"

																		elif Difficulty <= 90 and Difficulty >= 70:
																			difficulty = "<:Rare:573784880815538186>" 
																			diff = "Rare"

																		elif Difficulty <= 70 and Difficulty >= 50:
																			difficulty = "<:Uncommon:641361853817159685>"
																			diff = "Uncommon"

																		elif Difficulty <= 50 and Difficulty >= 0:
																			difficulty = "<:Common:573784881012932618> " 
																			diff = "Common"	

																	elif userinfo["location"] == "Lost City":
																		chance = random.randint(1, 100)

																		if chance >= 90:
																			debi = randchoice(["Death Knight"])
																		elif chance <= 90 and chance >= 60:
																			debi = randchoice(["Giant"])
																		elif chance <= 60 and chance >= 0:
																			debi = randchoice(["Skeleton", "Lizardmen"])
	
																		Difficulty = random.randint(1, 100)

																		userinfo["enemydifficulty"] = "Common"
																		if Difficulty >= 99:
																			difficulty = "<:Mythical:573784881386225694> " 
																			diff ="Mythical"

																		elif Difficulty <= 99 and Difficulty >= 90:
																			difficulty = "<:Legendary:639425368167809065> " 
																			diff = "Legendary"

																		elif Difficulty <= 90 and Difficulty >= 70:
																			difficulty = "<:Rare:573784880815538186>" 
																			diff = "Rare"

																		elif Difficulty <= 70 and Difficulty >= 50:
																			difficulty = "<:Uncommon:641361853817159685>"
																			diff = "Uncommon"

																		elif Difficulty <= 50 and Difficulty >= 0:
																			difficulty = "<:Common:573784881012932618> " 
																			diff = "Common"	
				
																	elif userinfo["location"] == "Drenheim":
					
																		chance = random.randint(1, 100)
					
																		if chance >= 90:
																			debi = randchoice(["Frost Dragon"])
																		elif chance <= 90 and chance >= 60:
																			debi = randchoice(["Frost Orc"])
																		elif chance <= 60 and chance >= 0:
																			debi = randchoice(["Ice Wolf", "Frost Goblin"])
																		
																		Difficulty = random.randint(1, 100)

																		userinfo["enemydifficulty"] = "Common"
																		if Difficulty >= 99:
																			difficulty = "<:Mythical:573784881386225694> " 
																			diff ="Mythical"

																		elif Difficulty <= 99 and Difficulty >= 90:
																			difficulty = "<:Legendary:639425368167809065> " 
																			diff = "Legendary"

																		elif Difficulty <= 90 and Difficulty >= 70:
																			difficulty = "<:Rare:573784880815538186>" 
																			diff = "Rare"

																		elif Difficulty <= 70 and Difficulty >= 50:
																			difficulty = "<:Uncommon:641361853817159685>"
																			diff = "Uncommon"

																		elif Difficulty <= 50 and Difficulty >= 0:
																			difficulty = "<:Common:573784881012932618> " 
																			diff = "Common"	
				
																	trap13 = debi
																	trap13diff = diff
																	trap13difficulty = difficulty
			except:
				return

			guild = ctx.guild
			guildinfo = db.servers.find_one({ "_id": guild.id })
			effectiveguildbonus = guildinfo["bonus"]
															
			trap1enemygold = 0
			trap1xpgain = 0
			trap2enemygold = 0
			trap2xpgain = 0
			trap3enemygold = 0
			trap3xpgain = 0
			trap4enemygold = 0
			trap4xpgain = 0
			trap5enemygold = 0
			trap5xpgain = 0
			trap6enemygold = 0
			trap6xpgain = 0
			trap7enemygold = 0
			trap7xpgain = 0
			trap8enemygold = 0
			trap8xpgain = 0
			trap9enemygold = 0
			trap9xpgain = 0
			trap10enemygold = 0
			trap10xpgain = 0
			trap11enemygold = 0
			trap11xpgain = 0
			trap12enemygold = 0
			trap12xpgain = 0
			trap13enemygold = 0
			trap13xpgain = 0



			try:
				# GOLDEN TEMPLE
				if trap1 == "Rachi" or trap1 == "Debin" or trap1 == "Oofer":				
					trap1enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap1xpgain = random.randint(5, 25)
				
					if trap1diff == "Uncommon":									
						trap1enemygold = (int((trap1enemygold / 100) * 120))					
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					if trap1diff == "Rare":					
		
						trap1enemygold = (int((trap1enemygold / 100) * 130))					
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					if trap1diff == "Legendary":					
						
						trap1enemygold = (int((trap1enemygold / 100) * 140))					
						trap1xpgain = (int((trap1xpgain / 100) * 140))	

					if trap1diff == "Mythical":					
					
						trap1enemygold = (int((trap1enemygold / 100) * 150))					
						trap1xpgain = (int((trap1xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap1 == "Wyvern":
					trap1enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap1xpgain = random.randint(10, 30)
				
					if trap1diff == "Uncommon":					
						trap1enemygold = (int((trap1enemygold / 100) * 120))					
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":					
						trap1enemygold = (int((trap1enemygold / 100) * 130))					
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":					
						trap1enemygold = (int((trap1enemygold / 100) * 140))					
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":				
						trap1enemygold = (int((trap1enemygold / 100) * 150))			
						trap1xpgain = (int((trap1xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap1 == "Fire Golem":
					trap1enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap1xpgain = random.randint(20, 40)

					if trap1diff == "Uncommon":	
						trap1enemygold = (int((trap1enemygold / 100) * 120))					
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":					
						trap1enemygold = (int((trap1enemygold / 100) * 130))					
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":					
						trap1enemygold = (int((trap1enemygold / 100) * 140))					
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))					
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# SAKER KEEP
				elif trap1 == "Draugr" or trap1 == "Stalker":
					trap1enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap1xpgain = random.randint(15, 35)

					if trap1diff == "Uncommon":					
						trap1enemygold = (int((trap1enemygold / 100) * 120))					
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":					
						trap1enemygold = (int((trap1enemygold / 100) * 130))					
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":					
						trap1enemygold = (int((trap1enemygold / 100) * 140))					
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":					
						trap1enemygold = (int((trap1enemygold / 100) * 150))			
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# SAKER KEEP
				elif trap1 == "Souleater":
					trap1enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap1xpgain = random.randint(20, 40)
				
					if trap1diff == "Uncommon":					
						trap1enemygold = (int((trap1enemygold / 100) * 120))					
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":					
						trap1enemygold = (int((trap1enemygold / 100) * 130))					
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":					
						trap1enemygold = (int((trap1enemygold / 100) * 140))					
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":				
						trap1enemygold = (int((trap1enemygold / 100) * 150))				
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# SAKER KEEP
				elif trap1 == "The Corrupted":
					trap1enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap1xpgain = random.randint(30, 50)
				
					if trap1diff == "Uncommon":				
						trap1enemygold = (int((trap1enemygold / 100) * 120))					
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":					
						trap1enemygold = (int((trap1enemygold / 100) * 130))					
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":					
						trap1enemygold = (int((trap1enemygold / 100) * 140))					
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":					
						trap1enemygold = (int((trap1enemygold / 100) * 150))					
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# THE FOREST
				elif trap1 == "Wolf" or trap1 == "Goblin":
					trap1enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap1xpgain = random.randint(25, 45)

					if trap1diff == "Uncommon":					
						trap1enemygold = (int((trap1enemygold / 100) * 120))					
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":					
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":					
						trap1enemygold = (int((trap1enemygold / 100) * 150))					
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# THE FOREST
				elif trap1 == "Zombie":				
					trap1enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap1xpgain = random.randint(30, 50)

					if trap1diff == "Uncommon":				
						trap1enemygold = (int((trap1enemygold / 100) * 120))					
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":				
						trap1enemygold = (int((trap1enemygold / 100) * 130))					
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":					
						trap1enemygold = (int((trap1enemygold / 100) * 140))					
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":				
						trap1enemygold = (int((trap1enemygold / 100) * 150))					
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# THE FOREST
				elif trap1 == "Phantasm":
					trap1enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap1xpgain = random.randint(40, 60)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap1 == "Elder Dragon" or trap1 == "Hades":
					trap1enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap1xpgain = random.randint(35, 55)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					if trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap1 == "Ebony Guardian":
				
					trap1enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap1xpgain = random.randint(40, 60)

					if trap1diff == "Uncommon":
						
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap1 == "The Accursed" :
					trap1enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap1xpgain = random.randint(50, 70)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap1 == "Ettin" or trap1 == "Dormammu":
					trap1enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap1xpgain = random.randint(45, 65)
				
					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap1 == "Harpy":
					trap1enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap1xpgain = random.randint(50, 70)
				
					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap1 == "The Nameless King":
					trap1enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap1xpgain = random.randint(60, 80)
				
					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# ZULANTHU
				elif trap1 == "Deathclaw" or trap1 == "Saurian":
					trap1enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap1xpgain = random.randint(55, 75)
				
					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# ZULANTHU
				elif trap1 == "Largos":
					trap1enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap1xpgain = random.randint(60, 80)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# ZULANTHU
				elif trap1 == "The Venomous":
					trap1enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap1xpgain = random.randint(70, 90)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# LOST CITY
				elif trap1 == "Skeleton" or trap1 == "Lizardmen":
					trap1enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap1xpgain = random.randint(65, 85)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# LOST CITY
				elif trap1 == "Giant":
					trap1enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap1xpgain = random.randint(70, 90)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# LOST CITY
				elif trap1 == "Death Knight": 
					trap1enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap1xpgain = random.randint(80, 100)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# DRENHEIM
				elif trap1 == "Ice Wolf" or trap1 == "Frost Goblin":
					trap1enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap1xpgain = random.randint(75, 95)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# DRENHEIM
				elif trap1 == "Frost Orc":
					trap1enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap1xpgain = random.randint(80, 100)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))

				# DRENHEIM
				elif trap1 == "Frost Dragon":
					trap1enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap1xpgain = random.randint(90, 110)

					if trap1diff == "Uncommon":
						trap1enemygold = (int((trap1enemygold / 100) * 120))
						trap1xpgain = (int((trap1xpgain / 100) * 120))

					elif trap1diff == "Rare":
						trap1enemygold = (int((trap1enemygold / 100) * 130))
						trap1xpgain = (int((trap1xpgain / 100) * 130))

					elif trap1diff == "Legendary":
						trap1enemygold = (int((trap1enemygold / 100) * 140))
						trap1xpgain = (int((trap1xpgain / 100) * 140))

					elif trap1diff == "Mythical":
						trap1enemygold = (int((trap1enemygold / 100) * 150))
						trap1xpgain = (int((trap1xpgain / 100) * 150))


				# GOLDEN TEMPLE
				if trap2 == "Rachi" or trap2 == "Debin" or trap2 == "Oofer":				
					trap2enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap2xpgain = random.randint(5, 25)
				
					if trap2diff == "Uncommon":									
						trap2enemygold = (int((trap2enemygold / 100) * 120))					
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					if trap2diff == "Rare":					
		
						trap2enemygold = (int((trap2enemygold / 100) * 130))					
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					if trap2diff == "Legendary":					
						
						trap2enemygold = (int((trap2enemygold / 100) * 140))					
						trap2xpgain = (int((trap2xpgain / 100) * 140))	

					if trap2diff == "Mythical":					
					
						trap2enemygold = (int((trap2enemygold / 100) * 150))					
						trap2xpgain = (int((trap2xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap2 == "Wyvern":
					trap2enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap2xpgain = random.randint(10, 30)
				
					if trap2diff == "Uncommon":					
						trap2enemygold = (int((trap2enemygold / 100) * 120))					
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":					
						trap2enemygold = (int((trap2enemygold / 100) * 130))					
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":					
						trap2enemygold = (int((trap2enemygold / 100) * 140))					
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":				
						trap2enemygold = (int((trap2enemygold / 100) * 150))			
						trap2xpgain = (int((trap2xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap2 == "Fire Golem":
					trap2enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap2xpgain = random.randint(20, 40)

					if trap2diff == "Uncommon":	
						trap2enemygold = (int((trap2enemygold / 100) * 120))					
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":					
						trap2enemygold = (int((trap2enemygold / 100) * 130))					
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":					
						trap2enemygold = (int((trap2enemygold / 100) * 140))					
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))					
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# SAKER KEEP
				elif trap2 == "Draugr" or trap2 == "Stalker":
					trap2enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap2xpgain = random.randint(15, 35)

					if trap2diff == "Uncommon":					
						trap2enemygold = (int((trap2enemygold / 100) * 120))					
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":					
						trap2enemygold = (int((trap2enemygold / 100) * 130))					
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":					
						trap2enemygold = (int((trap2enemygold / 100) * 140))					
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":					
						trap2enemygold = (int((trap2enemygold / 100) * 150))			
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# SAKER KEEP
				elif trap2 == "Souleater":
					trap2enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap2xpgain = random.randint(20, 40)
				
					if trap2diff == "Uncommon":					
						trap2enemygold = (int((trap2enemygold / 100) * 120))					
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":					
						trap2enemygold = (int((trap2enemygold / 100) * 130))					
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":					
						trap2enemygold = (int((trap2enemygold / 100) * 140))					
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":				
						trap2enemygold = (int((trap2enemygold / 100) * 150))				
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# SAKER KEEP
				elif trap2 == "The Corrupted":
					trap2enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap2xpgain = random.randint(30, 50)
				
					if trap2diff == "Uncommon":				
						trap2enemygold = (int((trap2enemygold / 100) * 120))					
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":					
						trap2enemygold = (int((trap2enemygold / 100) * 130))					
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":					
						trap2enemygold = (int((trap2enemygold / 100) * 140))					
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":					
						trap2enemygold = (int((trap2enemygold / 100) * 150))					
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# THE FOREST
				elif trap2 == "Wolf" or trap2 == "Goblin":
					trap2enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap2xpgain = random.randint(25, 45)

					if trap2diff == "Uncommon":					
						trap2enemygold = (int((trap2enemygold / 100) * 120))					
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":					
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":					
						trap2enemygold = (int((trap2enemygold / 100) * 150))					
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# THE FOREST
				elif trap2 == "Zombie":				
					trap2enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap2xpgain = random.randint(30, 50)

					if trap2diff == "Uncommon":				
						trap2enemygold = (int((trap2enemygold / 100) * 120))					
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":				
						trap2enemygold = (int((trap2enemygold / 100) * 130))					
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":					
						trap2enemygold = (int((trap2enemygold / 100) * 140))					
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":				
						trap2enemygold = (int((trap2enemygold / 100) * 150))					
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# THE FOREST
				elif trap2 == "Phantasm":
					trap2enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap2xpgain = random.randint(40, 60)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap2 == "Elder Dragon" or trap2 == "Hades":
					trap2enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap2xpgain = random.randint(35, 55)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					if trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap2 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap2enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap2xpgain = random.randint(40, 60)

					if trap2diff == "Uncommon":
						
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap2 == "The Accursed" :
					trap2enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap2xpgain = random.randint(50, 70)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap2 == "Ettin" or trap2 == "Dormammu":
					trap2enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap2xpgain = random.randint(45, 65)
				
					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap2 == "Harpy":
					trap2enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap2xpgain = random.randint(50, 70)
				
					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap2 == "The Nameless King":
					trap2enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap2xpgain = random.randint(60, 80)
				
					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# ZULANTHU
				elif trap2 == "Deathclaw" or trap2 == "Saurian":
					trap2enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap2xpgain = random.randint(55, 75)
				
					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# ZULANTHU
				elif trap2 == "Largos":
					trap2enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap2xpgain = random.randint(60, 80)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# ZULANTHU
				elif trap2 == "The Venomous":
					trap2enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap2xpgain = random.randint(70, 90)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# LOST CITY
				elif trap2 == "Skeleton" or trap2 == "Lizardmen":
					trap2enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap2xpgain = random.randint(65, 85)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# LOST CITY
				elif trap2 == "Giant":
					trap2enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap2xpgain = random.randint(70, 90)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# LOST CITY
				elif trap2 == "Death Knight": 
					trap2enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap2xpgain = random.randint(80, 100)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# DRENHEIM
				elif trap2 == "Ice Wolf" or trap2 == "Frost Goblin":
					trap2enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap2xpgain = random.randint(75, 95)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# DRENHEIM
				elif trap2 == "Frost Orc":
					trap2enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap2xpgain = random.randint(80, 100)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))

				# DRENHEIM
				elif trap2 == "Frost Dragon":
					trap2enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap2xpgain = random.randint(90, 110)

					if trap2diff == "Uncommon":
						trap2enemygold = (int((trap2enemygold / 100) * 120))
						trap2xpgain = (int((trap2xpgain / 100) * 120))

					elif trap2diff == "Rare":
						trap2enemygold = (int((trap2enemygold / 100) * 130))
						trap2xpgain = (int((trap2xpgain / 100) * 130))

					elif trap2diff == "Legendary":
						trap2enemygold = (int((trap2enemygold / 100) * 140))
						trap2xpgain = (int((trap2xpgain / 100) * 140))

					elif trap2diff == "Mythical":
						trap2enemygold = (int((trap2enemygold / 100) * 150))
						trap2xpgain = (int((trap2xpgain / 100) * 150))






				# GOLDEN TEMPLE
				if trap3 == "Rachi" or trap3 == "Debin" or trap3 == "Oofer":				
					trap3enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap3xpgain = random.randint(5, 25)
				
					if trap3diff == "Uncommon":									
						trap3enemygold = (int((trap3enemygold / 100) * 120))					
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					if trap3diff == "Rare":					
		
						trap3enemygold = (int((trap3enemygold / 100) * 130))					
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					if trap3diff == "Legendary":					
						
						trap3enemygold = (int((trap3enemygold / 100) * 140))					
						trap3xpgain = (int((trap3xpgain / 100) * 140))	

					if trap3diff == "Mythical":					
					
						trap3enemygold = (int((trap3enemygold / 100) * 150))					
						trap3xpgain = (int((trap3xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap3 == "Wyvern":
					trap3enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap3xpgain = random.randint(10, 30)
				
					if trap3diff == "Uncommon":					
						trap3enemygold = (int((trap3enemygold / 100) * 120))					
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":					
						trap3enemygold = (int((trap3enemygold / 100) * 130))					
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":					
						trap3enemygold = (int((trap3enemygold / 100) * 140))					
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":				
						trap3enemygold = (int((trap3enemygold / 100) * 150))			
						trap3xpgain = (int((trap3xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap3 == "Fire Golem":
					trap3enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap3xpgain = random.randint(20, 40)

					if trap3diff == "Uncommon":	
						trap3enemygold = (int((trap3enemygold / 100) * 120))					
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":					
						trap3enemygold = (int((trap3enemygold / 100) * 130))					
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":					
						trap3enemygold = (int((trap3enemygold / 100) * 140))					
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))					
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# SAKER KEEP
				elif trap3 == "Draugr" or trap3 == "Stalker":
					trap3enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap3xpgain = random.randint(15, 35)

					if trap3diff == "Uncommon":					
						trap3enemygold = (int((trap3enemygold / 100) * 120))					
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":					
						trap3enemygold = (int((trap3enemygold / 100) * 130))					
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":					
						trap3enemygold = (int((trap3enemygold / 100) * 140))					
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":					
						trap3enemygold = (int((trap3enemygold / 100) * 150))			
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# SAKER KEEP
				elif trap3 == "Souleater":
					trap3enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap3xpgain = random.randint(20, 40)
				
					if trap3diff == "Uncommon":					
						trap3enemygold = (int((trap3enemygold / 100) * 120))					
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":					
						trap3enemygold = (int((trap3enemygold / 100) * 130))					
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":					
						trap3enemygold = (int((trap3enemygold / 100) * 140))					
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":				
						trap3enemygold = (int((trap3enemygold / 100) * 150))				
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# SAKER KEEP
				elif trap3 == "The Corrupted":
					trap3enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap3xpgain = random.randint(30, 50)
				
					if trap3diff == "Uncommon":				
						trap3enemygold = (int((trap3enemygold / 100) * 120))					
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":					
						trap3enemygold = (int((trap3enemygold / 100) * 130))					
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":					
						trap3enemygold = (int((trap3enemygold / 100) * 140))					
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":					
						trap3enemygold = (int((trap3enemygold / 100) * 150))					
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# THE FOREST
				elif trap3 == "Wolf" or trap3 == "Goblin":
					trap3enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap3xpgain = random.randint(25, 45)

					if trap3diff == "Uncommon":					
						trap3enemygold = (int((trap3enemygold / 100) * 120))					
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":					
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":					
						trap3enemygold = (int((trap3enemygold / 100) * 150))					
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# THE FOREST
				elif trap3 == "Zombie":				
					trap3enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap3xpgain = random.randint(30, 50)

					if trap3diff == "Uncommon":				
						trap3enemygold = (int((trap3enemygold / 100) * 120))					
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":				
						trap3enemygold = (int((trap3enemygold / 100) * 130))					
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":					
						trap3enemygold = (int((trap3enemygold / 100) * 140))					
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":				
						trap3enemygold = (int((trap3enemygold / 100) * 150))					
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# THE FOREST
				elif trap3 == "Phantasm":
					trap3enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap3xpgain = random.randint(40, 60)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap3 == "Elder Dragon" or trap3 == "Hades":
					trap3enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap3xpgain = random.randint(35, 55)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					if trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap3 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap3enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap3xpgain = random.randint(40, 60)

					if trap3diff == "Uncommon":
						
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap3 == "The Accursed" :
					trap3enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap3xpgain = random.randint(50, 70)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap3 == "Ettin" or trap3 == "Dormammu":
					trap3enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap3xpgain = random.randint(45, 65)
				
					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap3 == "Harpy":
					trap3enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap3xpgain = random.randint(50, 70)
				
					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap3 == "The Nameless King":
					trap3enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap3xpgain = random.randint(60, 80)
				
					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# ZULANTHU
				elif trap3 == "Deathclaw" or trap3 == "Saurian":
					trap3enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap3xpgain = random.randint(55, 75)
				
					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# ZULANTHU
				elif trap3 == "Largos":
					trap3enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap3xpgain = random.randint(60, 80)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# ZULANTHU
				elif trap3 == "The Venomous":
					trap3enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap3xpgain = random.randint(70, 90)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# LOST CITY
				elif trap3 == "Skeleton" or trap3 == "Lizardmen":
					trap3enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap3xpgain = random.randint(65, 85)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# LOST CITY
				elif trap3 == "Giant":
					trap3enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap3xpgain = random.randint(70, 90)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# LOST CITY
				elif trap3 == "Death Knight": 
					trap3enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap3xpgain = random.randint(80, 100)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# DRENHEIM
				elif trap3 == "Ice Wolf" or trap3 == "Frost Goblin":
					trap3enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap3xpgain = random.randint(75, 95)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# DRENHEIM
				elif trap3 == "Frost Orc":
					trap3enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap3xpgain = random.randint(80, 100)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))

				# DRENHEIM
				elif trap3 == "Frost Dragon":
					trap3enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap3xpgain = random.randint(90, 110)

					if trap3diff == "Uncommon":
						trap3enemygold = (int((trap3enemygold / 100) * 120))
						trap3xpgain = (int((trap3xpgain / 100) * 120))

					elif trap3diff == "Rare":
						trap3enemygold = (int((trap3enemygold / 100) * 130))
						trap3xpgain = (int((trap3xpgain / 100) * 130))

					elif trap3diff == "Legendary":
						trap3enemygold = (int((trap3enemygold / 100) * 140))
						trap3xpgain = (int((trap3xpgain / 100) * 140))

					elif trap3diff == "Mythical":
						trap3enemygold = (int((trap3enemygold / 100) * 150))
						trap3xpgain = (int((trap3xpgain / 100) * 150))



					
				# GOLDEN TEMPLE
				if trap4 == "Rachi" or trap4 == "Debin" or trap4 == "Oofer":				
					trap4enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap4xpgain = random.randint(5, 25)
				
					if trap4diff == "Uncommon":									
						trap4enemygold = (int((trap4enemygold / 100) * 120))					
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					if trap4diff == "Rare":					
		
						trap4enemygold = (int((trap4enemygold / 100) * 130))					
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					if trap4diff == "Legendary":					
						
						trap4enemygold = (int((trap4enemygold / 100) * 140))					
						trap4xpgain = (int((trap4xpgain / 100) * 140))	

					if trap4diff == "Mythical":					
					
						trap4enemygold = (int((trap4enemygold / 100) * 150))					
						trap4xpgain = (int((trap4xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap4 == "Wyvern":
					trap4enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap4xpgain = random.randint(10, 30)
				
					if trap4diff == "Uncommon":					
						trap4enemygold = (int((trap4enemygold / 100) * 120))					
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":					
						trap4enemygold = (int((trap4enemygold / 100) * 130))					
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":					
						trap4enemygold = (int((trap4enemygold / 100) * 140))					
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":				
						trap4enemygold = (int((trap4enemygold / 100) * 150))			
						trap4xpgain = (int((trap4xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap4 == "Fire Golem":
					trap4enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap4xpgain = random.randint(20, 40)

					if trap4diff == "Uncommon":	
						trap4enemygold = (int((trap4enemygold / 100) * 120))					
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":					
						trap4enemygold = (int((trap4enemygold / 100) * 130))					
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":					
						trap4enemygold = (int((trap4enemygold / 100) * 140))					
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))					
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# SAKER KEEP
				elif trap4 == "Draugr" or trap4 == "Stalker":
					trap4enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap4xpgain = random.randint(15, 35)

					if trap4diff == "Uncommon":					
						trap4enemygold = (int((trap4enemygold / 100) * 120))					
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":					
						trap4enemygold = (int((trap4enemygold / 100) * 130))					
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":					
						trap4enemygold = (int((trap4enemygold / 100) * 140))					
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":					
						trap4enemygold = (int((trap4enemygold / 100) * 150))			
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# SAKER KEEP
				elif trap4 == "Souleater":
					trap4enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap4xpgain = random.randint(20, 40)
				
					if trap4diff == "Uncommon":					
						trap4enemygold = (int((trap4enemygold / 100) * 120))					
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":					
						trap4enemygold = (int((trap4enemygold / 100) * 130))					
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":					
						trap4enemygold = (int((trap4enemygold / 100) * 140))					
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":				
						trap4enemygold = (int((trap4enemygold / 100) * 150))				
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# SAKER KEEP
				elif trap4 == "The Corrupted":
					trap4enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap4xpgain = random.randint(30, 50)
				
					if trap4diff == "Uncommon":				
						trap4enemygold = (int((trap4enemygold / 100) * 120))					
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":					
						trap4enemygold = (int((trap4enemygold / 100) * 130))					
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":					
						trap4enemygold = (int((trap4enemygold / 100) * 140))					
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":					
						trap4enemygold = (int((trap4enemygold / 100) * 150))					
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# THE FOREST
				elif trap4 == "Wolf" or trap4 == "Goblin":
					trap4enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap4xpgain = random.randint(25, 45)

					if trap4diff == "Uncommon":					
						trap4enemygold = (int((trap4enemygold / 100) * 120))					
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":					
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":					
						trap4enemygold = (int((trap4enemygold / 100) * 150))					
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# THE FOREST
				elif trap4 == "Zombie":				
					trap4enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap4xpgain = random.randint(30, 50)

					if trap4diff == "Uncommon":				
						trap4enemygold = (int((trap4enemygold / 100) * 120))					
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":				
						trap4enemygold = (int((trap4enemygold / 100) * 130))					
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":					
						trap4enemygold = (int((trap4enemygold / 100) * 140))					
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":				
						trap4enemygold = (int((trap4enemygold / 100) * 150))					
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# THE FOREST
				elif trap4 == "Phantasm":
					trap4enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap4xpgain = random.randint(40, 60)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap4 == "Elder Dragon" or trap4 == "Hades":
					trap4enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap4xpgain = random.randint(35, 55)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					if trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap4 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap4enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap4xpgain = random.randint(40, 60)

					if trap4diff == "Uncommon":
						
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap4 == "The Accursed" :
					trap4enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap4xpgain = random.randint(50, 70)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap4 == "Ettin" or trap4 == "Dormammu":
					trap4enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap4xpgain = random.randint(45, 65)
				
					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap4 == "Harpy":
					trap4enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap4xpgain = random.randint(50, 70)
				
					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap4 == "The Nameless King":
					trap4enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap4xpgain = random.randint(60, 80)
				
					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# ZULANTHU
				elif trap4 == "Deathclaw" or trap4 == "Saurian":
					trap4enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap4xpgain = random.randint(55, 75)
				
					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# ZULANTHU
				elif trap4 == "Largos":
					trap4enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap4xpgain = random.randint(60, 80)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# ZULANTHU
				elif trap4 == "The Venomous":
					trap4enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap4xpgain = random.randint(70, 90)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# LOST CITY
				elif trap4 == "Skeleton" or trap4 == "Lizardmen":
					trap4enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap4xpgain = random.randint(65, 85)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# LOST CITY
				elif trap4 == "Giant":
					trap4enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap4xpgain = random.randint(70, 90)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# LOST CITY
				elif trap4 == "Death Knight": 
					trap4enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap4xpgain = random.randint(80, 100)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# DRENHEIM
				elif trap4 == "Ice Wolf" or trap4 == "Frost Goblin":
					trap4enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap4xpgain = random.randint(75, 95)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# DRENHEIM
				elif trap4 == "Frost Orc":
					trap4enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap4xpgain = random.randint(80, 100)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))

				# DRENHEIM
				elif trap4 == "Frost Dragon":
					trap4enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap4xpgain = random.randint(90, 110)

					if trap4diff == "Uncommon":
						trap4enemygold = (int((trap4enemygold / 100) * 120))
						trap4xpgain = (int((trap4xpgain / 100) * 120))

					elif trap4diff == "Rare":
						trap4enemygold = (int((trap4enemygold / 100) * 130))
						trap4xpgain = (int((trap4xpgain / 100) * 130))

					elif trap4diff == "Legendary":
						trap4enemygold = (int((trap4enemygold / 100) * 140))
						trap4xpgain = (int((trap4xpgain / 100) * 140))

					elif trap4diff == "Mythical":
						trap4enemygold = (int((trap4enemygold / 100) * 150))
						trap4xpgain = (int((trap4xpgain / 100) * 150))





					
				# GOLDEN TEMPLE
				if trap5 == "Rachi" or trap5 == "Debin" or trap5 == "Oofer":				
					trap5enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap5xpgain = random.randint(5, 25)
				
					if trap5diff == "Uncommon":									
						trap5enemygold = (int((trap5enemygold / 100) * 120))					
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					if trap5diff == "Rare":					
		
						trap5enemygold = (int((trap5enemygold / 100) * 130))					
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					if trap5diff == "Legendary":					
						
						trap5enemygold = (int((trap5enemygold / 100) * 140))					
						trap5xpgain = (int((trap5xpgain / 100) * 140))	

					if trap5diff == "Mythical":					
					
						trap5enemygold = (int((trap5enemygold / 100) * 150))					
						trap5xpgain = (int((trap5xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap5 == "Wyvern":
					trap5enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap5xpgain = random.randint(10, 30)
				
					if trap5diff == "Uncommon":					
						trap5enemygold = (int((trap5enemygold / 100) * 120))					
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":					
						trap5enemygold = (int((trap5enemygold / 100) * 130))					
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":					
						trap5enemygold = (int((trap5enemygold / 100) * 140))					
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":				
						trap5enemygold = (int((trap5enemygold / 100) * 150))			
						trap5xpgain = (int((trap5xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap5 == "Fire Golem":
					trap5enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap5xpgain = random.randint(20, 40)

					if trap5diff == "Uncommon":	
						trap5enemygold = (int((trap5enemygold / 100) * 120))					
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":					
						trap5enemygold = (int((trap5enemygold / 100) * 130))					
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":					
						trap5enemygold = (int((trap5enemygold / 100) * 140))					
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))					
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# SAKER KEEP
				elif trap5 == "Draugr" or trap5 == "Stalker":
					trap5enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap5xpgain = random.randint(15, 35)

					if trap5diff == "Uncommon":					
						trap5enemygold = (int((trap5enemygold / 100) * 120))					
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":					
						trap5enemygold = (int((trap5enemygold / 100) * 130))					
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":					
						trap5enemygold = (int((trap5enemygold / 100) * 140))					
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":					
						trap5enemygold = (int((trap5enemygold / 100) * 150))			
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# SAKER KEEP
				elif trap5 == "Souleater":
					trap5enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap5xpgain = random.randint(20, 40)
				
					if trap5diff == "Uncommon":					
						trap5enemygold = (int((trap5enemygold / 100) * 120))					
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":					
						trap5enemygold = (int((trap5enemygold / 100) * 130))					
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":					
						trap5enemygold = (int((trap5enemygold / 100) * 140))					
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":				
						trap5enemygold = (int((trap5enemygold / 100) * 150))				
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# SAKER KEEP
				elif trap5 == "The Corrupted":
					trap5enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap5xpgain = random.randint(30, 50)
				
					if trap5diff == "Uncommon":				
						trap5enemygold = (int((trap5enemygold / 100) * 120))					
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":					
						trap5enemygold = (int((trap5enemygold / 100) * 130))					
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":					
						trap5enemygold = (int((trap5enemygold / 100) * 140))					
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":					
						trap5enemygold = (int((trap5enemygold / 100) * 150))					
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# THE FOREST
				elif trap5 == "Wolf" or trap5 == "Goblin":
					trap5enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap5xpgain = random.randint(25, 45)

					if trap5diff == "Uncommon":					
						trap5enemygold = (int((trap5enemygold / 100) * 120))					
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":					
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":					
						trap5enemygold = (int((trap5enemygold / 100) * 150))					
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# THE FOREST
				elif trap5 == "Zombie":				
					trap5enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap5xpgain = random.randint(30, 50)

					if trap5diff == "Uncommon":				
						trap5enemygold = (int((trap5enemygold / 100) * 120))					
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":				
						trap5enemygold = (int((trap5enemygold / 100) * 130))					
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":					
						trap5enemygold = (int((trap5enemygold / 100) * 140))					
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":				
						trap5enemygold = (int((trap5enemygold / 100) * 150))					
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# THE FOREST
				elif trap5 == "Phantasm":
					trap5enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap5xpgain = random.randint(40, 60)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap5 == "Elder Dragon" or trap5 == "Hades":
					trap5enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap5xpgain = random.randint(35, 55)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					if trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap5 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap5enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap5xpgain = random.randint(40, 60)

					if trap5diff == "Uncommon":
						
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap5 == "The Accursed" :
					trap5enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap5xpgain = random.randint(50, 70)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap5 == "Ettin" or trap5 == "Dormammu":
					trap5enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap5xpgain = random.randint(45, 65)
				
					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap5 == "Harpy":
					trap5enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap5xpgain = random.randint(50, 70)
				
					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap5 == "The Nameless King":
					trap5enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap5xpgain = random.randint(60, 80)
				
					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# ZULANTHU
				elif trap5 == "Deathclaw" or trap5 == "Saurian":
					trap5enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap5xpgain = random.randint(55, 75)
				
					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# ZULANTHU
				elif trap5 == "Largos":
					trap5enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap5xpgain = random.randint(60, 80)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# ZULANTHU
				elif trap5 == "The Venomous":
					trap5enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap5xpgain = random.randint(70, 90)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# LOST CITY
				elif trap5 == "Skeleton" or trap5 == "Lizardmen":
					trap5enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap5xpgain = random.randint(65, 85)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# LOST CITY
				elif trap5 == "Giant":
					trap5enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap5xpgain = random.randint(70, 90)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# LOST CITY
				elif trap5 == "Death Knight": 
					trap5enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap5xpgain = random.randint(80, 100)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# DRENHEIM
				elif trap5 == "Ice Wolf" or trap5 == "Frost Goblin":
					trap5enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap5xpgain = random.randint(75, 95)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# DRENHEIM
				elif trap5 == "Frost Orc":
					trap5enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap5xpgain = random.randint(80, 100)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))

				# DRENHEIM
				elif trap5 == "Frost Dragon":
					trap5enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap5xpgain = random.randint(90, 110)

					if trap5diff == "Uncommon":
						trap5enemygold = (int((trap5enemygold / 100) * 120))
						trap5xpgain = (int((trap5xpgain / 100) * 120))

					elif trap5diff == "Rare":
						trap5enemygold = (int((trap5enemygold / 100) * 130))
						trap5xpgain = (int((trap5xpgain / 100) * 130))

					elif trap5diff == "Legendary":
						trap5enemygold = (int((trap5enemygold / 100) * 140))
						trap5xpgain = (int((trap5xpgain / 100) * 140))

					elif trap5diff == "Mythical":
						trap5enemygold = (int((trap5enemygold / 100) * 150))
						trap5xpgain = (int((trap5xpgain / 100) * 150))



					
				# GOLDEN TEMPLE
				if trap6 == "Rachi" or trap6 == "Debin" or trap6 == "Oofer":				
					trap6enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap6xpgain = random.randint(5, 25)
				
					if trap6diff == "Uncommon":									
						trap6enemygold = (int((trap6enemygold / 100) * 120))					
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					if trap6diff == "Rare":					
		
						trap6enemygold = (int((trap6enemygold / 100) * 130))					
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					if trap6diff == "Legendary":					
						
						trap6enemygold = (int((trap6enemygold / 100) * 140))					
						trap6xpgain = (int((trap6xpgain / 100) * 140))	

					if trap6diff == "Mythical":					
					
						trap6enemygold = (int((trap6enemygold / 100) * 150))					
						trap6xpgain = (int((trap6xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap6 == "Wyvern":
					trap6enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap6xpgain = random.randint(10, 30)
				
					if trap6diff == "Uncommon":					
						trap6enemygold = (int((trap6enemygold / 100) * 120))					
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":					
						trap6enemygold = (int((trap6enemygold / 100) * 130))					
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":					
						trap6enemygold = (int((trap6enemygold / 100) * 140))					
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":				
						trap6enemygold = (int((trap6enemygold / 100) * 150))			
						trap6xpgain = (int((trap6xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap6 == "Fire Golem":
					trap6enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap6xpgain = random.randint(20, 40)

					if trap6diff == "Uncommon":	
						trap6enemygold = (int((trap6enemygold / 100) * 120))					
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":					
						trap6enemygold = (int((trap6enemygold / 100) * 130))					
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":					
						trap6enemygold = (int((trap6enemygold / 100) * 140))					
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))					
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# SAKER KEEP
				elif trap6 == "Draugr" or trap6 == "Stalker":
					trap6enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap6xpgain = random.randint(15, 35)

					if trap6diff == "Uncommon":					
						trap6enemygold = (int((trap6enemygold / 100) * 120))					
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":					
						trap6enemygold = (int((trap6enemygold / 100) * 130))					
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":					
						trap6enemygold = (int((trap6enemygold / 100) * 140))					
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":					
						trap6enemygold = (int((trap6enemygold / 100) * 150))			
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# SAKER KEEP
				elif trap6 == "Souleater":
					trap6enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap6xpgain = random.randint(20, 40)
				
					if trap6diff == "Uncommon":					
						trap6enemygold = (int((trap6enemygold / 100) * 120))					
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":					
						trap6enemygold = (int((trap6enemygold / 100) * 130))					
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":					
						trap6enemygold = (int((trap6enemygold / 100) * 140))					
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":				
						trap6enemygold = (int((trap6enemygold / 100) * 150))				
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# SAKER KEEP
				elif trap6 == "The Corrupted":
					trap6enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap6xpgain = random.randint(30, 50)
				
					if trap6diff == "Uncommon":				
						trap6enemygold = (int((trap6enemygold / 100) * 120))					
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":					
						trap6enemygold = (int((trap6enemygold / 100) * 130))					
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":					
						trap6enemygold = (int((trap6enemygold / 100) * 140))					
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":					
						trap6enemygold = (int((trap6enemygold / 100) * 150))					
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# THE FOREST
				elif trap6 == "Wolf" or trap6 == "Goblin":
					trap6enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap6xpgain = random.randint(25, 45)

					if trap6diff == "Uncommon":					
						trap6enemygold = (int((trap6enemygold / 100) * 120))					
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":					
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":					
						trap6enemygold = (int((trap6enemygold / 100) * 150))					
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# THE FOREST
				elif trap6 == "Zombie":				
					trap6enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap6xpgain = random.randint(30, 50)

					if trap6diff == "Uncommon":				
						trap6enemygold = (int((trap6enemygold / 100) * 120))					
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":				
						trap6enemygold = (int((trap6enemygold / 100) * 130))					
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":					
						trap6enemygold = (int((trap6enemygold / 100) * 140))					
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":				
						trap6enemygold = (int((trap6enemygold / 100) * 150))					
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# THE FOREST
				elif trap6 == "Phantasm":
					trap6enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap6xpgain = random.randint(40, 60)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap6 == "Elder Dragon" or trap6 == "Hades":
					trap6enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap6xpgain = random.randint(35, 55)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					if trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap6 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap6enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap6xpgain = random.randint(40, 60)

					if trap6diff == "Uncommon":
						
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap6 == "The Accursed" :
					trap6enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap6xpgain = random.randint(50, 70)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap6 == "Ettin" or trap6 == "Dormammu":
					trap6enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap6xpgain = random.randint(45, 65)
				
					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap6 == "Harpy":
					trap6enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap6xpgain = random.randint(50, 70)
				
					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap6 == "The Nameless King":
					trap6enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap6xpgain = random.randint(60, 80)
				
					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# ZULANTHU
				elif trap6 == "Deathclaw" or trap6 == "Saurian":
					trap6enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap6xpgain = random.randint(55, 75)
				
					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# ZULANTHU
				elif trap6 == "Largos":
					trap6enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap6xpgain = random.randint(60, 80)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# ZULANTHU
				elif trap6 == "The Venomous":
					trap6enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap6xpgain = random.randint(70, 90)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# LOST CITY
				elif trap6 == "Skeleton" or trap6 == "Lizardmen":
					trap6enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap6xpgain = random.randint(65, 85)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# LOST CITY
				elif trap6 == "Giant":
					trap6enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap6xpgain = random.randint(70, 90)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# LOST CITY
				elif trap6 == "Death Knight": 
					trap6enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap6xpgain = random.randint(80, 100)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# DRENHEIM
				elif trap6 == "Ice Wolf" or trap6 == "Frost Goblin":
					trap6enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap6xpgain = random.randint(75, 95)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# DRENHEIM
				elif trap6 == "Frost Orc":
					trap6enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap6xpgain = random.randint(80, 100)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))

				# DRENHEIM
				elif trap6 == "Frost Dragon":
					trap6enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap6xpgain = random.randint(90, 110)

					if trap6diff == "Uncommon":
						trap6enemygold = (int((trap6enemygold / 100) * 120))
						trap6xpgain = (int((trap6xpgain / 100) * 120))

					elif trap6diff == "Rare":
						trap6enemygold = (int((trap6enemygold / 100) * 130))
						trap6xpgain = (int((trap6xpgain / 100) * 130))

					elif trap6diff == "Legendary":
						trap6enemygold = (int((trap6enemygold / 100) * 140))
						trap6xpgain = (int((trap6xpgain / 100) * 140))

					elif trap6diff == "Mythical":
						trap6enemygold = (int((trap6enemygold / 100) * 150))
						trap6xpgain = (int((trap6xpgain / 100) * 150))


					
				# GOLDEN TEMPLE
				if trap7 == "Rachi" or trap7 == "Debin" or trap7 == "Oofer":				
					trap7enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap7xpgain = random.randint(5, 25)
				
					if trap7diff == "Uncommon":									
						trap7enemygold = (int((trap7enemygold / 100) * 120))					
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					if trap7diff == "Rare":					
		
						trap7enemygold = (int((trap7enemygold / 100) * 130))					
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					if trap7diff == "Legendary":					
						
						trap7enemygold = (int((trap7enemygold / 100) * 140))					
						trap7xpgain = (int((trap7xpgain / 100) * 140))	

					if trap7diff == "Mythical":					
					
						trap7enemygold = (int((trap7enemygold / 100) * 150))					
						trap7xpgain = (int((trap7xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap7 == "Wyvern":
					trap7enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap7xpgain = random.randint(10, 30)
				
					if trap7diff == "Uncommon":					
						trap7enemygold = (int((trap7enemygold / 100) * 120))					
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":					
						trap7enemygold = (int((trap7enemygold / 100) * 130))					
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":					
						trap7enemygold = (int((trap7enemygold / 100) * 140))					
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":				
						trap7enemygold = (int((trap7enemygold / 100) * 150))			
						trap7xpgain = (int((trap7xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap7 == "Fire Golem":
					trap7enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap7xpgain = random.randint(20, 40)

					if trap7diff == "Uncommon":	
						trap7enemygold = (int((trap7enemygold / 100) * 120))					
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":					
						trap7enemygold = (int((trap7enemygold / 100) * 130))					
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":					
						trap7enemygold = (int((trap7enemygold / 100) * 140))					
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))					
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# SAKER KEEP
				elif trap7 == "Draugr" or trap7 == "Stalker":
					trap7enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap7xpgain = random.randint(15, 35)

					if trap7diff == "Uncommon":					
						trap7enemygold = (int((trap7enemygold / 100) * 120))					
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":					
						trap7enemygold = (int((trap7enemygold / 100) * 130))					
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":					
						trap7enemygold = (int((trap7enemygold / 100) * 140))					
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":					
						trap7enemygold = (int((trap7enemygold / 100) * 150))			
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# SAKER KEEP
				elif trap7 == "Souleater":
					trap7enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap7xpgain = random.randint(20, 40)
				
					if trap7diff == "Uncommon":					
						trap7enemygold = (int((trap7enemygold / 100) * 120))					
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":					
						trap7enemygold = (int((trap7enemygold / 100) * 130))					
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":					
						trap7enemygold = (int((trap7enemygold / 100) * 140))					
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":				
						trap7enemygold = (int((trap7enemygold / 100) * 150))				
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# SAKER KEEP
				elif trap7 == "The Corrupted":
					trap7enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap7xpgain = random.randint(30, 50)
				
					if trap7diff == "Uncommon":				
						trap7enemygold = (int((trap7enemygold / 100) * 120))					
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":					
						trap7enemygold = (int((trap7enemygold / 100) * 130))					
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":					
						trap7enemygold = (int((trap7enemygold / 100) * 140))					
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":					
						trap7enemygold = (int((trap7enemygold / 100) * 150))					
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# THE FOREST
				elif trap7 == "Wolf" or trap7 == "Goblin":
					trap7enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap7xpgain = random.randint(25, 45)

					if trap7diff == "Uncommon":					
						trap7enemygold = (int((trap7enemygold / 100) * 120))					
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":					
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":					
						trap7enemygold = (int((trap7enemygold / 100) * 150))					
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# THE FOREST
				elif trap7 == "Zombie":				
					trap7enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap7xpgain = random.randint(30, 50)

					if trap7diff == "Uncommon":				
						trap7enemygold = (int((trap7enemygold / 100) * 120))					
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":				
						trap7enemygold = (int((trap7enemygold / 100) * 130))					
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":					
						trap7enemygold = (int((trap7enemygold / 100) * 140))					
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":				
						trap7enemygold = (int((trap7enemygold / 100) * 150))					
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# THE FOREST
				elif trap7 == "Phantasm":
					trap7enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap7xpgain = random.randint(40, 60)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap7 == "Elder Dragon" or trap7 == "Hades":
					trap7enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap7xpgain = random.randint(35, 55)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					if trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap7 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap7enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap7xpgain = random.randint(40, 60)

					if trap7diff == "Uncommon":
						
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap7 == "The Accursed" :
					trap7enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap7xpgain = random.randint(50, 70)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap7 == "Ettin" or trap7 == "Dormammu":
					trap7enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap7xpgain = random.randint(45, 65)
				
					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap7 == "Harpy":
					trap7enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap7xpgain = random.randint(50, 70)
				
					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap7 == "The Nameless King":
					trap7enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap7xpgain = random.randint(60, 80)
				
					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# ZULANTHU
				elif trap7 == "Deathclaw" or trap7 == "Saurian":
					trap7enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap7xpgain = random.randint(55, 75)
				
					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# ZULANTHU
				elif trap7 == "Largos":
					trap7enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap7xpgain = random.randint(60, 80)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# ZULANTHU
				elif trap7 == "The Venomous":
					trap7enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap7xpgain = random.randint(70, 90)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# LOST CITY
				elif trap7 == "Skeleton" or trap7 == "Lizardmen":
					trap7enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap7xpgain = random.randint(65, 85)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# LOST CITY
				elif trap7 == "Giant":
					trap7enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap7xpgain = random.randint(70, 90)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# LOST CITY
				elif trap7 == "Death Knight": 
					trap7enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap7xpgain = random.randint(80, 100)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# DRENHEIM
				elif trap7 == "Ice Wolf" or trap7 == "Frost Goblin":
					trap7enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap7xpgain = random.randint(75, 95)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# DRENHEIM
				elif trap7 == "Frost Orc":
					trap7enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap7xpgain = random.randint(80, 100)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))

				# DRENHEIM
				elif trap7 == "Frost Dragon":
					trap7enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap7xpgain = random.randint(90, 110)

					if trap7diff == "Uncommon":
						trap7enemygold = (int((trap7enemygold / 100) * 120))
						trap7xpgain = (int((trap7xpgain / 100) * 120))

					elif trap7diff == "Rare":
						trap7enemygold = (int((trap7enemygold / 100) * 130))
						trap7xpgain = (int((trap7xpgain / 100) * 130))

					elif trap7diff == "Legendary":
						trap7enemygold = (int((trap7enemygold / 100) * 140))
						trap7xpgain = (int((trap7xpgain / 100) * 140))

					elif trap7diff == "Mythical":
						trap7enemygold = (int((trap7enemygold / 100) * 150))
						trap7xpgain = (int((trap7xpgain / 100) * 150))


					
				# GOLDEN TEMPLE
				if trap8 == "Rachi" or trap8 == "Debin" or trap8 == "Oofer":				
					trap8enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap8xpgain = random.randint(5, 25)
				
					if trap8diff == "Uncommon":									
						trap8enemygold = (int((trap8enemygold / 100) * 120))					
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					if trap8diff == "Rare":					
		
						trap8enemygold = (int((trap8enemygold / 100) * 130))					
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					if trap8diff == "Legendary":					
						
						trap8enemygold = (int((trap8enemygold / 100) * 140))					
						trap8xpgain = (int((trap8xpgain / 100) * 140))	

					if trap8diff == "Mythical":					
					
						trap8enemygold = (int((trap8enemygold / 100) * 150))					
						trap8xpgain = (int((trap8xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap8 == "Wyvern":
					trap8enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap8xpgain = random.randint(10, 30)
				
					if trap8diff == "Uncommon":					
						trap8enemygold = (int((trap8enemygold / 100) * 120))					
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":					
						trap8enemygold = (int((trap8enemygold / 100) * 130))					
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":					
						trap8enemygold = (int((trap8enemygold / 100) * 140))					
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":				
						trap8enemygold = (int((trap8enemygold / 100) * 150))			
						trap8xpgain = (int((trap8xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap8 == "Fire Golem":
					trap8enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap8xpgain = random.randint(20, 40)

					if trap8diff == "Uncommon":	
						trap8enemygold = (int((trap8enemygold / 100) * 120))					
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":					
						trap8enemygold = (int((trap8enemygold / 100) * 130))					
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":					
						trap8enemygold = (int((trap8enemygold / 100) * 140))					
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))					
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# SAKER KEEP
				elif trap8 == "Draugr" or trap8 == "Stalker":
					trap8enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap8xpgain = random.randint(15, 35)

					if trap8diff == "Uncommon":					
						trap8enemygold = (int((trap8enemygold / 100) * 120))					
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":					
						trap8enemygold = (int((trap8enemygold / 100) * 130))					
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":					
						trap8enemygold = (int((trap8enemygold / 100) * 140))					
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":					
						trap8enemygold = (int((trap8enemygold / 100) * 150))			
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# SAKER KEEP
				elif trap8 == "Souleater":
					trap8enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap8xpgain = random.randint(20, 40)
				
					if trap8diff == "Uncommon":					
						trap8enemygold = (int((trap8enemygold / 100) * 120))					
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":					
						trap8enemygold = (int((trap8enemygold / 100) * 130))					
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":					
						trap8enemygold = (int((trap8enemygold / 100) * 140))					
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":				
						trap8enemygold = (int((trap8enemygold / 100) * 150))				
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# SAKER KEEP
				elif trap8 == "The Corrupted":
					trap8enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap8xpgain = random.randint(30, 50)
				
					if trap8diff == "Uncommon":				
						trap8enemygold = (int((trap8enemygold / 100) * 120))					
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":					
						trap8enemygold = (int((trap8enemygold / 100) * 130))					
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":					
						trap8enemygold = (int((trap8enemygold / 100) * 140))					
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":					
						trap8enemygold = (int((trap8enemygold / 100) * 150))					
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# THE FOREST
				elif trap8 == "Wolf" or trap8 == "Goblin":
					trap8enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap8xpgain = random.randint(25, 45)

					if trap8diff == "Uncommon":					
						trap8enemygold = (int((trap8enemygold / 100) * 120))					
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":					
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":					
						trap8enemygold = (int((trap8enemygold / 100) * 150))					
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# THE FOREST
				elif trap8 == "Zombie":				
					trap8enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap8xpgain = random.randint(30, 50)

					if trap8diff == "Uncommon":				
						trap8enemygold = (int((trap8enemygold / 100) * 120))					
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":				
						trap8enemygold = (int((trap8enemygold / 100) * 130))					
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":					
						trap8enemygold = (int((trap8enemygold / 100) * 140))					
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":				
						trap8enemygold = (int((trap8enemygold / 100) * 150))					
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# THE FOREST
				elif trap8 == "Phantasm":
					trap8enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap8xpgain = random.randint(40, 60)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap8 == "Elder Dragon" or trap8 == "Hades":
					trap8enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap8xpgain = random.randint(35, 55)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					if trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap8 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap8enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap8xpgain = random.randint(40, 60)

					if trap8diff == "Uncommon":
						
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap8 == "The Accursed" :
					trap8enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap8xpgain = random.randint(50, 70)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap8 == "Ettin" or trap8 == "Dormammu":
					trap8enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap8xpgain = random.randint(45, 65)
				
					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap8 == "Harpy":
					trap8enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap8xpgain = random.randint(50, 70)
				
					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap8 == "The Nameless King":
					trap8enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap8xpgain = random.randint(60, 80)
				
					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# ZULANTHU
				elif trap8 == "Deathclaw" or trap8 == "Saurian":
					trap8enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap8xpgain = random.randint(55, 75)
				
					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# ZULANTHU
				elif trap8 == "Largos":
					trap8enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap8xpgain = random.randint(60, 80)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# ZULANTHU
				elif trap8 == "The Venomous":
					trap8enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap8xpgain = random.randint(70, 90)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# LOST CITY
				elif trap8 == "Skeleton" or trap8 == "Lizardmen":
					trap8enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap8xpgain = random.randint(65, 85)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# LOST CITY
				elif trap8 == "Giant":
					trap8enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap8xpgain = random.randint(70, 90)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# LOST CITY
				elif trap8 == "Death Knight": 
					trap8enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap8xpgain = random.randint(80, 100)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# DRENHEIM
				elif trap8 == "Ice Wolf" or trap8 == "Frost Goblin":
					trap8enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap8xpgain = random.randint(75, 95)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# DRENHEIM
				elif trap8 == "Frost Orc":
					trap8enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap8xpgain = random.randint(80, 100)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))

				# DRENHEIM
				elif trap8 == "Frost Dragon":
					trap8enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap8xpgain = random.randint(90, 110)

					if trap8diff == "Uncommon":
						trap8enemygold = (int((trap8enemygold / 100) * 120))
						trap8xpgain = (int((trap8xpgain / 100) * 120))

					elif trap8diff == "Rare":
						trap8enemygold = (int((trap8enemygold / 100) * 130))
						trap8xpgain = (int((trap8xpgain / 100) * 130))

					elif trap8diff == "Legendary":
						trap8enemygold = (int((trap8enemygold / 100) * 140))
						trap8xpgain = (int((trap8xpgain / 100) * 140))

					elif trap8diff == "Mythical":
						trap8enemygold = (int((trap8enemygold / 100) * 150))
						trap8xpgain = (int((trap8xpgain / 100) * 150))


						
					
				# GOLDEN TEMPLE
				if trap9 == "Rachi" or trap9 == "Debin" or trap9 == "Oofer":				
					trap9enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap9xpgain = random.randint(5, 25)
				
					if trap9diff == "Uncommon":									
						trap9enemygold = (int((trap9enemygold / 100) * 120))					
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					if trap9diff == "Rare":					
		
						trap9enemygold = (int((trap9enemygold / 100) * 130))					
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					if trap9diff == "Legendary":					
						
						trap9enemygold = (int((trap9enemygold / 100) * 140))					
						trap9xpgain = (int((trap9xpgain / 100) * 140))	

					if trap9diff == "Mythical":					
					
						trap9enemygold = (int((trap9enemygold / 100) * 150))					
						trap9xpgain = (int((trap9xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap9 == "Wyvern":
					trap9enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap9xpgain = random.randint(10, 30)
				
					if trap9diff == "Uncommon":					
						trap9enemygold = (int((trap9enemygold / 100) * 120))					
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":					
						trap9enemygold = (int((trap9enemygold / 100) * 130))					
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":					
						trap9enemygold = (int((trap9enemygold / 100) * 140))					
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":				
						trap9enemygold = (int((trap9enemygold / 100) * 150))			
						trap9xpgain = (int((trap9xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap9 == "Fire Golem":
					trap9enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap9xpgain = random.randint(20, 40)

					if trap9diff == "Uncommon":	
						trap9enemygold = (int((trap9enemygold / 100) * 120))					
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":					
						trap9enemygold = (int((trap9enemygold / 100) * 130))					
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":					
						trap9enemygold = (int((trap9enemygold / 100) * 140))					
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))					
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# SAKER KEEP
				elif trap9 == "Draugr" or trap9 == "Stalker":
					trap9enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap9xpgain = random.randint(15, 35)

					if trap9diff == "Uncommon":					
						trap9enemygold = (int((trap9enemygold / 100) * 120))					
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":					
						trap9enemygold = (int((trap9enemygold / 100) * 130))					
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":					
						trap9enemygold = (int((trap9enemygold / 100) * 140))					
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":					
						trap9enemygold = (int((trap9enemygold / 100) * 150))			
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# SAKER KEEP
				elif trap9 == "Souleater":
					trap9enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap9xpgain = random.randint(20, 40)
				
					if trap9diff == "Uncommon":					
						trap9enemygold = (int((trap9enemygold / 100) * 120))					
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":					
						trap9enemygold = (int((trap9enemygold / 100) * 130))					
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":					
						trap9enemygold = (int((trap9enemygold / 100) * 140))					
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":				
						trap9enemygold = (int((trap9enemygold / 100) * 150))				
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# SAKER KEEP
				elif trap9 == "The Corrupted":
					trap9enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap9xpgain = random.randint(30, 50)
				
					if trap9diff == "Uncommon":				
						trap9enemygold = (int((trap9enemygold / 100) * 120))					
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":					
						trap9enemygold = (int((trap9enemygold / 100) * 130))					
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":					
						trap9enemygold = (int((trap9enemygold / 100) * 140))					
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":					
						trap9enemygold = (int((trap9enemygold / 100) * 150))					
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# THE FOREST
				elif trap9 == "Wolf" or trap9 == "Goblin":
					trap9enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap9xpgain = random.randint(25, 45)

					if trap9diff == "Uncommon":					
						trap9enemygold = (int((trap9enemygold / 100) * 120))					
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":					
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":					
						trap9enemygold = (int((trap9enemygold / 100) * 150))					
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# THE FOREST
				elif trap9 == "Zombie":				
					trap9enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap9xpgain = random.randint(30, 50)

					if trap9diff == "Uncommon":				
						trap9enemygold = (int((trap9enemygold / 100) * 120))					
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":				
						trap9enemygold = (int((trap9enemygold / 100) * 130))					
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":					
						trap9enemygold = (int((trap9enemygold / 100) * 140))					
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":				
						trap9enemygold = (int((trap9enemygold / 100) * 150))					
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# THE FOREST
				elif trap9 == "Phantasm":
					trap9enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap9xpgain = random.randint(40, 60)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap9 == "Elder Dragon" or trap9 == "Hades":
					trap9enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap9xpgain = random.randint(35, 55)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					if trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap9 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap9enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap9xpgain = random.randint(40, 60)

					if trap9diff == "Uncommon":
						
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap9 == "The Accursed" :
					trap9enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap9xpgain = random.randint(50, 70)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap9 == "Ettin" or trap9 == "Dormammu":
					trap9enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap9xpgain = random.randint(45, 65)
				
					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap9 == "Harpy":
					trap9enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap9xpgain = random.randint(50, 70)
				
					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap9 == "The Nameless King":
					trap9enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap9xpgain = random.randint(60, 80)
				
					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# ZULANTHU
				elif trap9 == "Deathclaw" or trap9 == "Saurian":
					trap9enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap9xpgain = random.randint(55, 75)
				
					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# ZULANTHU
				elif trap9 == "Largos":
					trap9enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap9xpgain = random.randint(60, 80)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# ZULANTHU
				elif trap9 == "The Venomous":
					trap9enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap9xpgain = random.randint(70, 90)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# LOST CITY
				elif trap9 == "Skeleton" or trap9 == "Lizardmen":
					trap9enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap9xpgain = random.randint(65, 85)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# LOST CITY
				elif trap9 == "Giant":
					trap9enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap9xpgain = random.randint(70, 90)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# LOST CITY
				elif trap9 == "Death Knight": 
					trap9enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap9xpgain = random.randint(80, 100)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# DRENHEIM
				elif trap9 == "Ice Wolf" or trap9 == "Frost Goblin":
					trap9enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap9xpgain = random.randint(75, 95)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# DRENHEIM
				elif trap9 == "Frost Orc":
					trap9enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap9xpgain = random.randint(80, 100)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

				# DRENHEIM
				elif trap9 == "Frost Dragon":
					trap9enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap9xpgain = random.randint(90, 110)

					if trap9diff == "Uncommon":
						trap9enemygold = (int((trap9enemygold / 100) * 120))
						trap9xpgain = (int((trap9xpgain / 100) * 120))

					elif trap9diff == "Rare":
						trap9enemygold = (int((trap9enemygold / 100) * 130))
						trap9xpgain = (int((trap9xpgain / 100) * 130))

					elif trap9diff == "Legendary":
						trap9enemygold = (int((trap9enemygold / 100) * 140))
						trap9xpgain = (int((trap9xpgain / 100) * 140))

					elif trap9diff == "Mythical":
						trap9enemygold = (int((trap9enemygold / 100) * 150))
						trap9xpgain = (int((trap9xpgain / 100) * 150))

						
						
					
				# GOLDEN TEMPLE
				if trap10 == "Rachi" or trap10 == "Debin" or trap10 == "Oofer":				
					trap10enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap10xpgain = random.randint(5, 25)
				
					if trap10diff == "Uncommon":									
						trap10enemygold = (int((trap10enemygold / 100) * 120))					
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					if trap10diff == "Rare":					
		
						trap10enemygold = (int((trap10enemygold / 100) * 130))					
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					if trap10diff == "Legendary":					
						
						trap10enemygold = (int((trap10enemygold / 100) * 140))					
						trap10xpgain = (int((trap10xpgain / 100) * 140))	

					if trap10diff == "Mythical":					
					
						trap10enemygold = (int((trap10enemygold / 100) * 150))					
						trap10xpgain = (int((trap10xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap10 == "Wyvern":
					trap10enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap10xpgain = random.randint(10, 30)
				
					if trap10diff == "Uncommon":					
						trap10enemygold = (int((trap10enemygold / 100) * 120))					
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":					
						trap10enemygold = (int((trap10enemygold / 100) * 130))					
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":					
						trap10enemygold = (int((trap10enemygold / 100) * 140))					
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":				
						trap10enemygold = (int((trap10enemygold / 100) * 150))			
						trap10xpgain = (int((trap10xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap10 == "Fire Golem":
					trap10enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap10xpgain = random.randint(20, 40)

					if trap10diff == "Uncommon":	
						trap10enemygold = (int((trap10enemygold / 100) * 120))					
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":					
						trap10enemygold = (int((trap10enemygold / 100) * 130))					
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":					
						trap10enemygold = (int((trap10enemygold / 100) * 140))					
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))					
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# SAKER KEEP
				elif trap10 == "Draugr" or trap10 == "Stalker":
					trap10enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap10xpgain = random.randint(15, 35)

					if trap10diff == "Uncommon":					
						trap10enemygold = (int((trap10enemygold / 100) * 120))					
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":					
						trap10enemygold = (int((trap10enemygold / 100) * 130))					
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":					
						trap10enemygold = (int((trap10enemygold / 100) * 140))					
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":					
						trap10enemygold = (int((trap10enemygold / 100) * 150))			
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# SAKER KEEP
				elif trap10 == "Souleater":
					trap10enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap10xpgain = random.randint(20, 40)
				
					if trap10diff == "Uncommon":					
						trap10enemygold = (int((trap10enemygold / 100) * 120))					
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":					
						trap10enemygold = (int((trap10enemygold / 100) * 130))					
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":					
						trap10enemygold = (int((trap10enemygold / 100) * 140))					
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":				
						trap10enemygold = (int((trap10enemygold / 100) * 150))				
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# SAKER KEEP
				elif trap10 == "The Corrupted":
					trap10enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap10xpgain = random.randint(30, 50)
				
					if trap10diff == "Uncommon":				
						trap10enemygold = (int((trap10enemygold / 100) * 120))					
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":					
						trap10enemygold = (int((trap10enemygold / 100) * 130))					
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":					
						trap10enemygold = (int((trap10enemygold / 100) * 140))					
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":					
						trap10enemygold = (int((trap10enemygold / 100) * 150))					
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# THE FOREST
				elif trap10 == "Wolf" or trap10 == "Goblin":
					trap10enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap10xpgain = random.randint(25, 45)

					if trap10diff == "Uncommon":					
						trap10enemygold = (int((trap10enemygold / 100) * 120))					
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":					
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":					
						trap10enemygold = (int((trap10enemygold / 100) * 150))					
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# THE FOREST
				elif trap10 == "Zombie":				
					trap10enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap10xpgain = random.randint(30, 50)

					if trap10diff == "Uncommon":				
						trap10enemygold = (int((trap10enemygold / 100) * 120))					
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":				
						trap10enemygold = (int((trap10enemygold / 100) * 130))					
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":					
						trap10enemygold = (int((trap10enemygold / 100) * 140))					
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":				
						trap10enemygold = (int((trap10enemygold / 100) * 150))					
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# THE FOREST
				elif trap10 == "Phantasm":
					trap10enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap10xpgain = random.randint(40, 60)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap10 == "Elder Dragon" or trap10 == "Hades":
					trap10enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap10xpgain = random.randint(35, 55)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					if trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap10 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap10enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap10xpgain = random.randint(40, 60)

					if trap10diff == "Uncommon":
						
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap10 == "The Accursed" :
					trap10enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap10xpgain = random.randint(50, 70)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap10 == "Ettin" or trap10 == "Dormammu":
					trap10enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap10xpgain = random.randint(45, 65)
				
					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap10 == "Harpy":
					trap10enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap10xpgain = random.randint(50, 70)
				
					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap10 == "The Nameless King":
					trap10enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap10xpgain = random.randint(60, 80)
				
					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# ZULANTHU
				elif trap10 == "Deathclaw" or trap10 == "Saurian":
					trap10enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap10xpgain = random.randint(55, 75)
				
					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# ZULANTHU
				elif trap10 == "Largos":
					trap10enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap10xpgain = random.randint(60, 80)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# ZULANTHU
				elif trap10 == "The Venomous":
					trap10enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap10xpgain = random.randint(70, 90)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# LOST CITY
				elif trap10 == "Skeleton" or trap10 == "Lizardmen":
					trap10enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap10xpgain = random.randint(65, 85)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# LOST CITY
				elif trap10 == "Giant":
					trap10enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap10xpgain = random.randint(70, 90)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# LOST CITY
				elif trap10 == "Death Knight": 
					trap10enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap10xpgain = random.randint(80, 100)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# DRENHEIM
				elif trap10 == "Ice Wolf" or trap10 == "Frost Goblin":
					trap10enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap10xpgain = random.randint(75, 95)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# DRENHEIM
				elif trap10 == "Frost Orc":
					trap10enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap10xpgain = random.randint(80, 100)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))

				# DRENHEIM
				elif trap10 == "Frost Dragon":
					trap10enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap10xpgain = random.randint(90, 110)

					if trap10diff == "Uncommon":
						trap10enemygold = (int((trap10enemygold / 100) * 120))
						trap10xpgain = (int((trap10xpgain / 100) * 120))

					elif trap10diff == "Rare":
						trap10enemygold = (int((trap10enemygold / 100) * 130))
						trap10xpgain = (int((trap10xpgain / 100) * 130))

					elif trap10diff == "Legendary":
						trap10enemygold = (int((trap10enemygold / 100) * 140))
						trap10xpgain = (int((trap10xpgain / 100) * 140))

					elif trap10diff == "Mythical":
						trap10enemygold = (int((trap10enemygold / 100) * 150))
						trap10xpgain = (int((trap10xpgain / 100) * 150))


						
					
				# GOLDEN TEMPLE
				if trap11 == "Rachi" or trap11 == "Debin" or trap11 == "Oofer":				
					trap11enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap11xpgain = random.randint(5, 25)
				
					if trap11diff == "Uncommon":									
						trap11enemygold = (int((trap11enemygold / 100) * 120))					
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					if trap11diff == "Rare":					
		
						trap11enemygold = (int((trap11enemygold / 100) * 130))					
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					if trap11diff == "Legendary":					
						
						trap11enemygold = (int((trap11enemygold / 100) * 140))					
						trap11xpgain = (int((trap11xpgain / 100) * 140))	

					if trap11diff == "Mythical":					
					
						trap11enemygold = (int((trap11enemygold / 100) * 150))					
						trap11xpgain = (int((trap11xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap11 == "Wyvern":
					trap11enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap11xpgain = random.randint(10, 30)
				
					if trap11diff == "Uncommon":					
						trap11enemygold = (int((trap11enemygold / 100) * 120))					
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":					
						trap11enemygold = (int((trap11enemygold / 100) * 130))					
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":					
						trap11enemygold = (int((trap11enemygold / 100) * 140))					
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":				
						trap11enemygold = (int((trap11enemygold / 100) * 150))			
						trap11xpgain = (int((trap11xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap11 == "Fire Golem":
					trap11enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap11xpgain = random.randint(20, 40)

					if trap11diff == "Uncommon":	
						trap11enemygold = (int((trap11enemygold / 100) * 120))					
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":					
						trap11enemygold = (int((trap11enemygold / 100) * 130))					
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":					
						trap11enemygold = (int((trap11enemygold / 100) * 140))					
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))					
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# SAKER KEEP
				elif trap11 == "Draugr" or trap11 == "Stalker":
					trap11enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap11xpgain = random.randint(15, 35)

					if trap11diff == "Uncommon":					
						trap11enemygold = (int((trap11enemygold / 100) * 120))					
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":					
						trap11enemygold = (int((trap11enemygold / 100) * 130))					
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":					
						trap11enemygold = (int((trap11enemygold / 100) * 140))					
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":					
						trap11enemygold = (int((trap11enemygold / 100) * 150))			
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# SAKER KEEP
				elif trap11 == "Souleater":
					trap11enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap11xpgain = random.randint(20, 40)
				
					if trap11diff == "Uncommon":					
						trap11enemygold = (int((trap11enemygold / 100) * 120))					
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":					
						trap11enemygold = (int((trap11enemygold / 100) * 130))					
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":					
						trap11enemygold = (int((trap11enemygold / 100) * 140))					
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":				
						trap11enemygold = (int((trap11enemygold / 100) * 150))				
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# SAKER KEEP
				elif trap11 == "The Corrupted":
					trap11enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap11xpgain = random.randint(30, 50)
				
					if trap11diff == "Uncommon":				
						trap11enemygold = (int((trap11enemygold / 100) * 120))					
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":					
						trap11enemygold = (int((trap11enemygold / 100) * 130))					
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":					
						trap11enemygold = (int((trap11enemygold / 100) * 140))					
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":					
						trap11enemygold = (int((trap11enemygold / 100) * 150))					
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# THE FOREST
				elif trap11 == "Wolf" or trap11 == "Goblin":
					trap11enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap11xpgain = random.randint(25, 45)

					if trap11diff == "Uncommon":					
						trap11enemygold = (int((trap11enemygold / 100) * 120))					
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":					
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":					
						trap11enemygold = (int((trap11enemygold / 100) * 150))					
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# THE FOREST
				elif trap11 == "Zombie":				
					trap11enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap11xpgain = random.randint(30, 50)

					if trap11diff == "Uncommon":				
						trap11enemygold = (int((trap11enemygold / 100) * 120))					
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":				
						trap11enemygold = (int((trap11enemygold / 100) * 130))					
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":					
						trap11enemygold = (int((trap11enemygold / 100) * 140))					
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":				
						trap11enemygold = (int((trap11enemygold / 100) * 150))					
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# THE FOREST
				elif trap11 == "Phantasm":
					trap11enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap11xpgain = random.randint(40, 60)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap11 == "Elder Dragon" or trap11 == "Hades":
					trap11enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap11xpgain = random.randint(35, 55)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					if trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap11 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap11enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap11xpgain = random.randint(40, 60)

					if trap11diff == "Uncommon":
						
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap11 == "The Accursed" :
					trap11enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap11xpgain = random.randint(50, 70)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap11 == "Ettin" or trap11 == "Dormammu":
					trap11enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap11xpgain = random.randint(45, 65)
				
					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap11 == "Harpy":
					trap11enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap11xpgain = random.randint(50, 70)
				
					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap11 == "The Nameless King":
					trap11enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap11xpgain = random.randint(60, 80)
				
					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# ZULANTHU
				elif trap11 == "Deathclaw" or trap11 == "Saurian":
					trap11enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap11xpgain = random.randint(55, 75)
				
					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# ZULANTHU
				elif trap11 == "Largos":
					trap11enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap11xpgain = random.randint(60, 80)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# ZULANTHU
				elif trap11 == "The Venomous":
					trap11enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap11xpgain = random.randint(70, 90)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# LOST CITY
				elif trap11 == "Skeleton" or trap11 == "Lizardmen":
					trap11enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap11xpgain = random.randint(65, 85)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# LOST CITY
				elif trap11 == "Giant":
					trap11enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap11xpgain = random.randint(70, 90)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# LOST CITY
				elif trap11 == "Death Knight": 
					trap11enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap11xpgain = random.randint(80, 100)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# DRENHEIM
				elif trap11 == "Ice Wolf" or trap11 == "Frost Goblin":
					trap11enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap11xpgain = random.randint(75, 95)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# DRENHEIM
				elif trap11 == "Frost Orc":
					trap11enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap11xpgain = random.randint(80, 100)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))

				# DRENHEIM
				elif trap11 == "Frost Dragon":
					trap11enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap11xpgain = random.randint(90, 110)

					if trap11diff == "Uncommon":
						trap11enemygold = (int((trap11enemygold / 100) * 120))
						trap11xpgain = (int((trap11xpgain / 100) * 120))

					elif trap11diff == "Rare":
						trap11enemygold = (int((trap11enemygold / 100) * 130))
						trap11xpgain = (int((trap11xpgain / 100) * 130))

					elif trap11diff == "Legendary":
						trap11enemygold = (int((trap11enemygold / 100) * 140))
						trap11xpgain = (int((trap11xpgain / 100) * 140))

					elif trap11diff == "Mythical":
						trap11enemygold = (int((trap11enemygold / 100) * 150))
						trap11xpgain = (int((trap11xpgain / 100) * 150))


						
					
				# GOLDEN TEMPLE
				if trap12 == "Rachi" or trap12 == "Debin" or trap12 == "Oofer":				
					trap12enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap12xpgain = random.randint(5, 25)
				
					if trap12diff == "Uncommon":									
						trap12enemygold = (int((trap12enemygold / 100) * 120))					
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					if trap12diff == "Rare":					
		
						trap12enemygold = (int((trap12enemygold / 100) * 130))					
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					if trap12diff == "Legendary":					
						
						trap12enemygold = (int((trap12enemygold / 100) * 140))					
						trap12xpgain = (int((trap12xpgain / 100) * 140))	

					if trap12diff == "Mythical":					
					
						trap12enemygold = (int((trap12enemygold / 100) * 150))					
						trap12xpgain = (int((trap12xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap12 == "Wyvern":
					trap12enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap12xpgain = random.randint(10, 30)
				
					if trap12diff == "Uncommon":					
						trap12enemygold = (int((trap12enemygold / 100) * 120))					
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":					
						trap12enemygold = (int((trap12enemygold / 100) * 130))					
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":					
						trap12enemygold = (int((trap12enemygold / 100) * 140))					
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":				
						trap12enemygold = (int((trap12enemygold / 100) * 150))			
						trap12xpgain = (int((trap12xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap12 == "Fire Golem":
					trap12enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap12xpgain = random.randint(20, 40)

					if trap12diff == "Uncommon":	
						trap12enemygold = (int((trap12enemygold / 100) * 120))					
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":					
						trap12enemygold = (int((trap12enemygold / 100) * 130))					
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":					
						trap12enemygold = (int((trap12enemygold / 100) * 140))					
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))					
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# SAKER KEEP
				elif trap12 == "Draugr" or trap12 == "Stalker":
					trap12enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap12xpgain = random.randint(15, 35)

					if trap12diff == "Uncommon":					
						trap12enemygold = (int((trap12enemygold / 100) * 120))					
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":					
						trap12enemygold = (int((trap12enemygold / 100) * 130))					
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":					
						trap12enemygold = (int((trap12enemygold / 100) * 140))					
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":					
						trap12enemygold = (int((trap12enemygold / 100) * 150))			
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# SAKER KEEP
				elif trap12 == "Souleater":
					trap12enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap12xpgain = random.randint(20, 40)
				
					if trap12diff == "Uncommon":					
						trap12enemygold = (int((trap12enemygold / 100) * 120))					
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":					
						trap12enemygold = (int((trap12enemygold / 100) * 130))					
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":					
						trap12enemygold = (int((trap12enemygold / 100) * 140))					
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":				
						trap12enemygold = (int((trap12enemygold / 100) * 150))				
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# SAKER KEEP
				elif trap12 == "The Corrupted":
					trap12enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap12xpgain = random.randint(30, 50)
				
					if trap12diff == "Uncommon":				
						trap12enemygold = (int((trap12enemygold / 100) * 120))					
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":					
						trap12enemygold = (int((trap12enemygold / 100) * 130))					
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":					
						trap12enemygold = (int((trap12enemygold / 100) * 140))					
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":					
						trap12enemygold = (int((trap12enemygold / 100) * 150))					
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# THE FOREST
				elif trap12 == "Wolf" or trap12 == "Goblin":
					trap12enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap12xpgain = random.randint(25, 45)

					if trap12diff == "Uncommon":					
						trap12enemygold = (int((trap12enemygold / 100) * 120))					
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":					
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":					
						trap12enemygold = (int((trap12enemygold / 100) * 150))					
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# THE FOREST
				elif trap12 == "Zombie":				
					trap12enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap12xpgain = random.randint(30, 50)

					if trap12diff == "Uncommon":				
						trap12enemygold = (int((trap12enemygold / 100) * 120))					
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":				
						trap12enemygold = (int((trap12enemygold / 100) * 130))					
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":					
						trap12enemygold = (int((trap12enemygold / 100) * 140))					
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":				
						trap12enemygold = (int((trap12enemygold / 100) * 150))					
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# THE FOREST
				elif trap12 == "Phantasm":
					trap12enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap12xpgain = random.randint(40, 60)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap12 == "Elder Dragon" or trap12 == "Hades":
					trap12enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap12xpgain = random.randint(35, 55)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					if trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap12 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap12enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap12xpgain = random.randint(40, 60)

					if trap12diff == "Uncommon":
						
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap12 == "The Accursed" :
					trap12enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap12xpgain = random.randint(50, 70)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap12 == "Ettin" or trap12 == "Dormammu":
					trap12enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap12xpgain = random.randint(45, 65)
				
					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap12 == "Harpy":
					trap12enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap12xpgain = random.randint(50, 70)
				
					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap12 == "The Nameless King":
					trap12enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap12xpgain = random.randint(60, 80)
				
					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# ZULANTHU
				elif trap12 == "Deathclaw" or trap12 == "Saurian":
					trap12enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap12xpgain = random.randint(55, 75)
				
					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# ZULANTHU
				elif trap12 == "Largos":
					trap12enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap12xpgain = random.randint(60, 80)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# ZULANTHU
				elif trap12 == "The Venomous":
					trap12enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap12xpgain = random.randint(70, 90)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# LOST CITY
				elif trap12 == "Skeleton" or trap12 == "Lizardmen":
					trap12enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap12xpgain = random.randint(65, 85)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# LOST CITY
				elif trap12 == "Giant":
					trap12enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap12xpgain = random.randint(70, 90)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# LOST CITY
				elif trap12 == "Death Knight": 
					trap12enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap12xpgain = random.randint(80, 100)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# DRENHEIM
				elif trap12 == "Ice Wolf" or trap12 == "Frost Goblin":
					trap12enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap12xpgain = random.randint(75, 95)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# DRENHEIM
				elif trap12 == "Frost Orc":
					trap12enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap12xpgain = random.randint(80, 100)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))

				# DRENHEIM
				elif trap12 == "Frost Dragon":
					trap12enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap12xpgain = random.randint(90, 110)

					if trap12diff == "Uncommon":
						trap12enemygold = (int((trap12enemygold / 100) * 120))
						trap12xpgain = (int((trap12xpgain / 100) * 120))

					elif trap12diff == "Rare":
						trap12enemygold = (int((trap12enemygold / 100) * 130))
						trap12xpgain = (int((trap12xpgain / 100) * 130))

					elif trap12diff == "Legendary":
						trap12enemygold = (int((trap12enemygold / 100) * 140))
						trap12xpgain = (int((trap12xpgain / 100) * 140))

					elif trap12diff == "Mythical":
						trap12enemygold = (int((trap12enemygold / 100) * 150))
						trap12xpgain = (int((trap12xpgain / 100) * 150))


						
					
				# GOLDEN TEMPLE
				if trap13 == "Rachi" or trap13 == "Debin" or trap13 == "Oofer":				
					trap13enemygold = random.randint(10, 30) + (effectiveguildbonus)	
					trap13xpgain = random.randint(5, 25)
				
					if trap13diff == "Uncommon":									
						trap13enemygold = (int((trap13enemygold / 100) * 120))					
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					if trap13diff == "Rare":					
		
						trap13enemygold = (int((trap13enemygold / 100) * 130))					
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					if trap13diff == "Legendary":					
						
						trap13enemygold = (int((trap13enemygold / 100) * 140))					
						trap13xpgain = (int((trap13xpgain / 100) * 140))	

					if trap13diff == "Mythical":					
					
						trap13enemygold = (int((trap13enemygold / 100) * 150))					
						trap13xpgain = (int((trap13xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif trap13 == "Wyvern":
					trap13enemygold = random.randint(15, 35) + (effectiveguildbonus)				
					trap13xpgain = random.randint(10, 30)
				
					if trap13diff == "Uncommon":					
						trap13enemygold = (int((trap13enemygold / 100) * 120))					
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":					
						trap13enemygold = (int((trap13enemygold / 100) * 130))					
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":					
						trap13enemygold = (int((trap13enemygold / 100) * 140))					
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":				
						trap13enemygold = (int((trap13enemygold / 100) * 150))			
						trap13xpgain = (int((trap13xpgain / 100) * 150))


				# GOLDEN TEMPLE
				elif  trap13 == "Fire Golem":
					trap13enemygold = random.randint(25, 50) + (effectiveguildbonus)		
					trap13xpgain = random.randint(20, 40)

					if trap13diff == "Uncommon":	
						trap13enemygold = (int((trap13enemygold / 100) * 120))					
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":					
						trap13enemygold = (int((trap13enemygold / 100) * 130))					
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":					
						trap13enemygold = (int((trap13enemygold / 100) * 140))					
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))					
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# SAKER KEEP
				elif trap13 == "Draugr" or trap13 == "Stalker":
					trap13enemygold = random.randint(20, 40) + (effectiveguildbonus)			
					trap13xpgain = random.randint(15, 35)

					if trap13diff == "Uncommon":					
						trap13enemygold = (int((trap13enemygold / 100) * 120))					
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":					
						trap13enemygold = (int((trap13enemygold / 100) * 130))					
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":					
						trap13enemygold = (int((trap13enemygold / 100) * 140))					
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":					
						trap13enemygold = (int((trap13enemygold / 100) * 150))			
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# SAKER KEEP
				elif trap13 == "Souleater":
					trap13enemygold = random.randint(25, 45) + (effectiveguildbonus)				
					trap13xpgain = random.randint(20, 40)
				
					if trap13diff == "Uncommon":					
						trap13enemygold = (int((trap13enemygold / 100) * 120))					
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":					
						trap13enemygold = (int((trap13enemygold / 100) * 130))					
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":					
						trap13enemygold = (int((trap13enemygold / 100) * 140))					
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":				
						trap13enemygold = (int((trap13enemygold / 100) * 150))				
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# SAKER KEEP
				elif trap13 == "The Corrupted":
					trap13enemygold = random.randint(35, 55) + (effectiveguildbonus)				
					trap13xpgain = random.randint(30, 50)
				
					if trap13diff == "Uncommon":				
						trap13enemygold = (int((trap13enemygold / 100) * 120))					
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":					
						trap13enemygold = (int((trap13enemygold / 100) * 130))					
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":					
						trap13enemygold = (int((trap13enemygold / 100) * 140))					
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":					
						trap13enemygold = (int((trap13enemygold / 100) * 150))					
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# THE FOREST
				elif trap13 == "Wolf" or trap13 == "Goblin":
					trap13enemygold = random.randint(30, 50) + (effectiveguildbonus)
					trap13xpgain = random.randint(25, 45)

					if trap13diff == "Uncommon":					
						trap13enemygold = (int((trap13enemygold / 100) * 120))					
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":					
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":					
						trap13enemygold = (int((trap13enemygold / 100) * 150))					
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# THE FOREST
				elif trap13 == "Zombie":				
					trap13enemygold = random.randint(35, 55) + (effectiveguildbonus)
					trap13xpgain = random.randint(30, 50)

					if trap13diff == "Uncommon":				
						trap13enemygold = (int((trap13enemygold / 100) * 120))					
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":				
						trap13enemygold = (int((trap13enemygold / 100) * 130))					
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":					
						trap13enemygold = (int((trap13enemygold / 100) * 140))					
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":				
						trap13enemygold = (int((trap13enemygold / 100) * 150))					
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# THE FOREST
				elif trap13 == "Phantasm":
					trap13enemygold = random.randint(45, 65) + (effectiveguildbonus)
					trap13xpgain = random.randint(40, 60)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap13 == "Elder Dragon" or trap13 == "Hades":
					trap13enemygold = random.randint(40, 60) + (effectiveguildbonus)
					trap13xpgain = random.randint(35, 55)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					if trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

					# EBONY MOUNTAINS
				elif trap13 == "Ebony Guardian":
					enemydmg += random.randint(40, 45)
					trap13enemygold = random.randint(45, 65) + (effectiveguildbonus)
					
					trap13xpgain = random.randint(40, 60)

					if trap13diff == "Uncommon":
						
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# EBONY MOUNTAINS
				elif trap13 == "The Accursed" :
					trap13enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap13xpgain = random.randint(50, 70)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap13 == "Ettin" or trap13 == "Dormammu":
					trap13enemygold = random.randint(50, 70) + (effectiveguildbonus)
					trap13xpgain = random.randint(45, 65)
				
					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap13 == "Harpy":
					trap13enemygold = random.randint(55, 75) + (effectiveguildbonus)
					trap13xpgain = random.randint(50, 70)
				
					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# TOWNSHIP OF ARKINA
				elif trap13 == "The Nameless King":
					trap13enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap13xpgain = random.randint(60, 80)
				
					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# ZULANTHU
				elif trap13 == "Deathclaw" or trap13 == "Saurian":
					trap13enemygold = random.randint(60, 80) + (effectiveguildbonus)
					trap13xpgain = random.randint(55, 75)
				
					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# ZULANTHU
				elif trap13 == "Largos":
					trap13enemygold = random.randint(65, 85) + (effectiveguildbonus)
					trap13xpgain = random.randint(60, 80)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# ZULANTHU
				elif trap13 == "The Venomous":
					trap13enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap13xpgain = random.randint(70, 90)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# LOST CITY
				elif trap13 == "Skeleton" or trap13 == "Lizardmen":
					trap13enemygold = random.randint(70, 90) + (effectiveguildbonus)
					trap13xpgain = random.randint(65, 85)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# LOST CITY
				elif trap13 == "Giant":
					trap13enemygold = random.randint(75, 95) + (effectiveguildbonus)
					trap13xpgain = random.randint(70, 90)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# LOST CITY
				elif trap13 == "Death Knight": 
					trap13enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap13xpgain = random.randint(80, 100)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# DRENHEIM
				elif trap13 == "Ice Wolf" or trap13 == "Frost Goblin":
					trap13enemygold = random.randint(80, 100) + (effectiveguildbonus)
					trap13xpgain = random.randint(75, 95)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# DRENHEIM
				elif trap13 == "Frost Orc":
					trap13enemygold = random.randint(85, 105) + (effectiveguildbonus)
					trap13xpgain = random.randint(80, 100)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))

				# DRENHEIM
				elif trap13 == "Frost Dragon":
					trap13enemygold = random.randint(95, 115) + (effectiveguildbonus)
					trap13xpgain = random.randint(90, 110)

					if trap13diff == "Uncommon":
						trap13enemygold = (int((trap13enemygold / 100) * 120))
						trap13xpgain = (int((trap13xpgain / 100) * 120))

					elif trap13diff == "Rare":
						trap13enemygold = (int((trap13enemygold / 100) * 130))
						trap13xpgain = (int((trap13xpgain / 100) * 130))

					elif trap13diff == "Legendary":
						trap13enemygold = (int((trap13enemygold / 100) * 140))
						trap13xpgain = (int((trap13xpgain / 100) * 140))

					elif trap13diff == "Mythical":
						trap13enemygold = (int((trap13enemygold / 100) * 150))
						trap13xpgain = (int((trap13xpgain / 100) * 150))
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
			except:
				pass
			try:
				em.add_field(name="Failed Traps", value=list1)
			except:
				pass
			try:
				em.add_field(name="Broken Traps", value=list2)
			except:
				pass
			await ctx.send(embed=em)

			if not list3 == "_ _\n":
				em2 = discord.Embed(color=discord.Colour(0xffffff))
				em2.set_author(name="{}'s Traps 2nd page".format(userinfo["name"]), icon_url=user.avatar_url)
				try:
					em2.add_field(name="Successful Traps", value=list3)
				except:
					pass
				try:
					em2.add_field(name="Failed Traps", value=list4)
				except:
					pass
				try:
					em2.add_field(name="Broken Traps", value=list5)
				except:
					pass
			
				await ctx.send(embed=em2)
			else:
				pass

			totalgold = int(trap1enemygold) + int(trap2enemygold) +  int(trap3enemygold) +  int(trap4enemygold) +  int(trap5enemygold) +  int(trap6enemygold) +  int(trap7enemygold) +  int(trap8enemygold) +  int(trap9enemygold) +  int(trap10enemygold) +  int(trap11enemygold) +  int(trap12enemygold) +  int(trap13enemygold)
			totalexp = int(trap1xpgain) + int(trap2xpgain) +  int(trap3xpgain) +  int(trap4xpgain) +  int(trap5xpgain) +  int(trap6xpgain) +  int(trap7xpgain) +  int(trap8xpgain) +  int(trap9xpgain) +  int(trap10xpgain) +  int(trap11xpgain) +  int(trap12xpgain) +  int(trap13xpgain)

			em = discord.Embed(color=discord.Colour(0xffffff))
			em.set_author(name="{}'s total rewards".format(userinfo["name"]), icon_url=user.avatar_url)
			try:
				em.add_field(name="You have earned!", value="\n<:Gold:639484869809930251>**{}**\n<:Experience:560809103346368522>**{}**".format(totalgold, totalexp))
			except:
				pass
		
			await ctx.send(embed=em)

			userinfo["gold"] += totalgold
			userinfo["exp"] += totalexp
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = userinfo["MaxHealth"]
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)

				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = userinfo["MaxHealth"]
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)

					if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
						userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
						userinfo["lvl"] = userinfo["lvl"] + 1
						userinfo["health"] = userinfo["MaxHealth"]
						em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
						await ctx.send(embed=em)

						if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
							userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
							userinfo["lvl"] = userinfo["lvl"] + 1
							userinfo["health"] = userinfo["MaxHealth"]
							em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
							await ctx.send(embed=em)

							if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
								userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
								userinfo["lvl"] = userinfo["lvl"] + 1
								userinfo["health"] = userinfo["MaxHealth"]
								em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
								await ctx.send(embed=em)

								if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
									userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
									userinfo["lvl"] = userinfo["lvl"] + 1
									userinfo["health"] = userinfo["MaxHealth"]
									em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
									await ctx.send(embed=em)

									if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
										userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
										userinfo["lvl"] = userinfo["lvl"] + 1
										userinfo["health"] = userinfo["MaxHealth"]
										em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
										await ctx.send(embed=em)

										if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
											userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
											userinfo["lvl"] = userinfo["lvl"] + 1
											userinfo["health"] = userinfo["MaxHealth"]
											em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
											await ctx.send(embed=em)

											if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
												userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
												userinfo["lvl"] = userinfo["lvl"] + 1
												userinfo["health"] = userinfo["MaxHealth"]
												em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
												await ctx.send(embed=em)
			userinfo["trap_block"] = curr_time
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			
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