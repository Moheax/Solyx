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

class craft(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name="craft", pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _craft(self, ctx):
		"""Crafting!"""
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

	@_craft.group(name="Axe", aliases=["axe"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _axe(self, ctx):
		"""Upgrade your axe!"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to upgrade their Axe")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		if userinfo["axelvl"] == 0:
			userinfo["axelvl"] = 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		if userinfo["axelvl"] == 1:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 10000
					wood = 10
					stone = 10
					metal = 5

					em = discord.Embed(title="Do you want to upgrade your axe?", description="<:Axe:573574740220969007> Axe level: 1 --> 2\nWood gain + 2\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n\n Type yes to craft!".format(cost, wood, stone, metal), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your axe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your axe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your axe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your axe!**".format(neededmetal))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["axelvl"] = 2
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Axe:573574740220969007> Axe level 2 crafted!", description="You have succesfully upgraded your axe!\nYou now earn 2 more wood per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["axelvl"] == 2:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 12500
					wood = 25
					stone = 25
					metal = 10
					planks = 5
					

					em = discord.Embed(title="Do you want to upgrade your axe?", description="<:Axe:573574740220969007> Axe level: 2 --> 3\nWood gain + 2\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your axe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your axe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your axe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your axe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your axe!**".format(neededplanks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["axelvl"] = 3
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Axe:573574740220969007> Axe level 3 crafted!", description="You have succesfully upgraded your axe!\nYou now earn 2 more wood per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["axelvl"] == 3:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 15000
					wood = 40
					stone = 40
					metal = 15
					planks = 10
					bricks = 10
					

					em = discord.Embed(title="Do you want to upgrade your axe?", description="<:Axe:573574740220969007> Axe level: 3 --> 4\nWood gain + 2\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your axe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your axe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your axe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your axe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your axe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your axe!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["axelvl"] = 4
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Axe:573574740220969007> Axe level 4 crafted!", description="You have succesfully upgraded your axe!\nYou now earn 2 more wood per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["axelvl"] == 4:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 17500
					wood = 60
					stone = 60
					metal = 30
					planks = 10
					bricks = 10
					iron_plates = 5
					

					em = discord.Embed(title="Do you want to upgrade your axe?", description="<:Axe:573574740220969007> Axe level: 4 --> 5\nWood gain + 2\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your axe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your axe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your axe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your axe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your axe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your axe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your axe!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["axelvl"] = 5
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Axe:573574740220969007> Axe level 5 crafted!", description="You have succesfully upgraded your axe!\nYou now earn 2 more wood per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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
		elif userinfo["axelvl"] == 5:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 100:
				em = discord.Embed(title="<:Axe:573574740220969007> Max axe level reached!", description="You have reached your maximum axe level.\n Reach level 100+ to increase max level to 6\nOr become a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			if userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer" or userinfo["role"] == "Player" and userinfo["lvl"] >= 100:
				try:
					cost = 20000
					wood = 75
					stone = 75
					metal = 40
					planks = 15
					bricks = 15
					iron_plates = 10
					

					em = discord.Embed(title="Do you want to upgrade your axe?", description="<:Axe:573574740220969007> Axe level: 5 --> 6\nWood gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your axe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your axe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your axe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your axe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your axe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your axe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your axe!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["axelvl"] = 6
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Axe:573574740220969007> Axe level 6 crafted!", description="You have succesfully upgraded your axe!\nYou now have +1 min gain, +2 max gain per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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
		if userinfo["axelvl"] == 6:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 200:
				em = discord.Embed(title="<:Axe:573574740220969007> Max axe level reached!", description="You have reached your maximum axe level.\n Reach level 200+ to increase max level to 7\nOr become a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
		
			if userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer" or userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				try:
					cost = 22500
					wood = 90
					stone = 90
					metal = 50
					planks = 25
					bricks = 25
					iron_plates = 15
					

					em = discord.Embed(title="Do you want to upgrade your axe?", description="<:Axe:573574740220969007> Axe level: 6 --> 7\nWood gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your axe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your axe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your axe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your axe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your axe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your axe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your axe!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["axelvl"] = 7
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Axe:573574740220969007> Axe level 7 crafted!", description="You have succesfully upgraded your axe!\nYou now have +1 min gain, +2 max gain per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["axelvl"] == 7:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="<:Axe:573574740220969007> Max axe level reached!", description="You have reached your maximum axe level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			if userinfo["role"] == "patreon1":
				em = discord.Embed(title="<:Axe:573574740220969007> Max axe level reached!", description="You have reached your maximum axe level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
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
					cost = 25000
					wood = 100
					stone = 100
					metal = 60
					planks = 40
					bricks = 40
					iron_plates = 25
					

					em = discord.Embed(title="Do you want to upgrade your axe?", description="<:Axe:573574740220969007> Axe level: 7 --> 8\nWood gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your axe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your axe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your axe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your axe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your axe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your axe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your axe!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["axelvl"] = 8
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Axe:573574740220969007> Axe level 8 crafted!", description="You have succesfully upgraded your axe!\nYou now have +1 min gain, +2 max gain per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["axelvl"] == 8:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="<:Axe:573574740220969007> Max axe level reached!", description="You have reached your maximum axe level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2":
				em = discord.Embed(title="<:Axe:573574740220969007> Max axe level reached!", description="You have reached your maximum axe level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 27500
					wood = 110
					stone = 110
					metal = 70
					planks = 50
					bricks = 50
					iron_plates = 40
					

					em = discord.Embed(title="Do you want to upgrade your axe?", description="<:Axe:573574740220969007> Axe level: 8 --> 9\nWood gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your axe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your axe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your axe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your axe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your axe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your axe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your axe!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["axelvl"] = 9
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Axe:573574740220969007> Axe level 9 crafted!", description="You have succesfully upgraded your axe!\nYou now have +1 min gain, +2 max gain per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["axelvl"] == 9:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="<:Axe:573574740220969007> Max axe level reached!", description="You have reached your maximum axe level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3":
				em = discord.Embed(title="<:Axe:573574740220969007> Max axe level reached!", description="You have reached your maximum axe level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 30000
					wood = 120
					stone = 120
					metal = 80
					planks = 60
					bricks = 60
					iron_plates = 50
					

					em = discord.Embed(title="Do you want to upgrade your axe?", description="<:Axe:573574740220969007> Axe level: 8 --> 9\nWood gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your axe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your axe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your axe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your axe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your axe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your axe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your axe!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["axelvl"] = 10
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Axe:573574740220969007> Axe level 10 crafted!", description="You have succesfully upgraded your axe!\nThis is the last level!\nYou now have +1 min gain, +2 max gain per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["axelvl"] == 10:
			em = discord.Embed(title="<:Axe:573574740220969007> Axe level 10 already crafted!", description="Level 10 is the last level!".format(ctx.prefix), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
				return
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
	
	@_craft.group(name="Pickaxe", aliases=["pickaxe"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _pickaxe(self, ctx):
		"""Upgrade your pickaxe!"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has Tried to upgrade their Pickaxe")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		if userinfo["pickaxelvl"] == 0:
			userinfo["pickaxelvl"] = 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		if userinfo["pickaxelvl"] == 1:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 10000
					wood = 10
					stone = 10
					metal = 5

					em = discord.Embed(title="Do you want to upgrade your pickaxe?", description="<:Pickaxe:573574740640530471>  Pickaxe level: 1 --> 2\nStone and metal gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n\n Type yes to craft!".format(cost, wood, stone, metal), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your pickaxe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your pickaxe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your pickaxe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your pickaxe!**".format(neededmetal))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["pickaxelvl"] = 2
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Pickaxe:573574740640530471>  Pickaxe level 2 crafted!", description="You have succesfully upgraded your pickaxe!\nYou now earn 2 more wood per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["pickaxelvl"] == 2:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 12500
					wood = 25
					stone = 25
					metal = 10
					planks = 5
					

					em = discord.Embed(title="Do you want to upgrade your pickaxe?", description="<:Pickaxe:573574740640530471>  Pickaxe level: 2 --> 3\nStone and metal gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your pickaxe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your pickaxe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your pickaxe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your pickaxe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your pickaxe!**".format(neededplanks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["pickaxelvl"] = 3
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Pickaxe:573574740640530471>  Pickaxe level 3 crafted!", description="You have succesfully upgraded your pickaxe!\nYou now earn 2 more wood per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["pickaxelvl"] == 3:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 15000
					wood = 40
					stone = 40
					metal = 15
					planks = 10
					bricks = 10
					

					em = discord.Embed(title="Do you want to upgrade your pickaxe?", description="<:Pickaxe:573574740640530471>  Pickaxe level: 3 --> 4\nStone and metal gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your pickaxe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your pickaxe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your pickaxe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your pickaxe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your pickaxe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your pickaxe!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["pickaxelvl"] = 4
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Pickaxe:573574740640530471>  Pickaxe level 4 crafted!", description="You have succesfully upgraded your pickaxe!\nYou now earn 2 more wood per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["pickaxelvl"] == 4:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 17500
					wood = 60
					stone = 60
					metal = 30
					planks = 10
					bricks = 10
					iron_plates = 5
					

					em = discord.Embed(title="Do you want to upgrade your pickaxe?", description="<:Pickaxe:573574740640530471>  Pickaxe level: 4 --> 5\Stone and metal gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your pickaxe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your pickaxe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your pickaxe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your pickaxe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your pickaxe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your pickaxe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your pickaxe!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["pickaxelvl"] = 5
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Pickaxe:573574740640530471>  Pickaxe level 5 crafted!", description="You have succesfully upgraded your pickaxe!\nYou now earn 2 more wood per chop!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["pickaxelvl"] == 5:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 100:
				em = discord.Embed(title="<:Axe:573574740220969007> <:Axe:573574740220969007> Max pickaxe level reached!", description="You have reached your maximum pickaxe level.\n Reach level 100+ to increase max level to 6\nOr become a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer" or userinfo["role"] == "Player" and userinfo["lvl"] >= 100:
				try:
					cost = 20000
					wood = 75
					stone = 75
					metal = 40
					planks = 15
					bricks = 15
					iron_plates = 10
					

					em = discord.Embed(title="Do you want to upgrade your pickaxe?", description="<:Pickaxe:573574740640530471>  Pickaxe level: 5 --> 6\nStone and metal gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your pickaxe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your pickaxe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your pickaxe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your pickaxe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your pickaxe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your pickaxe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your pickaxe!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["pickaxelvl"] = 6
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Pickaxe:573574740640530471>  Pickaxe level 6 crafted!", description="You have succesfully upgraded your pickaxe!\nYou now have +1 min gain, +2 max gain stone and metal per mine!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["pickaxelvl"] == 6:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 200:
				em = discord.Embed(title="<:Axe:573574740220969007> Max pickaxe level reached!", description="You have reached your maximum pickaxe level.\n Reach level 200+ to increase max level to 7\nOr become a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer" or userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				try:
					cost = 22500
					wood = 90
					stone = 90
					metal = 50
					planks = 25
					bricks = 25
					iron_plates = 15
					

					em = discord.Embed(title="Do you want to upgrade your pickaxe?", description="<:Pickaxe:573574740640530471>  Pickaxe level: 6 --> 7\nStone and metal gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your pickaxe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your pickaxe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your pickaxe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your pickaxe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your pickaxe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your pickaxe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your pickaxe!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["pickaxelvl"] = 7
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Pickaxe:573574740640530471>  Pickaxe level 7 crafted!", description="You have succesfully upgraded your pickaxe!\nYou now have +1 min gain, +2 max gain stone and metal per mine!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["pickaxelvl"] == 7:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="<:Axe:573574740220969007> Max pickaxe level reached!", description="You have reached your maximum pickaxe level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1":
				em = discord.Embed(title="<:Axe:573574740220969007> Max pickaxe level reached!", description="You have reached your maximum pickaxe level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 25000
					wood = 100
					stone = 100
					metal = 60
					planks = 40
					bricks = 40
					iron_plates = 25
					

					em = discord.Embed(title="Do you want to upgrade your pickaxe?", description="<:Pickaxe:573574740640530471>  Pickaxe level: 7 --> 8\nStone and metal gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your pickaxe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your pickaxe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your pickaxe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your pickaxe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your pickaxe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your pickaxe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your pickaxe!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["pickaxelvl"] = 8
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Pickaxe:573574740640530471>  Pickaxe level 8 crafted!", description="You have succesfully upgraded your pickaxe!\nYou now have +1 min gain, +2 max gain stone and metal per mine!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["pickaxelvl"] == 8:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="<:Axe:573574740220969007> Max pickaxe level reached!", description="You have reached your maximum pickaxe level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2":
				em = discord.Embed(title="<:Axe:573574740220969007> Max pickaxe level reached!", description="You have reached your maximum pickaxe level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 27500
					wood = 110
					stone = 110
					metal = 70
					planks = 50
					bricks = 50
					iron_plates = 40
					

					em = discord.Embed(title="Do you want to upgrade your pickaxe?", description="<:Pickaxe:573574740640530471>  Pickaxe level: 8 --> 9\nStone and metal gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your pickaxe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your pickaxe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your pickaxe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your pickaxe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your pickaxe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your pickaxe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your pickaxe!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["pickaxelvl"] = 9
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Pickaxe:573574740640530471>  Pickaxe level 9 crafted!", description="You have succesfully upgraded your pickaxe!\nYou now have +1 min gain, +2 max gain stone and metal per mine!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["pickaxelvl"] == 9:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="<:Axe:573574740220969007> Max pickaxe level reached!", description="You have reached your maximum pickaxe level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3":
				em = discord.Embed(title="<:Axe:573574740220969007> Max pickaxe level reached!", description="You have reached your maximum pickaxe level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
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
					cost = 30000
					wood = 120
					stone = 120
					metal = 80
					planks = 60
					bricks = 60
					iron_plates = 50
					

					em = discord.Embed(title="Do you want to upgrade your pickaxe?", description="<:Pickaxe:573574740640530471>  Pickaxe level: 8 --> 9\nStone and metal gain +1 min gain, +2 max gain\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your pickaxe!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your pickaxe!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your pickaxe!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your pickaxe!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your pickaxe!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your pickaxe!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your pickaxe!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["pickaxelvl"] = 10
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="<:Pickaxe:573574740640530471>  Pickaxe level 10 crafted!", description="You have succesfully upgraded your pickaxe!\nThis is the last level!\nYou now have +1 min gain, +2 max gain stone and metal per mine!".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["pickaxelvl"] == 10:
			em = discord.Embed(title="<:Pickaxe:573574740640530471>  Pickaxe level 10 already crafted!", description="Level 10 is the last level!".format(ctx.prefix), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
				return
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	
	@_craft.group(name="Saw", aliases=["saw"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _saw(self, ctx):
		"""Upgrade your saw! to make more planks"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has Tried to upgrade their Pickaxe")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		if userinfo["sawlvl"] == 0:
			userinfo["sawlvl"] = 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		if userinfo["sawlvl"] == 1:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 10000
					wood = 10
					stone = 10
					metal = 5

					em = discord.Embed(title="Do you want to upgrade your saw?", description="Saw level: 1 --> 2\nPlanks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n\n Type yes to craft!".format(cost, wood, stone, metal), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your saw!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your saw!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your saw!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your saw!**".format(neededmetal))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["sawlvl"] = 2
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Saw level 2 crafted!", description="You have succesfully upgraded your saw!\nYou now have +1 plank limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["sawlvl"] == 2:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 12500
					wood = 25
					stone = 25
					metal = 10
					planks = 5
					

					em = discord.Embed(title="Do you want to upgrade your saw?", description="Saw level: 2 --> 3\nPlanks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your saw!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your saw!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your saw!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your saw!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your saw!**".format(neededplanks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["sawlvl"] = 3
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Saw level 3 crafted!", description="You have succesfully upgraded your saw!\nYou now have +1 plank limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["sawlvl"] == 3:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 15000
					wood = 40
					stone = 40
					metal = 15
					planks = 10
					bricks = 10
					

					em = discord.Embed(title="Do you want to upgrade your saw?", description="Saw level: 3 --> 4\nPlanks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your saw!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your saw!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your saw!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your saw!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your saw!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your saw!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["sawlvl"] = 4
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Saw level 4 crafted!", description="You have succesfully upgraded your saw!\nYou now have +1 plank limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["sawlvl"] == 4:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 17500
					wood = 60
					stone = 60
					metal = 30
					planks = 10
					bricks = 10
					iron_plates = 5
					

					em = discord.Embed(title="Do you want to upgrade your saw?", description="Saw level: 4 --> 5\nPlanks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your saw!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your saw!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your saw!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your saw!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your saw!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your saw!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your saw!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["sawlvl"] = 5
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Saw level 5 crafted!", description="You have succesfully upgraded your saw!\nYou now have +1 plank limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["sawlvl"] == 5:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 100:
				em = discord.Embed(title="<:Axe:573574740220969007> Max saw level reached!", description="You have reached your maximum saw level.\n Reach level 100+ to increase max level to 6\nOr become a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer" or userinfo["role"] == "Player" and userinfo["lvl"] >= 100:
				try:
					cost = 20000
					wood = 75
					stone = 75
					metal = 40
					planks = 15
					bricks = 15
					iron_plates = 10
					

					em = discord.Embed(title="Do you want to upgrade your saw?", description="Saw level: 5 --> 6\nPlanks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your saw!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your saw!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your saw!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your saw!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your saw!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your saw!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your saw!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["sawlvl"] = 6
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Saw level 6 crafted!", description="You have succesfully upgraded your saw!\nYou now have +1 plank limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["sawlvl"] == 6:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 200:
				em = discord.Embed(title="Max saw level reached!", description="You have reached your maximum saw level.\n Reach level 200+ to increase max level to 7\nOr become a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer" or userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				try:
					cost = 22500
					wood = 90
					stone = 90
					metal = 50
					planks = 25
					bricks = 25
					iron_plates = 15
					

					em = discord.Embed(title="Do you want to upgrade your saw?", description="Saw level: 6 --> 7\nPlanks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your saw!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your saw!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your saw!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your saw!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your saw!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your saw!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your saw!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["sawlvl"] = 7
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Saw level 7 crafted!", description="You have succesfully upgraded your saw!\nYou now have +1 plank limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["sawlvl"] == 7:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="Max saw level reached!", description="You have reached your maximum saw level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1":
				em = discord.Embed(title="Max saw level reached!", description="You have reached your maximum saw level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 25000
					wood = 100
					stone = 100
					metal = 60
					planks = 40
					bricks = 40
					iron_plates = 25
					

					em = discord.Embed(title="Do you want to upgrade your saw?", description="Saw level: 7 --> 8\nPlanks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your saw!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your saw!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your saw!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your saw!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your saw!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your saw!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your saw!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["sawlvl"] = 8
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Saw level 8 crafted!", description="You have succesfully upgraded your saw!\nYou now have +1 plank limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["sawlvl"] == 8:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="Max saw level reached!", description="You have reached your maximum saw level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2":
				em = discord.Embed(title="Max saw level reached!", description="You have reached your maximum saw level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 27500
					wood = 110
					stone = 110
					metal = 70
					planks = 50
					bricks = 50
					iron_plates = 40
					

					em = discord.Embed(title="Do you want to upgrade your saw?", description="Saw level: 8 --> 9\nPlanks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your saw!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your saw!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your saw!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your saw!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your saw!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your saw!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your saw!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["sawlvl"] = 9
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Saw level 9 crafted!", description="You have succesfully upgraded your saw!\nYou now have +1 plank limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["sawlvl"] == 9:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="Max saw level reached!", description="You have reached your maximum saw level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3":
				em = discord.Embed(title="Max saw level reached!", description="You have reached your maximum saw level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
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
					cost = 30000
					wood = 120
					stone = 120
					metal = 80
					planks = 60
					bricks = 60
					iron_plates = 50
					

					em = discord.Embed(title="Do you want to upgrade your saw?", description="Saw level: 8 --> 9\nPlanks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your saw!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your saw!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your saw!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your saw!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your saw!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your saw!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your saw!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["sawlvl"] = 10
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Saw level 10 crafted!", description="You have succesfully upgraded your saw!\nThis is the last level!\nYou now have +1 plank limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["sawlvl"] == 10:
			em = discord.Embed(title="Saw level 10 already crafted!", description="Level 10 is the last level!".format(ctx.prefix), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
				return
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	
	@_craft.group(name="Chisel", aliases=["chisel"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _chisel(self, ctx):
		"""Upgrade your chisel! to make more planks"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has Tried to upgrade their Pickaxe")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		if userinfo["chisellvl"] == 0:
			userinfo["chisellvl"] = 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		if userinfo["chisellvl"] == 1:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 10000
					wood = 10
					stone = 10
					metal = 5

					em = discord.Embed(title="Do you want to upgrade your chisel?", description="Chisel level: 1 --> 2\nBricks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n\n Type yes to craft!".format(cost, wood, stone, metal), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your chisel!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your chisel!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your chisel!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your chisel!**".format(neededmetal))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["chisellvl"] = 2
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Chisel level 2 crafted!", description="You have succesfully upgraded your chisel!\nYou now have +1 brick limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["chisellvl"] == 2:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 12500
					wood = 25
					stone = 25
					metal = 10
					planks = 5
					

					em = discord.Embed(title="Do you want to upgrade your chisel?", description="Chisel level: 2 --> 3\nBricks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your chisel!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your chisel!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your chisel!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your chisel!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your chisel!**".format(neededplanks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["chisellvl"] = 3
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Chisel level 3 crafted!", description="You have succesfully upgraded your chisel!\nYou now have +1 brick limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["chisellvl"] == 3:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 15000
					wood = 40
					stone = 40
					metal = 15
					planks = 10
					bricks = 10
					

					em = discord.Embed(title="Do you want to upgrade your chisel?", description="Chisel level: 3 --> 4\nBricks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your chisel!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your chisel!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your chisel!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your chisel!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your chisel!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your chisel!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["chisellvl"] = 4
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Chisel level 4 crafted!", description="You have succesfully upgraded your chisel!\nYou now have +1 brick limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["chisellvl"] == 4:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 17500
					wood = 60
					stone = 60
					metal = 30
					planks = 10
					bricks = 10
					iron_plates = 5
					

					em = discord.Embed(title="Do you want to upgrade your chisel?", description="Chisel level: 4 --> 5\nBricks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your chisel!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your chisel!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your chisel!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your chisel!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your chisel!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your chisel!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your chisel!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["chisellvl"] = 5
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Chisel level 5 crafted!", description="You have succesfully upgraded your chisel!\nYou now have +1 brick limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["chisellvl"] == 5:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 100:
				em = discord.Embed(title="<:Axe:573574740220969007> Max chisel level reached!", description="You have reached your maximum chisel level.\n Reach level 100+ to increase max level to 6\nOr become a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer" or userinfo["role"] == "Player" and userinfo["lvl"] >= 100:
				try:
					cost = 20000
					wood = 75
					stone = 75
					metal = 40
					planks = 15
					bricks = 15
					iron_plates = 10
					

					em = discord.Embed(title="Do you want to upgrade your chisel?", description="Chisel level: 5 --> 6\nBricks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your chisel!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your chisel!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your chisel!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your chisel!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your chisel!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your chisel!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your chisel!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["chisellvl"] = 6
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Chisel level 6 crafted!", description="You have succesfully upgraded your chisel!\nYou now have +1 brick limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["chisellvl"] == 6:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 200:
				em = discord.Embed(title="Max chisel level reached!", description="You have reached your maximum chisel level.\n Reach level 200+ to increase max level to 7\nOr become a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer" or userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				try:
					cost = 22500
					wood = 90
					stone = 90
					metal = 50
					planks = 25
					bricks = 25
					iron_plates = 15
					

					em = discord.Embed(title="Do you want to upgrade your chisel?", description="Chisel level: 6 --> 7\nBricks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your chisel!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your chisel!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your chisel!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your chisel!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your chisel!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your chisel!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your chisel!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["chisellvl"] = 7
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Chisel level 7 crafted!", description="You have succesfully upgraded your chisel!\nYou now have +1 brick limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["chisellvl"] == 7:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="Max chisel level reached!", description="You have reached your maximum chisel level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1":
				em = discord.Embed(title="Max chisel level reached!", description="You have reached your maximum chisel level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 25000
					wood = 100
					stone = 100
					metal = 60
					planks = 40
					bricks = 40
					iron_plates = 25
					

					em = discord.Embed(title="Do you want to upgrade your chisel?", description="Chisel level: 7 --> 8\nBricks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your chisel!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your chisel!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your chisel!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your chisel!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your chisel!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your chisel!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your chisel!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["chisellvl"] = 8
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Chisel level 8 crafted!", description="You have succesfully upgraded your chisel!\nYou now have +1 brick limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["chisellvl"] == 8:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="Max chisel level reached!", description="You have reached your maximum chisel level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2":
				em = discord.Embed(title="Max chisel level reached!", description="You have reached your maximum chisel level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 27500
					wood = 110
					stone = 110
					metal = 70
					planks = 50
					bricks = 50
					iron_plates = 40
					

					em = discord.Embed(title="Do you want to upgrade your chisel?", description="Chisel level: 8 --> 9\nBricks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your chisel!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your chisel!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your chisel!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your chisel!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your chisel!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your chisel!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your chisel!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["chisellvl"] = 9
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Chisel level 9 crafted!", description="You have succesfully upgraded your chisel!\nYou now have +1 brick limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["chisellvl"] == 9:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="Max chisel level reached!", description="You have reached your maximum chisel level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3":
				em = discord.Embed(title="Max chisel level reached!", description="You have reached your maximum chisel level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
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
					cost = 30000
					wood = 120
					stone = 120
					metal = 80
					planks = 60
					bricks = 60
					iron_plates = 50
					

					em = discord.Embed(title="Do you want to upgrade your chisel?", description="Chisel level: 8 --> 9\nBricks made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your chisel!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your chisel!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your chisel!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your chisel!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your chisel!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your chisel!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your chisel!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["chisellvl"] = 10
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Chisel level 10 crafted!", description="You have succesfully upgraded your chisel!\nThis is the last level!\nYou now have +1 brick limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["chisellvl"] == 10:
			em = discord.Embed(title="Chisel level 10 already crafted!", description="Level 10 is the last level!".format(ctx.prefix), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
				return
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	
	@_craft.group(name="Hammer", aliases=["hammer"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _hammer(self, ctx):
		"""Upgrade your hammer! to make more planks"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has Tried to upgrade their Pickaxe")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		if userinfo["hammerlvl"] == 0:
			userinfo["hammerlvl"] = 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		if userinfo["hammerlvl"] == 1:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 10000
					wood = 10
					stone = 10
					metal = 5

					em = discord.Embed(title="Do you want to upgrade your hammer?", description="Hammer level: 1 --> 2\nIront plates made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n\n Type yes to craft!".format(cost, wood, stone, metal), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your hammer!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your hammer!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your hammer!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your hammer!**".format(neededmetal))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["hammerlvl"] = 2
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Hammer level 2 crafted!", description="You have succesfully upgraded your hammer!\nYou now have +1 iron plate limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["hammerlvl"] == 2:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 12500
					wood = 25
					stone = 25
					metal = 10
					planks = 5
					

					em = discord.Embed(title="Do you want to upgrade your hammer?", description="Hammer level: 2 --> 3\nIront plates made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your hammer!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your hammer!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your hammer!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your hammer!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your hammer!**".format(neededplanks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["hammerlvl"] = 3
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Hammer level 3 crafted!", description="You have succesfully upgraded your hammer!\nYou now have +1 iron plate limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["hammerlvl"] == 3:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 15000
					wood = 40
					stone = 40
					metal = 15
					planks = 10
					bricks = 10
					

					em = discord.Embed(title="Do you want to upgrade your hammer?", description="Hammer level: 3 --> 4\nIront plates made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your hammer!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your hammer!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your hammer!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your hammer!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your hammer!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your hammer!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["hammerlvl"] = 4
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Hammer level 4 crafted!", description="You have succesfully upgraded your hammer!\nYou now have +1 iron plate limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		elif userinfo["hammerlvl"] == 4:
			if userinfo["role"] == "Player" or userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 17500
					wood = 60
					stone = 60
					metal = 30
					planks = 10
					bricks = 10
					iron_plates = 5
					

					em = discord.Embed(title="Do you want to upgrade your hammer?", description="Hammer level: 4 --> 5\nIront plates made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your hammer!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your hammer!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your hammer!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your hammer!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your hammer!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your hammer!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your hammer!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["hammerlvl"] = 5
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Hammer level 5 crafted!", description="You have succesfully upgraded your hammer!\nYou now have +1 iron plate limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["hammerlvl"] == 5:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 100:
				em = discord.Embed(title="<:Axe:573574740220969007> Max hammer level reached!", description="You have reached your maximum hammer level.\n Reach level 100+ to increase max level to 6\nOr become a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer" or userinfo["role"] == "Player" and userinfo["lvl"] >= 100:
				try:
					cost = 20000
					wood = 75
					stone = 75
					metal = 40
					planks = 15
					bricks = 15
					iron_plates = 10
					

					em = discord.Embed(title="Do you want to upgrade your hammer?", description="Hammer level: 5 --> 6\nIront plates made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your hammer!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your hammer!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your hammer!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your hammer!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your hammer!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your hammer!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your hammer!**".format(neededbricks))
							return

						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["hammerlvl"] = 6
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Hammer level 6 crafted!", description="You have succesfully upgraded your hammer!\nYou now have +1 iron plate limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["hammerlvl"] == 6:
			if userinfo["role"] == "Player" and userinfo["lvl"] <= 200:
				em = discord.Embed(title="Max hammer level reached!", description="You have reached your maximum hammer level.\n Reach level 200+ to increase max level to 7\nOr become a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer" or userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				try:
					cost = 22500
					wood = 90
					stone = 90
					metal = 50
					planks = 25
					bricks = 25
					iron_plates = 15
					

					em = discord.Embed(title="Do you want to upgrade your hammer?", description="Hammer level: 6 --> 7\nIront plates made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your hammer!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your hammer!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your hammer!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your hammer!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your hammer!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your hammer!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your hammer!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["hammerlvl"] = 7
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Hammer level 7 crafted!", description="You have succesfully upgraded your hammer!\nYou now have +1 iron plate limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["hammerlvl"] == 7:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="Max hammer level reached!", description="You have reached your maximum hammer level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1":
				em = discord.Embed(title="Max hammer level reached!", description="You have reached your maximum hammer level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 25000
					wood = 100
					stone = 100
					metal = 60
					planks = 40
					bricks = 40
					iron_plates = 25
					

					em = discord.Embed(title="Do you want to upgrade your hammer?", description="Hammer level: 7 --> 8\nIront plates made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your hammer!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your hammer!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your hammer!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your hammer!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your hammer!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your hammer!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your hammer!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["hammerlvl"] = 8
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Hammer level 8 crafted!", description="You have succesfully upgraded your hammer!\nYou now have +1 iron plate limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["hammerlvl"] == 8:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="Max hammer level reached!", description="You have reached your maximum hammer level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2":
				em = discord.Embed(title="Max hammer level reached!", description="You have reached your maximum hammer level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4" or userinfo["role"] == "Developer":
				try:
					cost = 27500
					wood = 110
					stone = 110
					metal = 70
					planks = 50
					bricks = 50
					iron_plates = 40
					

					em = discord.Embed(title="Do you want to upgrade your hammer?", description="Hammer level: 8 --> 9\nIront plates made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your hammer!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your hammer!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your hammer!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your hammer!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your hammer!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your hammer!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your hammer!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["hammerlvl"] = 9
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Hammer level 9 crafted!", description="You have succesfully upgraded your hammer!\nYou now have +1 iron plate limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["hammerlvl"] == 9:
			if userinfo["role"] == "Player" and userinfo["lvl"] >= 200:
				em = discord.Embed(title="Max hammer level reached!", description="You have reached your maximum hammer level.\n \nBecome a patreon to increase the max level!", color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["role"] == "patreon1" or userinfo["role"] == "patreon2" or userinfo["role"] == "patreon3":
				em = discord.Embed(title="Max hammer level reached!", description="You have reached your maximum hammer level.\n \nBecome a higher tier patreon to increase the max level!", color=discord.Colour(0xffffff))
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
					cost = 30000
					wood = 120
					stone = 120
					metal = 80
					planks = 60
					bricks = 60
					iron_plates = 50
					

					em = discord.Embed(title="Do you want to upgrade your hammer?", description="Hammer level: 8 --> 9\nIront plates made +1\nThis will cost you:\n<:Gold:639484869809930251> {}\n<:Wood:573574660185260042> {}\n<:Stone:573574662525550593> {}\n<:Metal:573574661108006915> {}\n<:PlanksbyMaxie:780992714463510530> {}\n<:BricksbyMaxie:780999521249263616> {}\n<:IronPlatebyMaxie:781003325675012146> {}\n\n Type yes to craft!".format(cost, wood, stone, metal, planks, bricks, iron_plates), color=discord.Colour(0xffffff))
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
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to upgrade your hammer!**".format(neededgold))
							return

						if not int(userinfo["wood"]) >= int(wood):
							neededwood = int(wood) - int(userinfo["wood"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to upgrade your hammer!**".format(neededwood))
							return

						if not int(userinfo["stone"]) >= int(stone):
							neededstone = int(stone) - int(userinfo["stone"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to upgrade your hammer!**".format(neededstone))
							return

						if not int(userinfo["metal"]) >= int(metal):
							neededmetal = int(metal) - int(userinfo["metal"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to upgrade your hammer!**".format(neededmetal))
							return
						
						if not int(userinfo["planks"]) >= int(planks):
							neededplanks = int(planks) - int(userinfo["planks"])
							await ctx.send("<:PlanksbyMaxie:780992714463510530>  **| You need {} more planks to upgrade your hammer!**".format(neededplanks))
							return

						if not int(userinfo["bricks"]) >= int(bricks):
							neededbricks = int(bricks) - int(userinfo["bricks"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more bricks to upgrade your hammer!**".format(neededbricks))
							return

						if not int(userinfo["iron_plates"]) >= int(iron_plates):
							needediron_plates = int(iron_plates) - int(userinfo["iron_plates"])
							await ctx.send("<:Solyx:560809141766193152> **| You need {} more iron plates to upgrade your hammer!**".format(neededbricks))
							return
						userinfo["gold"] = userinfo["gold"] - cost
						userinfo["wood"] = userinfo["wood"] - wood
						userinfo["stone"] = userinfo["stone"] - stone
						userinfo["metal"] = userinfo["metal"] - metal
						userinfo["planks"] = userinfo["planks"] - planks
						userinfo["bricks"] = userinfo["bricks"] - bricks
						userinfo["iron_plates"] = userinfo["iron_plates"] - iron_plates
					
						userinfo["hammerlvl"] = 10
						

						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						em = discord.Embed(title="Hammer level 10 crafted!", description="You have succesfully upgraded your hammer!\nThis is the last level!\nYou now have +1 iron plate limit.".format(ctx.prefix), color=discord.Colour(0xffffff))
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

		if userinfo["hammerlvl"] == 10:
			em = discord.Embed(title="Hammer level 10 already crafted!", description="Level 10 is the last level!".format(ctx.prefix), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
				return
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
	n = craft(bot)
	bot.add_cog(n)