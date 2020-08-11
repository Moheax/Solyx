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




class loot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# - - - Loot - - - NEEDS WORKING (sometimes says you got nover even you got something/ opens twice for no reason)

	@commands.command(pass_context=True, no_pm=True, aliases=["lootbag", "lb", "chest", "open"])
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def crate(self, ctx):

		user = ctx.message.author

		print(user.name+"#"+user.discriminator,"has tried opening a crate")

		userinfo = db.users.find_one({ "_id": user.id })
		titlesinfo = db.titles.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo["lootbag"] == 0 or userinfo["lootbag"] < 0:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nocrates"]["translation"], color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if userinfo["keys"] == 0 or userinfo["keys"] < 0:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nokeys"]["translation"], color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if len(userinfo["inventory"]) >= 24:
			try:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["general"]["fullinv"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			except:
				return
			return

		userinfo["keys"] = userinfo["keys"] - 1
		userinfo["lootbag"] = userinfo["lootbag"] - 1
		em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening"]["translation"].format(userinfo["name"]), color=discord.Colour(0xffffff))
		await ctx.send(embed=em)

		await asyncio.sleep(4)

		goldmul = random.randint(12, 28)
		goldgain = goldmul * 3 + userinfo["lvl"]
		chance = random.randint(1, 1000)
		legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor"])
		rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])

		if legendary == "Excalibur":
			legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

		if legendary == "Twilight":
			legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

		if legendary == "Devil's Kiss":
			legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

		if legendary == "Hawkeye":
			legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

		if legendary == "Solarflare":
			legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

		if legendary == "Thunderguard":
			legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

		if legendary == "Doomblade":
			legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

		if legendary == "Deathraze":
			legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

		if legendary == "Soulreaper":
			legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

		if legendary == "Nightstalker Mantle":
			legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "None"}

		if legendary == "Bane Of The Goblin Lord":
			legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "None"}

		if legendary == "Hephaestus Armor":
			legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 30, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "None"}

		if chance > 950:
			userinfo["inventory"].append(legendaryitemobj)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
				except:
					pass

			if "Legendary" in titlesinfo["titles_list"]:
				legendary2title = "Twice Told Legend"
				if not legendary2title in titlesinfo["titles_list"]:
					titlesinfo["titles_list"].append(legendary2title)
					titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
					db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
					em = discord.Embed(title="New Title", description=legendary2title, color=discord.Colour(0x00ff00))
					em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
					try:
						await ctx.send(user, embed=em)
						return
					except:
						await ctx.send(embed=em)
						return

			legendarytitle = "Legendary"
			if not legendarytitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(legendarytitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
				em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
				try:
					await ctx.send(user, embed=em)
					return
				except:
					await ctx.send(embed=em)
					return
			return

		if rare == "Iron Claws":
			rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

		if rare == "Iron Mace":
			rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

		if rare == "Curved Dagger":
			rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

		if rare == "Tomb of Water":
			rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

		if rare == "Spiked Mace":
			rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

		if rare == "Mithril Sword":
			rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

		if rare == "Etched Longbow":
			rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

		if rare == "Verdant Bow":
			rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}


		elif chance < 950 and chance > 600:
			userinfo["inventory"].append(rareitemobj)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare))
			except:
				pass
		else:
			em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
			except:
				pass
				

def setup(bot):
	n = loot(bot)
	bot.add_cog(n)