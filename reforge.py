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
from cogs.quests import _quest_check

class reforge(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		
	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def reforge(self, ctx, number:int):

		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has reforged a item")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if number not in range(1, 24): # Max
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["itemnotexist"]["translation"])
			return
		try:
			item = userinfo["inventory"][number-1]
		except:
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["noiteminslot"]["translation"])
			return

		


		refinement = item["refinement"]

		if refinement == "Normal":
			refinementlist = ["Fine"]
			newrefinement = randchoice(refinementlist)
			ref = "Fine"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 8000
			wood = 50
			stone = 25
			metal = 15

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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


		if refinement == "Fine":
			refinementlist = ["Keen"]
			newrefinement = randchoice(refinementlist)
			ref = "Keen"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 12000
			wood = 100
			stone = 50
			metal = 30

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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


		if refinement == "Keen":
			refinementlist = ["Mythic"]
			newrefinement = randchoice(refinementlist)
			ref = "Mythic"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 16000
			wood = 200
			stone = 100
			metal = 60

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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


		if refinement == "Mythic":
			refinementlist = ["Shiny"]
			newrefinement = randchoice(refinementlist)
			ref = "Shiny"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 20000
			wood = 300
			stone = 200
			metal = 150

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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


		if refinement == "Shiny":
			refinementlist = ["Superior"]
			newrefinement = randchoice(refinementlist)
			ref = "Superior"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 25000
			wood = 500
			stone = 350
			metal = 200

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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


		if refinement == "Superior":
			refinementlist = ["Vivid"]
			newrefinement = randchoice(refinementlist)
			ref = "Vivid"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 30000
			wood = 750
			stone = 500
			metal = 300

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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


		if refinement == "Vivid":
			refinementlist = ["Deadly"]
			newrefinement = randchoice(refinementlist)
			ref = "Deadly"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 35000
			wood = 1000
			stone = 750
			metal = 500

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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

		if refinement == "Deadly":
			refinementlist = ["Heroic"]
			newrefinement = randchoice(refinementlist)
			ref = "Heroic"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 40000
			wood = 1250
			stone = 1000
			metal = 750

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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
					
		if refinement == "Heroic":
			refinementlist = ["Ominous"]
			newrefinement = randchoice(refinementlist)
			ref = "Ominous"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 45000
			wood = 1500
			stone = 1250
			metal = 1000

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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
					
		if refinement == "Ominous":
			refinementlist = ["Strange"]
			newrefinement = randchoice(refinementlist)
			ref = "Strange"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 50000
			wood = 1750
			stone = 1500
			metal = 1250

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Refogred {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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
					
		if refinement == "Strange":
			refinementlist = ["Unreal"]
			newrefinement = randchoice(refinementlist)
			ref = "Unreal"

			newstats_min = item["stats_min"] + 2
			newstats_max = item["stats_max"] + 2

			cost = 60000
			wood = 2000
			stone = 1750
			metal = 1500

			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["reforge"]["confirmation"]["description"]["translation"].format(item["name"], item["rarity"], item["type"], item["refinement"], ref, item["stats_min"], item["stats_max"], newstats_min, newstats_max, cost, wood, stone, metal), color=discord.Colour(0xffffff))
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

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

				if userinfo["questname"] == "Reforge I":
					userinfo["questprogress"] += 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

				if not int(userinfo["gold"]) >= int(cost):
					neededgold = int(cost) - int(userinfo["gold"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more gold to reforge!**".format(neededgold))
					return

				if not int(userinfo["wood"]) >= int(wood):
					neededwood = int(wood) - int(userinfo["wood"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more wood to reforge!**".format(neededwood))
					return

				if not int(userinfo["stone"]) >= int(stone):
					neededstone = int(stone) - int(userinfo["stone"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more stone to reforge!**".format(neededstone))
					return

				if not int(userinfo["metal"]) >= int(metal):
					neededmetal = int(metal) - int(userinfo["metal"])
					await ctx.send("<:Solyx:560809141766193152> **| You need {} more metal to reforge!**".format(neededmetal))
					return

				newitem = {"name": item["name"], "type": item["type"], "rarity": item["rarity"], "stats_min": newstats_min, "stats_max": newstats_max, "refinement": newrefinement, "description": item["description"],  "image": item["image"]}
				userinfo["gold"] = userinfo["gold"] - cost
				userinfo["wood"] = userinfo["wood"] - wood
				userinfo["stone"] = userinfo["stone"] - stone
				userinfo["metal"] = userinfo["metal"] - metal
				
				userinfo["inventory"].remove(item)
				userinfo["inventory"].append(newitem)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				em = discord.Embed(title="Reforged {}".format(item["name"]), description="**Rarity:** {}\n**Refinement:** {}\n**Type:** {}\n**Stats:** {}-{}\n".format(newitem["rarity"], newitem["refinement"], newitem["type"], newitem["stats_min"], newitem["stats_max"]), color=discord.Colour(0xffffff))
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
			if refinement == "Unreal":
				ctx.send("<:Solyx:560809141766193152> | Item can't be reforged!")


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
	n = reforge(bot)
	bot.add_cog(n)