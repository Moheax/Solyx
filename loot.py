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
	async def crate(self, ctx, amount: int):
		"""say how many crates you want to open!\nlevel 0-99 can open 1 crate\nlevel 100+ can open 2 crates\nlevel 200+ can open 3 crates\npatreons can open more!"""
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has tried opening a crate")

		userinfo = db.users.find_one({ "_id": user.id })
		titlesinfo = db.titles.find_one({ "_id": user.id })

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		if amount == None:
			em = discord.Embed(description="level 0-99 can open 1 crate\nlevel 100+ can open 2 crates\npatreons can open more!", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

		if userinfo["role"] == "Player":
			if amount == 1:
				times = 1

			if amount == 2 and userinfo["lvl"] >= 100:
				times = 2

			if amount == 2 and not userinfo["lvl"] >= 100:
				em = discord.Embed(description="Reach level 100+ to open 2 crates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount == 3 and userinfo["lvl"] >= 200:
				times = 3

			if amount == 3 and not userinfo["lvl"] >= 200:
				em = discord.Embed(description="Reach level 200+ to open 3 crates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if amount >= 4:
				em = discord.Embed(description="You cant open more then 3 crates!\n Become a patreon to open more crates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if userinfo["questname"] == "Unboxing I":
				userinfo["questprogress"] = userinfo["questprogress"] + amount
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				if userinfo["questprogress"] >= 10:
					await ctx.send("Quest Updated!")
				pass

			if userinfo["lootbag"] == 0 or userinfo["lootbag"] < amount:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nocrates"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if userinfo["keys"] == 0 or userinfo["keys"] < amount:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nokeys"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			opening = 27 - times
			if len(userinfo["inventory"]) >= 27 or len(userinfo["inventory"]) >= opening:
				try:
					em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["general"]["fullinv"]["translation"], color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				except:
					return
				return

			
			if amount == 1: 
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening"]["translation"].format(userinfo["name"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			else:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening2"]["translation"].format(userinfo["name"], amount), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)

			await asyncio.sleep(5)

			guildinfo = db.servers.find_one({ "_id": guild.id })
			try:
				if guildinfo["mission"] == "Open 250 lootbags":
					if not guildinfo["mission"] == "Open 250 lootbags":
						pass
				try:
					guildinfo["missionprogress"] = guildinfo["missionprogress"] + amount
					db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
					pass
				except:
					print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
					pass
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				pass

			goldmul = random.randint(12, 28)
			goldgain = goldmul * 3 + userinfo["lvl"]

			# Crate 1
			if amount>= 1:
				await asyncio.sleep(0.6)
				userinfo["keys"] = userinfo["keys"] - 1
				userinfo["lootbag"] = userinfo["lootbag"] - 1
				try:
					chance = random.randint(1, 1000)
					legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
					rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
					common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
					material = randchoice(["Stone", "Metal", "Wood"])


					if legendary == "Excalibur":
						legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

					elif legendary == "Twilight":
						legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

					elif legendary == "Devil's Kiss":
						legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

					elif legendary == "Hawkeye":
						legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

					elif legendary == "Solarflare":
						legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

					elif legendary == "Thunderguard":
						legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

					elif legendary == "Doomblade":
						legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

					elif legendary == "Deathraze":
						legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

					elif legendary == "Soulreaper":
						legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

					elif legendary == "Nightstalker Mantle":
						legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

					elif legendary == "Bane Of The Goblin Lord":
						legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

					elif legendary == "Hephaestus Armor":
						legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

					if chance > 990:
			
						if legendary == "exp":
							expgained = random.randint(1, 3)
							userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						userinfo["inventory"].append(legendaryitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
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
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

						legendarytitle = "Legendary"
						if not legendarytitle in titlesinfo["titles_list"]:
							titlesinfo["titles_list"].append(legendarytitle)
							titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
							db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
							em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
							em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
							try:
								await ctx.send(user, embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass
						return

					if rare == "Iron Claws":
						rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

					elif rare == "Iron Mace":
						rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

					elif rare == "Curved Dagger":
						rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

					elif rare == "Tomb of Water":
						rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

					elif rare == "Spiked Mace":
						rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

					elif rare == "Mithril Sword":
						rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

					elif rare == "Etched Longbow":
						rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

					elif rare == "Verdant Bow":
						rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

					elif rare == "Iron Armor":
						rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Branded Metal Armor":
						rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Wolf Fur":
						rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Enchanted Steel Armor":
						rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


					if chance < 950 and chance > 700:
						userinfo["inventory"].append(rareitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							pass
						except:
							userinfo["keys"] = userinfo["keys"] + 1
							userinfo["lootbag"] = userinfo["lootbag"] + 1
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
							em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
							await ctx.send(embed=em)
							pass

					if common == "Sclerite Sword":
						commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

					elif common == "Iron Greatsword":
						commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

					elif common == "Abaddon Dagger":
						commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

					elif common == "Rusted Short Sword":
						commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

					elif common == "Makeshift Shortbow":
						commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

					elif common == "Obsidian Longbow":
						commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

					elif common == "Concealed Blade":
						commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

					elif common == "Tomb of Fire":
						commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

					elif common == "Scroll of Blizzards":
						commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

					elif common ==  "Glyphic Bow":
						commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

					elif common == "Oblivion":
						commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

					elif common == "Staff of Milos":
						commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

					elif common == "Calcite Staff":
						commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

					elif common == "Leather Armor":
						commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Banded Armor":
						commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Pit Fighter Armor":
						commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Chainmail Armor":
						commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Barbaric Armor":
						commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

					if chance < 700 and chance > 300:

						userinfo["inventory"].append(commonitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							pass
						except:
							userinfo["keys"] = userinfo["keys"] + 1
							userinfo["lootbag"] = userinfo["lootbag"] + 1
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
							em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
							await ctx.send(embed=em)
						pass


					if chance < 300 and chance > 50:

						if material == "Stone":
							mined_stone = random.randint(1, 5)
							userinfo["stone"] = userinfo["stone"] + mined_stone
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						elif material == "Metal":
							mined_metal= random.randint(1, 2)
							userinfo["metal"] = userinfo["metal"] + mined_metal
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						elif material == "Wood":
							chopped = random.randint(1, 5)
							userinfo["wood"] = userinfo["wood"] + chopped
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

					
						
				except:
					em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
					try:
						await ctx.send(embed=em)
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						except:
							pass
					pass
				if amount>= 2:
					await asyncio.sleep(0.6)
					userinfo["keys"] = userinfo["keys"] - 1
					userinfo["lootbag"] = userinfo["lootbag"] - 1
					try:
						chance = random.randint(1, 1000)
						legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
						rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
						common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
						material = randchoice(["Stone", "Metal", "Wood"])


						if legendary == "Excalibur":
							legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

						elif legendary == "Twilight":
							legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

						elif legendary == "Devil's Kiss":
							legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

						elif legendary == "Hawkeye":
							legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

						elif legendary == "Solarflare":
							legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

						elif legendary == "Thunderguard":
							legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

						elif legendary == "Doomblade":
							legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

						elif legendary == "Deathraze":
							legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

						elif legendary == "Soulreaper":
							legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

						elif legendary == "Nightstalker Mantle":
							legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

						elif legendary == "Bane Of The Goblin Lord":
							legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

						elif legendary == "Hephaestus Armor":
							legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

						if chance > 990:
			
							if legendary == "exp":
								expgained = random.randint(1, 3)
								userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							userinfo["inventory"].append(legendaryitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
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
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

							legendarytitle = "Legendary"
							if not legendarytitle in titlesinfo["titles_list"]:
								titlesinfo["titles_list"].append(legendarytitle)
								titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
								db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
								em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
								em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
								try:
									await ctx.send(user, embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass
							return

						if rare == "Iron Claws":
							rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

						elif rare == "Iron Mace":
							rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

						elif rare == "Curved Dagger":
							rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

						elif rare == "Tomb of Water":
							rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

						elif rare == "Spiked Mace":
							rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

						elif rare == "Mithril Sword":
							rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

						elif rare == "Etched Longbow":
							rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

						elif rare == "Verdant Bow":
							rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

						elif rare == "Iron Armor":
							rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Branded Metal Armor":
							rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Wolf Fur":
							rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Enchanted Steel Armor":
							rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


						if chance < 950 and chance > 700:
							userinfo["inventory"].append(rareitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						if common == "Sclerite Sword":
							commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

						elif common == "Iron Greatsword":
							commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

						elif common == "Abaddon Dagger":
							commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

						elif common == "Rusted Short Sword":
							commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

						elif common == "Makeshift Shortbow":
							commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

						elif common == "Obsidian Longbow":
							commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

						elif common == "Concealed Blade":
							commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

						elif common == "Tomb of Fire":
							commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

						elif common == "Scroll of Blizzards":
							commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

						elif common ==  "Glyphic Bow":
							commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

						elif common == "Oblivion":
							commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

						elif common == "Staff of Milos":
							commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

						elif common == "Calcite Staff":
							commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

						elif common == "Leather Armor":
							commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Banded Armor":
							commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Pit Fighter Armor":
							commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Chainmail Armor":
							commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Barbaric Armor":
							commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

						if chance < 700 and chance > 300:

							userinfo["inventory"].append(commonitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
							pass


						if chance < 300 and chance > 50:

							if material == "Stone":
								mined_stone = random.randint(1, 5)
								userinfo["stone"] = userinfo["stone"] + mined_stone
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							elif material == "Metal":
								mined_metal= random.randint(1, 2)
								userinfo["metal"] = userinfo["metal"] + mined_metal
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							elif material == "Wood":
								chopped = random.randint(1, 5)
								userinfo["wood"] = userinfo["wood"] + chopped
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

					
						
					except:
						em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							except:
								pass
						pass
					if amount>= 3:
						await asyncio.sleep(0.6)
						userinfo["keys"] = userinfo["keys"] - 1
						userinfo["lootbag"] = userinfo["lootbag"] - 1
						try:
							chance = random.randint(1, 1000)
							legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
							rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
							common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
							material = randchoice(["Stone", "Metal", "Wood"])


							if legendary == "Excalibur":
								legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

							elif legendary == "Twilight":
								legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

							elif legendary == "Devil's Kiss":
								legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

							elif legendary == "Hawkeye":
								legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

							elif legendary == "Solarflare":
								legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

							elif legendary == "Thunderguard":
								legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

							elif legendary == "Doomblade":
								legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

							elif legendary == "Deathraze":
								legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

							elif legendary == "Soulreaper":
								legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

							elif legendary == "Nightstalker Mantle":
								legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

							elif legendary == "Bane Of The Goblin Lord":
								legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

							elif legendary == "Hephaestus Armor":
								legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

							if chance > 990:
			
								if legendary == "exp":
									expgained = random.randint(1, 3)
									userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								userinfo["inventory"].append(legendaryitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
								except:
									try:
										await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
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
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

								legendarytitle = "Legendary"
								if not legendarytitle in titlesinfo["titles_list"]:
									titlesinfo["titles_list"].append(legendarytitle)
									titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
									db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
									em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
									em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
									try:
										await ctx.send(user, embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass
								return

							if rare == "Iron Claws":
								rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

							elif rare == "Iron Mace":
								rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

							elif rare == "Curved Dagger":
								rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

							elif rare == "Tomb of Water":
								rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

							elif rare == "Spiked Mace":
								rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

							elif rare == "Mithril Sword":
								rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

							elif rare == "Etched Longbow":
								rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

							elif rare == "Verdant Bow":
								rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

							elif rare == "Iron Armor":
								rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Branded Metal Armor":
								rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Wolf Fur":
								rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Enchanted Steel Armor":
								rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


							if chance < 950 and chance > 700:
								userinfo["inventory"].append(rareitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							if common == "Sclerite Sword":
								commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

							elif common == "Iron Greatsword":
								commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

							elif common == "Abaddon Dagger":
								commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

							elif common == "Rusted Short Sword":
								commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

							elif common == "Makeshift Shortbow":
								commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

							elif common == "Obsidian Longbow":
								commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

							elif common == "Concealed Blade":
								commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

							elif common == "Tomb of Fire":
								commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

							elif common == "Scroll of Blizzards":
								commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

							elif common ==  "Glyphic Bow":
								commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

							elif common == "Oblivion":
								commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

							elif common == "Staff of Milos":
								commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

							elif common == "Calcite Staff":
								commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

							elif common == "Leather Armor":
								commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Banded Armor":
								commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Pit Fighter Armor":
								commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Chainmail Armor":
								commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Barbaric Armor":
								commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

							if chance < 700 and chance > 300:

								userinfo["inventory"].append(commonitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
								pass


							if chance < 300 and chance > 50:

								if material == "Stone":
									mined_stone = random.randint(1, 5)
									userinfo["stone"] = userinfo["stone"] + mined_stone
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								elif material == "Metal":
									mined_metal= random.randint(1, 2)
									userinfo["metal"] = userinfo["metal"] + mined_metal
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								elif material == "Wood":
									chopped = random.randint(1, 5)
									userinfo["wood"] = userinfo["wood"] + chopped
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

					
						
						except:
							em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								except:
									pass
							pass




		elif userinfo["role"] == "patreon1" or userinfo["role"] == "Developer":

			times = amount

			if amount >= 3:
				em = discord.Embed(description="You cant open more then 3 crates!\n Become a higher tier patreon to open more crates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if userinfo["questname"] == "Unboxing I":
				userinfo["questprogress"] = userinfo["questprogress"] + amount
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				if userinfo["questprogress"] >= 10:
					await ctx.send("Quest Updated!")
				pass

			if userinfo["lootbag"] == 0 or userinfo["lootbag"] < amount:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nocrates"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if userinfo["keys"] == 0 or userinfo["keys"] < amount:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nokeys"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			opening = 27 - times
			if len(userinfo["inventory"]) >= 27 or len(userinfo["inventory"]) >= opening:
				try:
					em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["general"]["fullinv"]["translation"], color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				except:
					return
				return



			if amount == 1: 
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening"]["translation"].format(userinfo["name"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			else:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening2"]["translation"].format(userinfo["name"], amount), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)

			await asyncio.sleep(5)

			guildinfo = db.servers.find_one({ "_id": guild.id })
			try:
				if guildinfo["mission"] == "Open 250 lootbags":
					if not guildinfo["mission"] == "Open 250 lootbags":
						pass
				try:
					guildinfo["missionprogress"] = guildinfo["missionprogress"] + amount
					db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
					pass
				except:
					print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
					pass
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				pass

			goldmul = random.randint(12, 28)
			goldgain = goldmul * 3 + userinfo["lvl"]
			
			# Crate 1
	# Crate 1
			if amount>= 1:
				await asyncio.sleep(0.6)
				userinfo["keys"] = userinfo["keys"] - 1
				userinfo["lootbag"] = userinfo["lootbag"] - 1
				try:
					chance = random.randint(1, 1000)
					legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
					rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
					common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
					material = randchoice(["Stone", "Metal", "Wood"])


					if legendary == "Excalibur":
						legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

					elif legendary == "Twilight":
						legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

					elif legendary == "Devil's Kiss":
						legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

					elif legendary == "Hawkeye":
						legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

					elif legendary == "Solarflare":
						legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

					elif legendary == "Thunderguard":
						legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

					elif legendary == "Doomblade":
						legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

					elif legendary == "Deathraze":
						legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

					elif legendary == "Soulreaper":
						legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

					elif legendary == "Nightstalker Mantle":
						legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

					elif legendary == "Bane Of The Goblin Lord":
						legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

					elif legendary == "Hephaestus Armor":
						legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

					if chance > 990:
			
						if legendary == "exp":
							expgained = random.randint(1, 3)
							userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						userinfo["inventory"].append(legendaryitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
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
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

						legendarytitle = "Legendary"
						if not legendarytitle in titlesinfo["titles_list"]:
							titlesinfo["titles_list"].append(legendarytitle)
							titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
							db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
							em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
							em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
							try:
								await ctx.send(user, embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass
						return

					if rare == "Iron Claws":
						rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

					elif rare == "Iron Mace":
						rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

					elif rare == "Curved Dagger":
						rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

					elif rare == "Tomb of Water":
						rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

					elif rare == "Spiked Mace":
						rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

					elif rare == "Mithril Sword":
						rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

					elif rare == "Etched Longbow":
						rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

					elif rare == "Verdant Bow":
						rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

					elif rare == "Iron Armor":
						rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Branded Metal Armor":
						rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Wolf Fur":
						rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Enchanted Steel Armor":
						rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


					if chance < 950 and chance > 700:
						userinfo["inventory"].append(rareitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							pass
						except:
							userinfo["keys"] = userinfo["keys"] + 1
							userinfo["lootbag"] = userinfo["lootbag"] + 1
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
							em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
							await ctx.send(embed=em)
							pass

					if common == "Sclerite Sword":
						commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

					elif common == "Iron Greatsword":
						commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

					elif common == "Abaddon Dagger":
						commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

					elif common == "Rusted Short Sword":
						commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

					elif common == "Makeshift Shortbow":
						commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

					elif common == "Obsidian Longbow":
						commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

					elif common == "Concealed Blade":
						commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

					elif common == "Tomb of Fire":
						commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

					elif common == "Scroll of Blizzards":
						commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

					elif common ==  "Glyphic Bow":
						commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

					elif common == "Oblivion":
						commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

					elif common == "Staff of Milos":
						commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

					elif common == "Calcite Staff":
						commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

					elif common == "Leather Armor":
						commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Banded Armor":
						commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Pit Fighter Armor":
						commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Chainmail Armor":
						commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Barbaric Armor":
						commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

					if chance < 700 and chance > 300:

						userinfo["inventory"].append(commonitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							pass
						except:
							userinfo["keys"] = userinfo["keys"] + 1
							userinfo["lootbag"] = userinfo["lootbag"] + 1
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
							em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
							await ctx.send(embed=em)
						pass


					if chance < 300 and chance > 50:

						if material == "Stone":
							mined_stone = random.randint(1, 5)
							userinfo["stone"] = userinfo["stone"] + mined_stone
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						elif material == "Metal":
							mined_metal= random.randint(1, 2)
							userinfo["metal"] = userinfo["metal"] + mined_metal
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						elif material == "Wood":
							chopped = random.randint(1, 5)
							userinfo["wood"] = userinfo["wood"] + chopped
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

					
						
				except:
					em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
					try:
						await ctx.send(embed=em)
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						except:
							pass
					pass
				if amount>= 2:
					await asyncio.sleep(0.6)
					userinfo["keys"] = userinfo["keys"] - 1
					userinfo["lootbag"] = userinfo["lootbag"] - 1
					try:
						chance = random.randint(1, 1000)
						legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
						rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
						common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
						material = randchoice(["Stone", "Metal", "Wood"])


						if legendary == "Excalibur":
							legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

						elif legendary == "Twilight":
							legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

						elif legendary == "Devil's Kiss":
							legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

						elif legendary == "Hawkeye":
							legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

						elif legendary == "Solarflare":
							legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

						elif legendary == "Thunderguard":
							legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

						elif legendary == "Doomblade":
							legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

						elif legendary == "Deathraze":
							legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

						elif legendary == "Soulreaper":
							legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

						elif legendary == "Nightstalker Mantle":
							legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

						elif legendary == "Bane Of The Goblin Lord":
							legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

						elif legendary == "Hephaestus Armor":
							legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

						if chance > 990:
			
							if legendary == "exp":
								expgained = random.randint(1, 3)
								userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							userinfo["inventory"].append(legendaryitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
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
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

							legendarytitle = "Legendary"
							if not legendarytitle in titlesinfo["titles_list"]:
								titlesinfo["titles_list"].append(legendarytitle)
								titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
								db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
								em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
								em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
								try:
									await ctx.send(user, embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass
							return

						if rare == "Iron Claws":
							rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

						elif rare == "Iron Mace":
							rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

						elif rare == "Curved Dagger":
							rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

						elif rare == "Tomb of Water":
							rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

						elif rare == "Spiked Mace":
							rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

						elif rare == "Mithril Sword":
							rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

						elif rare == "Etched Longbow":
							rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

						elif rare == "Verdant Bow":
							rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

						elif rare == "Iron Armor":
							rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Branded Metal Armor":
							rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Wolf Fur":
							rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Enchanted Steel Armor":
							rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


						if chance < 950 and chance > 700:
							userinfo["inventory"].append(rareitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						if common == "Sclerite Sword":
							commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

						elif common == "Iron Greatsword":
							commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

						elif common == "Abaddon Dagger":
							commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

						elif common == "Rusted Short Sword":
							commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

						elif common == "Makeshift Shortbow":
							commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

						elif common == "Obsidian Longbow":
							commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

						elif common == "Concealed Blade":
							commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

						elif common == "Tomb of Fire":
							commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

						elif common == "Scroll of Blizzards":
							commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

						elif common ==  "Glyphic Bow":
							commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

						elif common == "Oblivion":
							commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

						elif common == "Staff of Milos":
							commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

						elif common == "Calcite Staff":
							commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

						elif common == "Leather Armor":
							commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Banded Armor":
							commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Pit Fighter Armor":
							commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Chainmail Armor":
							commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Barbaric Armor":
							commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

						if chance < 700 and chance > 300:

							userinfo["inventory"].append(commonitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
							pass


						if chance < 300 and chance > 50:

							if material == "Stone":
								mined_stone = random.randint(1, 5)
								userinfo["stone"] = userinfo["stone"] + mined_stone
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							elif material == "Metal":
								mined_metal= random.randint(1, 2)
								userinfo["metal"] = userinfo["metal"] + mined_metal
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							elif material == "Wood":
								chopped = random.randint(1, 5)
								userinfo["wood"] = userinfo["wood"] + chopped
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

					
						
					except:
						em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							except:
								pass
						pass
					if amount>= 3:
						await asyncio.sleep(0.6)
						userinfo["keys"] = userinfo["keys"] - 1
						userinfo["lootbag"] = userinfo["lootbag"] - 1
						try:
							chance = random.randint(1, 1000)
							legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
							rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
							common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
							material = randchoice(["Stone", "Metal", "Wood"])


							if legendary == "Excalibur":
								legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

							elif legendary == "Twilight":
								legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

							elif legendary == "Devil's Kiss":
								legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

							elif legendary == "Hawkeye":
								legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

							elif legendary == "Solarflare":
								legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

							elif legendary == "Thunderguard":
								legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

							elif legendary == "Doomblade":
								legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

							elif legendary == "Deathraze":
								legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

							elif legendary == "Soulreaper":
								legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

							elif legendary == "Nightstalker Mantle":
								legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

							elif legendary == "Bane Of The Goblin Lord":
								legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

							elif legendary == "Hephaestus Armor":
								legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

							if chance > 990:
			
								if legendary == "exp":
									expgained = random.randint(1, 3)
									userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								userinfo["inventory"].append(legendaryitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
								except:
									try:
										await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
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
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

								legendarytitle = "Legendary"
								if not legendarytitle in titlesinfo["titles_list"]:
									titlesinfo["titles_list"].append(legendarytitle)
									titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
									db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
									em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
									em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
									try:
										await ctx.send(user, embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass
								return

							if rare == "Iron Claws":
								rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

							elif rare == "Iron Mace":
								rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

							elif rare == "Curved Dagger":
								rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

							elif rare == "Tomb of Water":
								rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

							elif rare == "Spiked Mace":
								rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

							elif rare == "Mithril Sword":
								rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

							elif rare == "Etched Longbow":
								rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

							elif rare == "Verdant Bow":
								rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

							elif rare == "Iron Armor":
								rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Branded Metal Armor":
								rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Wolf Fur":
								rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Enchanted Steel Armor":
								rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


							if chance < 950 and chance > 700:
								userinfo["inventory"].append(rareitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							if common == "Sclerite Sword":
								commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

							elif common == "Iron Greatsword":
								commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

							elif common == "Abaddon Dagger":
								commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

							elif common == "Rusted Short Sword":
								commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

							elif common == "Makeshift Shortbow":
								commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

							elif common == "Obsidian Longbow":
								commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

							elif common == "Concealed Blade":
								commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

							elif common == "Tomb of Fire":
								commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

							elif common == "Scroll of Blizzards":
								commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

							elif common ==  "Glyphic Bow":
								commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

							elif common == "Oblivion":
								commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

							elif common == "Staff of Milos":
								commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

							elif common == "Calcite Staff":
								commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

							elif common == "Leather Armor":
								commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Banded Armor":
								commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Pit Fighter Armor":
								commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Chainmail Armor":
								commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Barbaric Armor":
								commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

							if chance < 700 and chance > 300:

								userinfo["inventory"].append(commonitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
								pass


							if chance < 300 and chance > 50:

								if material == "Stone":
									mined_stone = random.randint(1, 5)
									userinfo["stone"] = userinfo["stone"] + mined_stone
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								elif material == "Metal":
									mined_metal= random.randint(1, 2)
									userinfo["metal"] = userinfo["metal"] + mined_metal
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								elif material == "Wood":
									chopped = random.randint(1, 5)
									userinfo["wood"] = userinfo["wood"] + chopped
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

					
						
						except:
							em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								except:
									pass
							pass












		elif userinfo["role"] == "patreon2" :

			times = amount

			if amount >= 4:
				em = discord.Embed(description="You cant open more then 3 crates!\n Become a higher tier patreon to open more crates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if userinfo["questname"] == "Unboxing I":
				userinfo["questprogress"] = userinfo["questprogress"] + amount
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				if userinfo["questprogress"] >= 10:
					await ctx.send("Quest Updated!")
				pass

			if userinfo["lootbag"] == 0 or userinfo["lootbag"] < amount:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nocrates"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if userinfo["keys"] == 0 or userinfo["keys"] < amount:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nokeys"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			opening = 27 - times
			if len(userinfo["inventory"]) >= 27 or len(userinfo["inventory"]) >= opening:
				try:
					em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["general"]["fullinv"]["translation"], color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				except:
					return
				return

		

			if amount == 1: 
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening"]["translation"].format(userinfo["name"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			else:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening2"]["translation"].format(userinfo["name"], amount), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)

			await asyncio.sleep(5)

			guildinfo = db.servers.find_one({ "_id": guild.id })
			try:
				if guildinfo["mission"] == "Open 250 lootbags":
					if not guildinfo["mission"] == "Open 250 lootbags":
						pass
				try:
					guildinfo["missionprogress"] = guildinfo["missionprogress"] + amount
					db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
					pass
				except:
					print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
					pass
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				pass

			goldmul = random.randint(12, 28)
			goldgain = goldmul * 3 + userinfo["lvl"]
			
			# Crate 1
	# Crate 1
			if amount>= 1:
				await asyncio.sleep(0.6)
				userinfo["keys"] = userinfo["keys"] - 1
				userinfo["lootbag"] = userinfo["lootbag"] - 1
				try:
					chance = random.randint(1, 1000)
					legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
					rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
					common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
					material = randchoice(["Stone", "Metal", "Wood"])


					if legendary == "Excalibur":
						legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

					elif legendary == "Twilight":
						legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

					elif legendary == "Devil's Kiss":
						legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

					elif legendary == "Hawkeye":
						legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

					elif legendary == "Solarflare":
						legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

					elif legendary == "Thunderguard":
						legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

					elif legendary == "Doomblade":
						legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

					elif legendary == "Deathraze":
						legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

					elif legendary == "Soulreaper":
						legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

					elif legendary == "Nightstalker Mantle":
						legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

					elif legendary == "Bane Of The Goblin Lord":
						legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

					elif legendary == "Hephaestus Armor":
						legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

					if chance > 990:
			
						if legendary == "exp":
							expgained = random.randint(1, 3)
							userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						userinfo["inventory"].append(legendaryitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
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
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

						legendarytitle = "Legendary"
						if not legendarytitle in titlesinfo["titles_list"]:
							titlesinfo["titles_list"].append(legendarytitle)
							titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
							db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
							em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
							em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
							try:
								await ctx.send(user, embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass
						return

					if rare == "Iron Claws":
						rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

					elif rare == "Iron Mace":
						rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

					elif rare == "Curved Dagger":
						rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

					elif rare == "Tomb of Water":
						rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

					elif rare == "Spiked Mace":
						rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

					elif rare == "Mithril Sword":
						rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

					elif rare == "Etched Longbow":
						rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

					elif rare == "Verdant Bow":
						rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

					elif rare == "Iron Armor":
						rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Branded Metal Armor":
						rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Wolf Fur":
						rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Enchanted Steel Armor":
						rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


					if chance < 950 and chance > 700:
						userinfo["inventory"].append(rareitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							pass
						except:
							userinfo["keys"] = userinfo["keys"] + 1
							userinfo["lootbag"] = userinfo["lootbag"] + 1
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
							em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
							await ctx.send(embed=em)
							pass

					if common == "Sclerite Sword":
						commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

					elif common == "Iron Greatsword":
						commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

					elif common == "Abaddon Dagger":
						commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

					elif common == "Rusted Short Sword":
						commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

					elif common == "Makeshift Shortbow":
						commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

					elif common == "Obsidian Longbow":
						commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

					elif common == "Concealed Blade":
						commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

					elif common == "Tomb of Fire":
						commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

					elif common == "Scroll of Blizzards":
						commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

					elif common ==  "Glyphic Bow":
						commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

					elif common == "Oblivion":
						commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

					elif common == "Staff of Milos":
						commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

					elif common == "Calcite Staff":
						commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

					elif common == "Leather Armor":
						commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Banded Armor":
						commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Pit Fighter Armor":
						commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Chainmail Armor":
						commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Barbaric Armor":
						commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

					if chance < 700 and chance > 300:

						userinfo["inventory"].append(commonitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							pass
						except:
							userinfo["keys"] = userinfo["keys"] + 1
							userinfo["lootbag"] = userinfo["lootbag"] + 1
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
							em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
							await ctx.send(embed=em)
						pass


					if chance < 300 and chance > 50:

						if material == "Stone":
							mined_stone = random.randint(1, 5)
							userinfo["stone"] = userinfo["stone"] + mined_stone
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						elif material == "Metal":
							mined_metal= random.randint(1, 2)
							userinfo["metal"] = userinfo["metal"] + mined_metal
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						elif material == "Wood":
							chopped = random.randint(1, 5)
							userinfo["wood"] = userinfo["wood"] + chopped
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

					
						
				except:
					em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
					try:
						await ctx.send(embed=em)
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						except:
							pass
					pass
				if amount>= 2:
					await asyncio.sleep(0.6)
					userinfo["keys"] = userinfo["keys"] - 1
					userinfo["lootbag"] = userinfo["lootbag"] - 1
					try:
						chance = random.randint(1, 1000)
						legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
						rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
						common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
						material = randchoice(["Stone", "Metal", "Wood"])


						if legendary == "Excalibur":
							legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

						elif legendary == "Twilight":
							legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

						elif legendary == "Devil's Kiss":
							legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

						elif legendary == "Hawkeye":
							legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

						elif legendary == "Solarflare":
							legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

						elif legendary == "Thunderguard":
							legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

						elif legendary == "Doomblade":
							legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

						elif legendary == "Deathraze":
							legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

						elif legendary == "Soulreaper":
							legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

						elif legendary == "Nightstalker Mantle":
							legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

						elif legendary == "Bane Of The Goblin Lord":
							legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

						elif legendary == "Hephaestus Armor":
							legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

						if chance > 990:
			
							if legendary == "exp":
								expgained = random.randint(1, 3)
								userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							userinfo["inventory"].append(legendaryitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
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
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

							legendarytitle = "Legendary"
							if not legendarytitle in titlesinfo["titles_list"]:
								titlesinfo["titles_list"].append(legendarytitle)
								titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
								db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
								em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
								em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
								try:
									await ctx.send(user, embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass
							return

						if rare == "Iron Claws":
							rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

						elif rare == "Iron Mace":
							rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

						elif rare == "Curved Dagger":
							rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

						elif rare == "Tomb of Water":
							rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

						elif rare == "Spiked Mace":
							rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

						elif rare == "Mithril Sword":
							rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

						elif rare == "Etched Longbow":
							rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

						elif rare == "Verdant Bow":
							rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

						elif rare == "Iron Armor":
							rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Branded Metal Armor":
							rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Wolf Fur":
							rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Enchanted Steel Armor":
							rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


						if chance < 950 and chance > 700:
							userinfo["inventory"].append(rareitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						if common == "Sclerite Sword":
							commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

						elif common == "Iron Greatsword":
							commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

						elif common == "Abaddon Dagger":
							commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

						elif common == "Rusted Short Sword":
							commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

						elif common == "Makeshift Shortbow":
							commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

						elif common == "Obsidian Longbow":
							commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

						elif common == "Concealed Blade":
							commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

						elif common == "Tomb of Fire":
							commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

						elif common == "Scroll of Blizzards":
							commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

						elif common ==  "Glyphic Bow":
							commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

						elif common == "Oblivion":
							commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

						elif common == "Staff of Milos":
							commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

						elif common == "Calcite Staff":
							commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

						elif common == "Leather Armor":
							commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Banded Armor":
							commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Pit Fighter Armor":
							commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Chainmail Armor":
							commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Barbaric Armor":
							commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

						if chance < 700 and chance > 300:

							userinfo["inventory"].append(commonitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
							pass


						if chance < 300 and chance > 50:

							if material == "Stone":
								mined_stone = random.randint(1, 5)
								userinfo["stone"] = userinfo["stone"] + mined_stone
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							elif material == "Metal":
								mined_metal= random.randint(1, 2)
								userinfo["metal"] = userinfo["metal"] + mined_metal
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							elif material == "Wood":
								chopped = random.randint(1, 5)
								userinfo["wood"] = userinfo["wood"] + chopped
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

					
						
					except:
						em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							except:
								pass
						pass
					if amount>= 3:
						await asyncio.sleep(0.6)
						userinfo["keys"] = userinfo["keys"] - 1
						userinfo["lootbag"] = userinfo["lootbag"] - 1
						try:
							chance = random.randint(1, 1000)
							legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
							rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
							common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
							material = randchoice(["Stone", "Metal", "Wood"])


							if legendary == "Excalibur":
								legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

							elif legendary == "Twilight":
								legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

							elif legendary == "Devil's Kiss":
								legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

							elif legendary == "Hawkeye":
								legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

							elif legendary == "Solarflare":
								legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

							elif legendary == "Thunderguard":
								legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

							elif legendary == "Doomblade":
								legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

							elif legendary == "Deathraze":
								legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

							elif legendary == "Soulreaper":
								legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

							elif legendary == "Nightstalker Mantle":
								legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

							elif legendary == "Bane Of The Goblin Lord":
								legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

							elif legendary == "Hephaestus Armor":
								legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

							if chance > 990:
			
								if legendary == "exp":
									expgained = random.randint(1, 3)
									userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								userinfo["inventory"].append(legendaryitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
								except:
									try:
										await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
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
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

								legendarytitle = "Legendary"
								if not legendarytitle in titlesinfo["titles_list"]:
									titlesinfo["titles_list"].append(legendarytitle)
									titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
									db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
									em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
									em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
									try:
										await ctx.send(user, embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass
								return

							if rare == "Iron Claws":
								rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

							elif rare == "Iron Mace":
								rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

							elif rare == "Curved Dagger":
								rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

							elif rare == "Tomb of Water":
								rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

							elif rare == "Spiked Mace":
								rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

							elif rare == "Mithril Sword":
								rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

							elif rare == "Etched Longbow":
								rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

							elif rare == "Verdant Bow":
								rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

							elif rare == "Iron Armor":
								rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Branded Metal Armor":
								rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Wolf Fur":
								rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Enchanted Steel Armor":
								rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


							if chance < 950 and chance > 700:
								userinfo["inventory"].append(rareitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							if common == "Sclerite Sword":
								commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

							elif common == "Iron Greatsword":
								commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

							elif common == "Abaddon Dagger":
								commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

							elif common == "Rusted Short Sword":
								commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

							elif common == "Makeshift Shortbow":
								commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

							elif common == "Obsidian Longbow":
								commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

							elif common == "Concealed Blade":
								commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

							elif common == "Tomb of Fire":
								commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

							elif common == "Scroll of Blizzards":
								commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

							elif common ==  "Glyphic Bow":
								commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

							elif common == "Oblivion":
								commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

							elif common == "Staff of Milos":
								commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

							elif common == "Calcite Staff":
								commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

							elif common == "Leather Armor":
								commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Banded Armor":
								commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Pit Fighter Armor":
								commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Chainmail Armor":
								commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Barbaric Armor":
								commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

							if chance < 700 and chance > 300:

								userinfo["inventory"].append(commonitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
								pass


							if chance < 300 and chance > 50:

								if material == "Stone":
									mined_stone = random.randint(1, 5)
									userinfo["stone"] = userinfo["stone"] + mined_stone
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								elif material == "Metal":
									mined_metal= random.randint(1, 2)
									userinfo["metal"] = userinfo["metal"] + mined_metal
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								elif material == "Wood":
									chopped = random.randint(1, 5)
									userinfo["wood"] = userinfo["wood"] + chopped
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

					
						
						except:
							em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								except:
									pass
							pass











		elif userinfo["role"] == "patreon3":

			times = amount

			if amount >= 5:
				em = discord.Embed(description="You cant open more then 4 crates!\n Become a higher tier patreon to open more crates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if userinfo["questname"] == "Unboxing I":
				userinfo["questprogress"] = userinfo["questprogress"] + amount
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				if userinfo["questprogress"] >= 10:
					await ctx.send("Quest Updated!")
				pass

			if userinfo["lootbag"] == 0 or userinfo["lootbag"] < amount:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nocrates"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if userinfo["keys"] == 0 or userinfo["keys"] < amount:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nokeys"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			opening = 27 - times
			if len(userinfo["inventory"]) >= 27 or len(userinfo["inventory"]) >= opening:
				try:
					em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["general"]["fullinv"]["translation"], color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				except:
					return
				return

	

			if amount == 1: 
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening"]["translation"].format(userinfo["name"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			else:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening2"]["translation"].format(userinfo["name"], amount), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)

			await asyncio.sleep(5)

			guildinfo = db.servers.find_one({ "_id": guild.id })
			try:
				if guildinfo["mission"] == "Open 250 lootbags":
					if not guildinfo["mission"] == "Open 250 lootbags":
						pass
				try:
					guildinfo["missionprogress"] = guildinfo["missionprogress"] + amount
					db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
					pass
				except:
					print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
					pass
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				pass

			goldmul = random.randint(12, 28)
			goldgain = goldmul * 3 + userinfo["lvl"]
				# Crate 1
			if amount>= 1:
				await asyncio.sleep(0.6)
				userinfo["keys"] = userinfo["keys"] - 1
				userinfo["lootbag"] = userinfo["lootbag"] - 1
				try:
					chance = random.randint(1, 1000)
					legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
					rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
					common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
					material = randchoice(["Stone", "Metal", "Wood"])


					if legendary == "Excalibur":
						legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

					elif legendary == "Twilight":
						legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

					elif legendary == "Devil's Kiss":
						legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

					elif legendary == "Hawkeye":
						legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

					elif legendary == "Solarflare":
						legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

					elif legendary == "Thunderguard":
						legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

					elif legendary == "Doomblade":
						legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

					elif legendary == "Deathraze":
						legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

					elif legendary == "Soulreaper":
						legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

					elif legendary == "Nightstalker Mantle":
						legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

					elif legendary == "Bane Of The Goblin Lord":
						legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

					elif legendary == "Hephaestus Armor":
						legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

					if chance > 990:
			
						if legendary == "exp":
							expgained = random.randint(1, 3)
							userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						userinfo["inventory"].append(legendaryitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
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
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

						legendarytitle = "Legendary"
						if not legendarytitle in titlesinfo["titles_list"]:
							titlesinfo["titles_list"].append(legendarytitle)
							titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
							db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
							em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
							em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
							try:
								await ctx.send(user, embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass
						return

					if rare == "Iron Claws":
						rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

					elif rare == "Iron Mace":
						rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

					elif rare == "Curved Dagger":
						rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

					elif rare == "Tomb of Water":
						rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

					elif rare == "Spiked Mace":
						rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

					elif rare == "Mithril Sword":
						rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

					elif rare == "Etched Longbow":
						rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

					elif rare == "Verdant Bow":
						rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

					elif rare == "Iron Armor":
						rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Branded Metal Armor":
						rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Wolf Fur":
						rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Enchanted Steel Armor":
						rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


					if chance < 950 and chance > 700:
						userinfo["inventory"].append(rareitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							pass
						except:
							userinfo["keys"] = userinfo["keys"] + 1
							userinfo["lootbag"] = userinfo["lootbag"] + 1
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
							em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
							await ctx.send(embed=em)
							pass

					if common == "Sclerite Sword":
						commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

					elif common == "Iron Greatsword":
						commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

					elif common == "Abaddon Dagger":
						commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

					elif common == "Rusted Short Sword":
						commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

					elif common == "Makeshift Shortbow":
						commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

					elif common == "Obsidian Longbow":
						commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

					elif common == "Concealed Blade":
						commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

					elif common == "Tomb of Fire":
						commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

					elif common == "Scroll of Blizzards":
						commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

					elif common ==  "Glyphic Bow":
						commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

					elif common == "Oblivion":
						commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

					elif common == "Staff of Milos":
						commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

					elif common == "Calcite Staff":
						commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

					elif common == "Leather Armor":
						commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Banded Armor":
						commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Pit Fighter Armor":
						commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Chainmail Armor":
						commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Barbaric Armor":
						commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

					if chance < 700 and chance > 300:

						userinfo["inventory"].append(commonitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							pass
						except:
							userinfo["keys"] = userinfo["keys"] + 1
							userinfo["lootbag"] = userinfo["lootbag"] + 1
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
							em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
							await ctx.send(embed=em)
						pass


					if chance < 300 and chance > 50:

						if material == "Stone":
							mined_stone = random.randint(1, 5)
							userinfo["stone"] = userinfo["stone"] + mined_stone
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						elif material == "Metal":
							mined_metal= random.randint(1, 2)
							userinfo["metal"] = userinfo["metal"] + mined_metal
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						elif material == "Wood":
							chopped = random.randint(1, 5)
							userinfo["wood"] = userinfo["wood"] + chopped
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

					
						
				except:
					em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
					try:
						await ctx.send(embed=em)
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						except:
							pass
					pass
				if amount>= 2:
					await asyncio.sleep(0.6)
					userinfo["keys"] = userinfo["keys"] - 1
					userinfo["lootbag"] = userinfo["lootbag"] - 1
					try:
						chance = random.randint(1, 1000)
						legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
						rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
						common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
						material = randchoice(["Stone", "Metal", "Wood"])


						if legendary == "Excalibur":
							legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

						elif legendary == "Twilight":
							legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

						elif legendary == "Devil's Kiss":
							legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

						elif legendary == "Hawkeye":
							legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

						elif legendary == "Solarflare":
							legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

						elif legendary == "Thunderguard":
							legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

						elif legendary == "Doomblade":
							legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

						elif legendary == "Deathraze":
							legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

						elif legendary == "Soulreaper":
							legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

						elif legendary == "Nightstalker Mantle":
							legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

						elif legendary == "Bane Of The Goblin Lord":
							legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

						elif legendary == "Hephaestus Armor":
							legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

						if chance > 990:
			
							if legendary == "exp":
								expgained = random.randint(1, 3)
								userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							userinfo["inventory"].append(legendaryitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
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
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

							legendarytitle = "Legendary"
							if not legendarytitle in titlesinfo["titles_list"]:
								titlesinfo["titles_list"].append(legendarytitle)
								titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
								db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
								em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
								em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
								try:
									await ctx.send(user, embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass
							return

						if rare == "Iron Claws":
							rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

						elif rare == "Iron Mace":
							rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

						elif rare == "Curved Dagger":
							rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

						elif rare == "Tomb of Water":
							rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

						elif rare == "Spiked Mace":
							rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

						elif rare == "Mithril Sword":
							rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

						elif rare == "Etched Longbow":
							rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

						elif rare == "Verdant Bow":
							rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

						elif rare == "Iron Armor":
							rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Branded Metal Armor":
							rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Wolf Fur":
							rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Enchanted Steel Armor":
							rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


						if chance < 950 and chance > 700:
							userinfo["inventory"].append(rareitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						if common == "Sclerite Sword":
							commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

						elif common == "Iron Greatsword":
							commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

						elif common == "Abaddon Dagger":
							commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

						elif common == "Rusted Short Sword":
							commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

						elif common == "Makeshift Shortbow":
							commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

						elif common == "Obsidian Longbow":
							commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

						elif common == "Concealed Blade":
							commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

						elif common == "Tomb of Fire":
							commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

						elif common == "Scroll of Blizzards":
							commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

						elif common ==  "Glyphic Bow":
							commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

						elif common == "Oblivion":
							commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

						elif common == "Staff of Milos":
							commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

						elif common == "Calcite Staff":
							commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

						elif common == "Leather Armor":
							commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Banded Armor":
							commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Pit Fighter Armor":
							commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Chainmail Armor":
							commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Barbaric Armor":
							commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

						if chance < 700 and chance > 300:

							userinfo["inventory"].append(commonitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
							pass


						if chance < 300 and chance > 50:

							if material == "Stone":
								mined_stone = random.randint(1, 5)
								userinfo["stone"] = userinfo["stone"] + mined_stone
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							elif material == "Metal":
								mined_metal= random.randint(1, 2)
								userinfo["metal"] = userinfo["metal"] + mined_metal
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							elif material == "Wood":
								chopped = random.randint(1, 5)
								userinfo["wood"] = userinfo["wood"] + chopped
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

					
						
					except:
						em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							except:
								pass
						pass
					if amount>= 3:
						await asyncio.sleep(0.6)
						userinfo["keys"] = userinfo["keys"] - 1
						userinfo["lootbag"] = userinfo["lootbag"] - 1
						try:
							chance = random.randint(1, 1000)
							legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
							rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
							common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
							material = randchoice(["Stone", "Metal", "Wood"])


							if legendary == "Excalibur":
								legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

							elif legendary == "Twilight":
								legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

							elif legendary == "Devil's Kiss":
								legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

							elif legendary == "Hawkeye":
								legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

							elif legendary == "Solarflare":
								legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

							elif legendary == "Thunderguard":
								legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

							elif legendary == "Doomblade":
								legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

							elif legendary == "Deathraze":
								legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

							elif legendary == "Soulreaper":
								legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

							elif legendary == "Nightstalker Mantle":
								legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

							elif legendary == "Bane Of The Goblin Lord":
								legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

							elif legendary == "Hephaestus Armor":
								legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

							if chance > 990:
			
								if legendary == "exp":
									expgained = random.randint(1, 3)
									userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								userinfo["inventory"].append(legendaryitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
								except:
									try:
										await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
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
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

								legendarytitle = "Legendary"
								if not legendarytitle in titlesinfo["titles_list"]:
									titlesinfo["titles_list"].append(legendarytitle)
									titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
									db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
									em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
									em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
									try:
										await ctx.send(user, embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass
								return

							if rare == "Iron Claws":
								rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

							elif rare == "Iron Mace":
								rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

							elif rare == "Curved Dagger":
								rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

							elif rare == "Tomb of Water":
								rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

							elif rare == "Spiked Mace":
								rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

							elif rare == "Mithril Sword":
								rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

							elif rare == "Etched Longbow":
								rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

							elif rare == "Verdant Bow":
								rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

							elif rare == "Iron Armor":
								rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Branded Metal Armor":
								rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Wolf Fur":
								rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Enchanted Steel Armor":
								rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


							if chance < 950 and chance > 700:
								userinfo["inventory"].append(rareitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							if common == "Sclerite Sword":
								commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

							elif common == "Iron Greatsword":
								commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

							elif common == "Abaddon Dagger":
								commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

							elif common == "Rusted Short Sword":
								commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

							elif common == "Makeshift Shortbow":
								commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

							elif common == "Obsidian Longbow":
								commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

							elif common == "Concealed Blade":
								commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

							elif common == "Tomb of Fire":
								commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

							elif common == "Scroll of Blizzards":
								commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

							elif common ==  "Glyphic Bow":
								commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

							elif common == "Oblivion":
								commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

							elif common == "Staff of Milos":
								commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

							elif common == "Calcite Staff":
								commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

							elif common == "Leather Armor":
								commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Banded Armor":
								commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Pit Fighter Armor":
								commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Chainmail Armor":
								commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Barbaric Armor":
								commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

							if chance < 700 and chance > 300:

								userinfo["inventory"].append(commonitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
								pass


							if chance < 300 and chance > 50:

								if material == "Stone":
									mined_stone = random.randint(1, 5)
									userinfo["stone"] = userinfo["stone"] + mined_stone
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								elif material == "Metal":
									mined_metal= random.randint(1, 2)
									userinfo["metal"] = userinfo["metal"] + mined_metal
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								elif material == "Wood":
									chopped = random.randint(1, 5)
									userinfo["wood"] = userinfo["wood"] + chopped
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

					
						
						except:
							em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								except:
									pass
							pass
						if amount>= 4:
							await asyncio.sleep(0.6)
							userinfo["keys"] = userinfo["keys"] - 1
							userinfo["lootbag"] = userinfo["lootbag"] - 1
							try:
								chance = random.randint(1, 1000)
								legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
								rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
								common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
								material = randchoice(["Stone", "Metal", "Wood"])


								if legendary == "Excalibur":
									legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

								elif legendary == "Twilight":
									legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

								elif legendary == "Devil's Kiss":
									legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

								elif legendary == "Hawkeye":
									legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

								elif legendary == "Solarflare":
									legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

								elif legendary == "Thunderguard":
									legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

								elif legendary == "Doomblade":
									legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

								elif legendary == "Deathraze":
									legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

								elif legendary == "Soulreaper":
									legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

								elif legendary == "Nightstalker Mantle":
									legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

								elif legendary == "Bane Of The Goblin Lord":
									legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

								elif legendary == "Hephaestus Armor":
									legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

								if chance > 990:
			
									if legendary == "exp":
										expgained = random.randint(1, 3)
										userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

									userinfo["inventory"].append(legendaryitemobj)
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
									except:
										try:
											await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
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
												pass
											except:
												userinfo["keys"] = userinfo["keys"] + 1
												userinfo["lootbag"] = userinfo["lootbag"] + 1
												db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
												print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
												em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
												await ctx.send(embed=em)
												pass

									legendarytitle = "Legendary"
									if not legendarytitle in titlesinfo["titles_list"]:
										titlesinfo["titles_list"].append(legendarytitle)
										titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
										db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
										em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
										em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
										try:
											await ctx.send(user, embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass
									return

								if rare == "Iron Claws":
									rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

								elif rare == "Iron Mace":
									rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

								elif rare == "Curved Dagger":
									rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

								elif rare == "Tomb of Water":
									rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

								elif rare == "Spiked Mace":
									rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

								elif rare == "Mithril Sword":
									rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

								elif rare == "Etched Longbow":
									rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

								elif rare == "Verdant Bow":
									rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

								elif rare == "Iron Armor":
									rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

								elif rare == "Branded Metal Armor":
									rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

								elif rare == "Wolf Fur":
									rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

								elif rare == "Enchanted Steel Armor":
									rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


								if chance < 950 and chance > 700:
									userinfo["inventory"].append(rareitemobj)
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								if common == "Sclerite Sword":
									commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

								elif common == "Iron Greatsword":
									commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

								elif common == "Abaddon Dagger":
									commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

								elif common == "Rusted Short Sword":
									commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

								elif common == "Makeshift Shortbow":
									commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

								elif common == "Obsidian Longbow":
									commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

								elif common == "Concealed Blade":
									commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

								elif common == "Tomb of Fire":
									commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

								elif common == "Scroll of Blizzards":
									commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

								elif common ==  "Glyphic Bow":
									commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

								elif common == "Oblivion":
									commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

								elif common == "Staff of Milos":
									commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

								elif common == "Calcite Staff":
									commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

								elif common == "Leather Armor":
									commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

								elif common == "Banded Armor":
									commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

								elif common == "Pit Fighter Armor":
									commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

								elif common == "Chainmail Armor":
									commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

								elif common == "Barbaric Armor":
									commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

								if chance < 700 and chance > 300:

									userinfo["inventory"].append(commonitemobj)
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
									pass


								if chance < 300 and chance > 50:

									if material == "Stone":
										mined_stone = random.randint(1, 5)
										userinfo["stone"] = userinfo["stone"] + mined_stone
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

									elif material == "Metal":
										mined_metal= random.randint(1, 2)
										userinfo["metal"] = userinfo["metal"] + mined_metal
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

									elif material == "Wood":
										chopped = random.randint(1, 5)
										userinfo["wood"] = userinfo["wood"] + chopped
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

					
						
							except:
								em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
								try:
									await ctx.send(embed=em)
								except:
									try:
										await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
									except:
										pass
								pass













		elif userinfo["role"] == "patreon4":

			times = amount 

			if amount >= 6:
				em = discord.Embed(description="You cant open more then 5 crates!", color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return
			
			if userinfo["questname"] == "Unboxing I":
				userinfo["questprogress"] = userinfo["questprogress"] + amount
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				if userinfo["questprogress"] >= 10:
					await ctx.send("Quest Updated!")
				pass

			if userinfo["lootbag"] == 0 or userinfo["lootbag"] < amount:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nocrates"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			if userinfo["keys"] == 0 or userinfo["keys"] < amount:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["nokeys"]["translation"], color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				return

			opening = 27 - times
			if len(userinfo["inventory"]) >= 25 or len(userinfo["inventory"]) >= opening:
				try:
					em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["general"]["fullinv"]["translation"], color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
				except:
					return
				return

		

			if amount == 1: 
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening"]["translation"].format(userinfo["name"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
			else:
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["opening2"]["translation"].format(userinfo["name"], amount), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)

			await asyncio.sleep(5)

			guildinfo = db.servers.find_one({ "_id": guild.id })
			try:
				if guildinfo["mission"] == "Open 250 lootbags":
					if not guildinfo["mission"] == "Open 250 lootbags":
						pass
				try:
					guildinfo["missionprogress"] = guildinfo["missionprogress"] + amount
					db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
					pass
				except:
					print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
					pass
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				pass

			goldmul = random.randint(12, 28)
			goldgain = goldmul * 3 + userinfo["lvl"]
			
				# Crate 1
			if amount>= 1:
				await asyncio.sleep(0.6)
				userinfo["keys"] = userinfo["keys"] - 1
				userinfo["lootbag"] = userinfo["lootbag"] - 1
				try:
					chance = random.randint(1, 1000)
					legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
					rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
					common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
					material = randchoice(["Stone", "Metal", "Wood"])


					if legendary == "Excalibur":
						legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

					elif legendary == "Twilight":
						legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

					elif legendary == "Devil's Kiss":
						legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

					elif legendary == "Hawkeye":
						legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

					elif legendary == "Solarflare":
						legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

					elif legendary == "Thunderguard":
						legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

					elif legendary == "Doomblade":
						legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

					elif legendary == "Deathraze":
						legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

					elif legendary == "Soulreaper":
						legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

					elif legendary == "Nightstalker Mantle":
						legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

					elif legendary == "Bane Of The Goblin Lord":
						legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

					elif legendary == "Hephaestus Armor":
						legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

					if chance > 990:
			
						if legendary == "exp":
							expgained = random.randint(1, 3)
							userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						userinfo["inventory"].append(legendaryitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
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
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

						legendarytitle = "Legendary"
						if not legendarytitle in titlesinfo["titles_list"]:
							titlesinfo["titles_list"].append(legendarytitle)
							titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
							db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
							em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
							em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
							try:
								await ctx.send(user, embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass
						return

					if rare == "Iron Claws":
						rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

					elif rare == "Iron Mace":
						rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

					elif rare == "Curved Dagger":
						rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

					elif rare == "Tomb of Water":
						rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

					elif rare == "Spiked Mace":
						rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

					elif rare == "Mithril Sword":
						rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

					elif rare == "Etched Longbow":
						rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

					elif rare == "Verdant Bow":
						rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

					elif rare == "Iron Armor":
						rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Branded Metal Armor":
						rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Wolf Fur":
						rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

					elif rare == "Enchanted Steel Armor":
						rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


					if chance < 950 and chance > 700:
						userinfo["inventory"].append(rareitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							pass
						except:
							userinfo["keys"] = userinfo["keys"] + 1
							userinfo["lootbag"] = userinfo["lootbag"] + 1
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
							em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
							await ctx.send(embed=em)
							pass

					if common == "Sclerite Sword":
						commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

					elif common == "Iron Greatsword":
						commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

					elif common == "Abaddon Dagger":
						commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

					elif common == "Rusted Short Sword":
						commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

					elif common == "Makeshift Shortbow":
						commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

					elif common == "Obsidian Longbow":
						commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

					elif common == "Concealed Blade":
						commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

					elif common == "Tomb of Fire":
						commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

					elif common == "Scroll of Blizzards":
						commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

					elif common ==  "Glyphic Bow":
						commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

					elif common == "Oblivion":
						commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

					elif common == "Staff of Milos":
						commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

					elif common == "Calcite Staff":
						commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

					elif common == "Leather Armor":
						commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Banded Armor":
						commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Pit Fighter Armor":
						commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Chainmail Armor":
						commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

					elif common == "Barbaric Armor":
						commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

					if chance < 700 and chance > 300:

						userinfo["inventory"].append(commonitemobj)
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
						em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
						try:
							await ctx.send(embed=em)
							pass
						except:
							userinfo["keys"] = userinfo["keys"] + 1
							userinfo["lootbag"] = userinfo["lootbag"] + 1
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
							em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
							await ctx.send(embed=em)
						pass


					if chance < 300 and chance > 50:

						if material == "Stone":
							mined_stone = random.randint(1, 5)
							userinfo["stone"] = userinfo["stone"] + mined_stone
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						elif material == "Metal":
							mined_metal= random.randint(1, 2)
							userinfo["metal"] = userinfo["metal"] + mined_metal
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						elif material == "Wood":
							chopped = random.randint(1, 5)
							userinfo["wood"] = userinfo["wood"] + chopped
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

					
						
				except:
					em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
					try:
						await ctx.send(embed=em)
					except:
						try:
							await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						except:
							pass
					pass
				if amount>= 2:
					await asyncio.sleep(0.6)
					userinfo["keys"] = userinfo["keys"] - 1
					userinfo["lootbag"] = userinfo["lootbag"] - 1
					try:
						chance = random.randint(1, 1000)
						legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
						rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
						common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
						material = randchoice(["Stone", "Metal", "Wood"])


						if legendary == "Excalibur":
							legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

						elif legendary == "Twilight":
							legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

						elif legendary == "Devil's Kiss":
							legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

						elif legendary == "Hawkeye":
							legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

						elif legendary == "Solarflare":
							legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

						elif legendary == "Thunderguard":
							legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

						elif legendary == "Doomblade":
							legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

						elif legendary == "Deathraze":
							legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

						elif legendary == "Soulreaper":
							legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

						elif legendary == "Nightstalker Mantle":
							legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

						elif legendary == "Bane Of The Goblin Lord":
							legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

						elif legendary == "Hephaestus Armor":
							legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

						if chance > 990:
			
							if legendary == "exp":
								expgained = random.randint(1, 3)
								userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							userinfo["inventory"].append(legendaryitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
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
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

							legendarytitle = "Legendary"
							if not legendarytitle in titlesinfo["titles_list"]:
								titlesinfo["titles_list"].append(legendarytitle)
								titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
								db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
								em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
								em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
								try:
									await ctx.send(user, embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass
							return

						if rare == "Iron Claws":
							rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

						elif rare == "Iron Mace":
							rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

						elif rare == "Curved Dagger":
							rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

						elif rare == "Tomb of Water":
							rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

						elif rare == "Spiked Mace":
							rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

						elif rare == "Mithril Sword":
							rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

						elif rare == "Etched Longbow":
							rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

						elif rare == "Verdant Bow":
							rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

						elif rare == "Iron Armor":
							rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Branded Metal Armor":
							rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Wolf Fur":
							rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

						elif rare == "Enchanted Steel Armor":
							rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


						if chance < 950 and chance > 700:
							userinfo["inventory"].append(rareitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
								pass

						if common == "Sclerite Sword":
							commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

						elif common == "Iron Greatsword":
							commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

						elif common == "Abaddon Dagger":
							commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

						elif common == "Rusted Short Sword":
							commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

						elif common == "Makeshift Shortbow":
							commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

						elif common == "Obsidian Longbow":
							commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

						elif common == "Concealed Blade":
							commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

						elif common == "Tomb of Fire":
							commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

						elif common == "Scroll of Blizzards":
							commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

						elif common ==  "Glyphic Bow":
							commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

						elif common == "Oblivion":
							commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

						elif common == "Staff of Milos":
							commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

						elif common == "Calcite Staff":
							commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

						elif common == "Leather Armor":
							commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Banded Armor":
							commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Pit Fighter Armor":
							commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Chainmail Armor":
							commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

						elif common == "Barbaric Armor":
							commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

						if chance < 700 and chance > 300:

							userinfo["inventory"].append(commonitemobj)
							db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
							em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
							try:
								await ctx.send(embed=em)
								pass
							except:
								userinfo["keys"] = userinfo["keys"] + 1
								userinfo["lootbag"] = userinfo["lootbag"] + 1
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
								em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
								await ctx.send(embed=em)
							pass


						if chance < 300 and chance > 50:

							if material == "Stone":
								mined_stone = random.randint(1, 5)
								userinfo["stone"] = userinfo["stone"] + mined_stone
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							elif material == "Metal":
								mined_metal= random.randint(1, 2)
								userinfo["metal"] = userinfo["metal"] + mined_metal
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							elif material == "Wood":
								chopped = random.randint(1, 5)
								userinfo["wood"] = userinfo["wood"] + chopped
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

					
						
					except:
						em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
							except:
								pass
						pass
					if amount>= 3:
						await asyncio.sleep(0.6)
						userinfo["keys"] = userinfo["keys"] - 1
						userinfo["lootbag"] = userinfo["lootbag"] - 1
						try:
							chance = random.randint(1, 1000)
							legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
							rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
							common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
							material = randchoice(["Stone", "Metal", "Wood"])


							if legendary == "Excalibur":
								legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

							elif legendary == "Twilight":
								legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

							elif legendary == "Devil's Kiss":
								legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

							elif legendary == "Hawkeye":
								legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

							elif legendary == "Solarflare":
								legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

							elif legendary == "Thunderguard":
								legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

							elif legendary == "Doomblade":
								legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

							elif legendary == "Deathraze":
								legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

							elif legendary == "Soulreaper":
								legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

							elif legendary == "Nightstalker Mantle":
								legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

							elif legendary == "Bane Of The Goblin Lord":
								legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

							elif legendary == "Hephaestus Armor":
								legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

							if chance > 990:
			
								if legendary == "exp":
									expgained = random.randint(1, 3)
									userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								userinfo["inventory"].append(legendaryitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
								except:
									try:
										await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
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
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

								legendarytitle = "Legendary"
								if not legendarytitle in titlesinfo["titles_list"]:
									titlesinfo["titles_list"].append(legendarytitle)
									titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
									db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
									em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
									em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
									try:
										await ctx.send(user, embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass
								return

							if rare == "Iron Claws":
								rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

							elif rare == "Iron Mace":
								rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

							elif rare == "Curved Dagger":
								rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

							elif rare == "Tomb of Water":
								rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

							elif rare == "Spiked Mace":
								rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

							elif rare == "Mithril Sword":
								rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

							elif rare == "Etched Longbow":
								rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

							elif rare == "Verdant Bow":
								rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

							elif rare == "Iron Armor":
								rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Branded Metal Armor":
								rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Wolf Fur":
								rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

							elif rare == "Enchanted Steel Armor":
								rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


							if chance < 950 and chance > 700:
								userinfo["inventory"].append(rareitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
									pass

							if common == "Sclerite Sword":
								commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

							elif common == "Iron Greatsword":
								commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

							elif common == "Abaddon Dagger":
								commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

							elif common == "Rusted Short Sword":
								commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

							elif common == "Makeshift Shortbow":
								commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

							elif common == "Obsidian Longbow":
								commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

							elif common == "Concealed Blade":
								commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

							elif common == "Tomb of Fire":
								commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

							elif common == "Scroll of Blizzards":
								commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

							elif common ==  "Glyphic Bow":
								commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

							elif common == "Oblivion":
								commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

							elif common == "Staff of Milos":
								commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

							elif common == "Calcite Staff":
								commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

							elif common == "Leather Armor":
								commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Banded Armor":
								commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Pit Fighter Armor":
								commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Chainmail Armor":
								commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

							elif common == "Barbaric Armor":
								commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

							if chance < 700 and chance > 300:

								userinfo["inventory"].append(commonitemobj)
								db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
								em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
								try:
									await ctx.send(embed=em)
									pass
								except:
									userinfo["keys"] = userinfo["keys"] + 1
									userinfo["lootbag"] = userinfo["lootbag"] + 1
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
									em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
									await ctx.send(embed=em)
								pass


							if chance < 300 and chance > 50:

								if material == "Stone":
									mined_stone = random.randint(1, 5)
									userinfo["stone"] = userinfo["stone"] + mined_stone
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								elif material == "Metal":
									mined_metal= random.randint(1, 2)
									userinfo["metal"] = userinfo["metal"] + mined_metal
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								elif material == "Wood":
									chopped = random.randint(1, 5)
									userinfo["wood"] = userinfo["wood"] + chopped
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

					
						
						except:
							em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
								except:
									pass
							pass
						if amount>= 4:
							await asyncio.sleep(0.6)
							userinfo["keys"] = userinfo["keys"] - 1
							userinfo["lootbag"] = userinfo["lootbag"] - 1
							try:
								chance = random.randint(1, 1000)
								legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
								rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
								common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
								material = randchoice(["Stone", "Metal", "Wood"])


								if legendary == "Excalibur":
									legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

								elif legendary == "Twilight":
									legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

								elif legendary == "Devil's Kiss":
									legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

								elif legendary == "Hawkeye":
									legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

								elif legendary == "Solarflare":
									legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

								elif legendary == "Thunderguard":
									legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

								elif legendary == "Doomblade":
									legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

								elif legendary == "Deathraze":
									legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

								elif legendary == "Soulreaper":
									legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

								elif legendary == "Nightstalker Mantle":
									legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

								elif legendary == "Bane Of The Goblin Lord":
									legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

								elif legendary == "Hephaestus Armor":
									legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

								if chance > 990:
			
									if legendary == "exp":
										expgained = random.randint(1, 3)
										userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

									userinfo["inventory"].append(legendaryitemobj)
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
									except:
										try:
											await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
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
												pass
											except:
												userinfo["keys"] = userinfo["keys"] + 1
												userinfo["lootbag"] = userinfo["lootbag"] + 1
												db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
												print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
												em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
												await ctx.send(embed=em)
												pass

									legendarytitle = "Legendary"
									if not legendarytitle in titlesinfo["titles_list"]:
										titlesinfo["titles_list"].append(legendarytitle)
										titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
										db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
										em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
										em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
										try:
											await ctx.send(user, embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass
									return

								if rare == "Iron Claws":
									rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

								elif rare == "Iron Mace":
									rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

								elif rare == "Curved Dagger":
									rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

								elif rare == "Tomb of Water":
									rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

								elif rare == "Spiked Mace":
									rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

								elif rare == "Mithril Sword":
									rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

								elif rare == "Etched Longbow":
									rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

								elif rare == "Verdant Bow":
									rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

								elif rare == "Iron Armor":
									rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

								elif rare == "Branded Metal Armor":
									rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

								elif rare == "Wolf Fur":
									rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

								elif rare == "Enchanted Steel Armor":
									rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


								if chance < 950 and chance > 700:
									userinfo["inventory"].append(rareitemobj)
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
										pass

								if common == "Sclerite Sword":
									commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

								elif common == "Iron Greatsword":
									commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

								elif common == "Abaddon Dagger":
									commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

								elif common == "Rusted Short Sword":
									commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

								elif common == "Makeshift Shortbow":
									commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

								elif common == "Obsidian Longbow":
									commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

								elif common == "Concealed Blade":
									commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

								elif common == "Tomb of Fire":
									commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

								elif common == "Scroll of Blizzards":
									commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

								elif common ==  "Glyphic Bow":
									commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

								elif common == "Oblivion":
									commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

								elif common == "Staff of Milos":
									commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

								elif common == "Calcite Staff":
									commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

								elif common == "Leather Armor":
									commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

								elif common == "Banded Armor":
									commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

								elif common == "Pit Fighter Armor":
									commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

								elif common == "Chainmail Armor":
									commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

								elif common == "Barbaric Armor":
									commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

								if chance < 700 and chance > 300:

									userinfo["inventory"].append(commonitemobj)
									db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
									em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
									try:
										await ctx.send(embed=em)
										pass
									except:
										userinfo["keys"] = userinfo["keys"] + 1
										userinfo["lootbag"] = userinfo["lootbag"] + 1
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
										em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
										await ctx.send(embed=em)
									pass


								if chance < 300 and chance > 50:

									if material == "Stone":
										mined_stone = random.randint(1, 5)
										userinfo["stone"] = userinfo["stone"] + mined_stone
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

									elif material == "Metal":
										mined_metal= random.randint(1, 2)
										userinfo["metal"] = userinfo["metal"] + mined_metal
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

									elif material == "Wood":
										chopped = random.randint(1, 5)
										userinfo["wood"] = userinfo["wood"] + chopped
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

					
						
							except:
								em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
								try:
									await ctx.send(embed=em)
								except:
									try:
										await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
									except:
										pass
								pass
							if amount>= 5:
								await asyncio.sleep(0.6)
								userinfo["keys"] = userinfo["keys"] - 1
								userinfo["lootbag"] = userinfo["lootbag"] - 1
								try:
									chance = random.randint(1, 1000)
									legendary = randchoice(["Excalibur", "Twilight", "Devil's Kiss", "Hawkeye", "Solarflare", "Thunderguard", "Doomblade", "Deathraze", "Soulreaper", "Nightstalker Mantle", "Bane Of The Goblin Lord", "Hephaestus Armor", "exp"])
									rare = randchoice(["Iron Claws", "Iron Mace", "Tomb of Water", "Curved Dagger", "Spiked Mace", "Mithril Sword", "Etched Longbow", "Verdant Bow"])
									common = randchoice(["Sclerite Sword", "Iron Greatsword", "Concealed Blade", "Abaddon Dagger", "Rusted Short Sword", "Makeshift Shortbow", "Obsidian Longbow", "Glyphic Bow", "Tomb of Fire", "Scroll of Blizzards", "Oblivion", "Staff of Milos", "Calcite Staff", "Leather Armor", "Banded Armor", "Pit Fighter Armor", "Chainmail Armor", "Barbaric Armor"])
									material = randchoice(["Stone", "Metal", "Wood"])


									if legendary == "Excalibur":
										legendaryitemobj = {"name": "Excalibur", "type": "sword", "rarity": "Legendary", "stats_min": 25, "stats_max": 41, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/mnQAA1X.png"}

									elif legendary == "Twilight":
										legendaryitemobj = {"name": "Twilight", "type": "sword", "rarity": "Legendary", "stats_min": 31, "stats_max": 40, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/HFH7ugZ.png"}

									elif legendary == "Devil's Kiss":
										legendaryitemobj = {"name": "Devil's Kiss", "type": "bow", "rarity": "Legendary", "stats_min": 25, "stats_max": 37, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/59tnHA8.png"}

									elif legendary == "Hawkeye":
										legendaryitemobj = {"name": "Hawkeye", "type": "bow", "rarity": "Legendary", "stats_min": 32, "stats_max": 44, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/dnkLTAj.png"}

									elif legendary == "Solarflare":
										legendaryitemobj = {"name": "Solarflare", "type": "staff", "rarity": "Legendary", "stats_min": 27, "stats_max": 51, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/ZP2KxJl.png"}

									elif legendary == "Thunderguard":
										legendaryitemobj = {"name": "Thunderguard", "type": "staff", "rarity": "Legendary", "stats_min": 29, "stats_max": 39, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/XXSZylz.png"}

									elif legendary == "Doomblade":
										legendaryitemobj = {"name": "Doomblade", "type": "dagger", "rarity": "Legendary", "stats_min": 31, "stats_max": 48, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/kFHHkyu.png"}

									elif legendary == "Deathraze":
										legendaryitemobj = {"name": "Deathraze", "type": "dagger", "rarity": "Legendary", "stats_min": 32, "stats_max": 52, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/2jRAyud.png"}

									elif legendary == "Soulreaper":
										legendaryitemobj = {"name": "Soulreaper", "type": "dagger", "rarity": "Legendary", "stats_min": 27, "stats_max": 46, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/xpmTArc.png"}

									elif legendary == "Nightstalker Mantle":
										legendaryitemobj = {"name": "Nightstalker Mantle", "type": "armor", "rarity": "Legendary", "stats_min": 12, "stats_max": 28, "refinement": "Normal", "description": "?!",  "image": "None"}

									elif legendary == "Bane Of The Goblin Lord":
										legendaryitemobj = {"name": "Bane Of The Goblin Lord", "type": "armor", "rarity": "Legendary", "stats_min": 20, "stats_max": 25, "refinement": "Normal", "description": "?!",  "image": "None"}

									elif legendary == "Hephaestus Armor":
										legendaryitemobj = {"name": "Hephaestus Armor", "type": "armor", "rarity": "Legendary", "stats_min": 16, "stats_max": 27, "refinement": "Normal", "description": "?!",  "image": "None"}
		

									if chance > 990:
			
										if legendary == "exp":
											expgained = random.randint(1, 3)
											userinfo["exp_potions"] = userinfo["exp_potions"] + expgained
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											em = discord.Embed(title="<:ExpBottle:770044187348566046>You find some Experience Potions!", description="+" + str(expgained) + " Experience Potions! <:ExpBottle:770044187348566046>", color=discord.Colour(0xffffff))
											try:
												await ctx.send(embed=em)
												pass
											except:
												userinfo["keys"] = userinfo["keys"] + 1
												userinfo["lootbag"] = userinfo["lootbag"] + 1
												db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
												print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
												em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
												await ctx.send(embed=em)
												pass

										userinfo["inventory"].append(legendaryitemobj)
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary), color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
										except:
											try:
												await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["legendary"]["description"]["translation"].format(legendary))
											except:
												userinfo["keys"] = userinfo["keys"] + 1
												userinfo["lootbag"] = userinfo["lootbag"] + 1
												db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
												print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
												em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
												await ctx.send(embed=em)
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
													pass
												except:
													userinfo["keys"] = userinfo["keys"] + 1
													userinfo["lootbag"] = userinfo["lootbag"] + 1
													db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
													print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
													em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
													await ctx.send(embed=em)
													pass

										legendarytitle = "Legendary"
										if not legendarytitle in titlesinfo["titles_list"]:
											titlesinfo["titles_list"].append(legendarytitle)
											titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
											db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
											em = discord.Embed(title="New Title", description=legendarytitle, color=discord.Colour(0x00ff00))
											em.set_thumbnail(url="https://i.imgur.com/nJBlCei.png")
											try:
												await ctx.send(user, embed=em)
												pass
											except:
												userinfo["keys"] = userinfo["keys"] + 1
												userinfo["lootbag"] = userinfo["lootbag"] + 1
												db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
												print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
												em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
												await ctx.send(embed=em)
												pass
										return

									if rare == "Iron Claws":
										rareitemobj = {"name": "Iron Claws", "type": "dagger", "rarity": "Rare", "stats_min": 24, "stats_max": 28, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/lrk0y5p.png"}

									elif rare == "Iron Mace":
										rareitemobj = {"name": "Iron Mace", "type": "mace", "rarity": "Rare", "stats_min": 20, "stats_max": 30, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/eMGSaS5.png"}

									elif rare == "Curved Dagger":
										rareitemobj = {"name": "Curved Dagger", "type": "dagger", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/31mYMgk.png"}

									elif rare == "Tomb of Water":
										rareitemobj = {"name": "Tomb of Water", "type": "staff", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/H7Umwgs.png"}

									elif rare == "Spiked Mace":
										rareitemobj = {"name": "Spiked Mace", "type": "mace", "rarity": "Rare", "stats_min": 5, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3PZfnkC.png"}

									elif rare == "Mithril Sword":
										rareitemobj = {"name": "Mithril Sword", "type": "sword", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/UNc4JeO.png"}

									elif rare == "Etched Longbow":
										rareitemobj = {"name": "Etched Longbow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/VvYc9zY.png"}

									elif rare == "Verdant Bow":
										rareitemobj = {"name": "Verdant Bow", "type": "bow", "rarity": "Rare", "stats_min": 2, "stats_max": 25, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/3EyPeH2.png"}

									elif rare == "Iron Armor":
										rareitemobj = {"name": "Iron Armor", "type": "armor", "rarity": "Rare", "stats_min": 14, "stats_max": 16, "refinement": "Normal", "description": "?!", "image": "None"}

									elif rare == "Branded Metal Armor":
										rareitemobj = {"name": "Branded Metal Armor", "type": "armor", "rarity": "Rare", "stats_min": 13, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}

									elif rare == "Wolf Fur":
										rareitemobj = {"name": "Wolf Fur", "type": "armor", "rarity": "Rare", "stats_min": 1, "stats_max": 24, "refinement": "Normal", "description": "?!", "image": "None"}

									elif rare == "Enchanted Steel Armor":
										rareitemobj = {"name": "Enchanted Steel Armor", "type": "armor", "rarity": "Rare", "stats_min": 12, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "None"}


									if chance < 950 and chance > 700:
										userinfo["inventory"].append(rareitemobj)
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["rare"]["description"]["translation"].format(rare), color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
											pass

									if common == "Sclerite Sword":
										commonitemobj = {"name": "Sclerite Sword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Evoke3O.png"}

									elif common == "Iron Greatsword":
										commonitemobj = {"name": "Iron Greatsword", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/TlKPvfz.png"}

									elif common == "Abaddon Dagger":
										commonitemobj ={"name": "Abaddon Dagger", "type": "dagger", "rarity": "Common", "stats_min": 3, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/yNkqfOo.png"}

									elif common == "Rusted Short Sword":
										commonitemobj = {"name": "Rusted Short Sword", "type": "dagger", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/Ox1CXhJ.png"}

									elif common == "Makeshift Shortbow":
										commonitemobj = {"name": "Makeshift Shortbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/IDwPClu.png"}

									elif common == "Obsidian Longbow":
										commonitemobj = {"name": "Obsidian Longbow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/0LEmcAH.png"}

									elif common == "Concealed Blade":
										commonitemobj = {"name": "Concealed Blade", "type": "sword", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/dQ6Qt1J.png"}

									elif common == "Tomb of Fire":
										commonitemobj = {"name": "Tomb of Fire", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/xOtnEZO.png"}

									elif common == "Scroll of Blizzards":
										commonitemobj = {"name": "Scroll of Blizzards", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/5dbmIRN.png"}

									elif common ==  "Glyphic Bow":
										commonitemobj ={"name": "Glyphic Bow", "type": "bow", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/DzHgPl4.png"}

									elif common == "Oblivion":
										commonitemobj = {"name": "Oblivion", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/jVIN9in.png"}

									elif common == "Staff of Milos":
										commonitemobj = {"name": "Staff of Milos", "type": "staff", "rarity": "Common", "stats_min": 2, "stats_max": 18, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/9Lakl7u.png"}

									elif common == "Calcite Staff":
										commonitemobj = {"name": "Calcite Staff", "type": "staff", "rarity": "Common", "stats_min": 4, "stats_max": 17, "refinement": "Normal", "description": "?!", "image": "https://i.imgur.com/ZRV97xu.png"}

									elif common == "Leather Armor":
										commonitemobj = {"name": "Leather Armor", "type": "armor", "rarity": "Common", "stats_min": 3, "stats_max": 8, "refinement": "Normal", "description": "?!", "image": "None"}

									elif common == "Banded Armor":
										commonitemobj = {"name": "Banded Armor", "type": "armor", "rarity": "Common", "stats_min": 1, "stats_max": 10, "refinement": "Normal", "description": "?!", "image": "None"}

									elif common == "Pit Fighter Armor":
										commonitemobj = {"name": "Pit Fighter Armor", "type": "armor", "rarity": "Common", "stats_min": 4, "stats_max": 9, "refinement": "Normal", "description": "?!", "image": "None"}

									elif common == "Chainmail Armor":
										commonitemobj = {"name": "Chainmail Armor", "type": "armor", "rarity": "Common", "stats_min": 2, "stats_max": 12, "refinement": "Normal", "description": "?!", "image": "None"}

									elif common == "Barbaric Armor":
										commonitemobj = {"name": "Barbaric Armor", "type": "armor", "rarity": "Common", "stats_min": 5, "stats_max": 7, "refinement": "Normal", "description": "?!", "image": "None"}

									if chance < 700 and chance > 300:

										userinfo["inventory"].append(commonitemobj)
										db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
										em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["crate"]["common"]["description"]["translation"].format(common), color=discord.Colour(0xffffff))
										try:
											await ctx.send(embed=em)
											pass
										except:
											userinfo["keys"] = userinfo["keys"] + 1
											userinfo["lootbag"] = userinfo["lootbag"] + 1
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
											em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
											await ctx.send(embed=em)
										pass


									if chance < 300 and chance > 50:

										if material == "Stone":
											mined_stone = random.randint(1, 5)
											userinfo["stone"] = userinfo["stone"] + mined_stone
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_stone) + " Stone <:Stone:573574662525550593>", color=discord.Colour(0xffffff))
											try:
												await ctx.send(embed=em)
												pass
											except:
												userinfo["keys"] = userinfo["keys"] + 1
												userinfo["lootbag"] = userinfo["lootbag"] + 1
												db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
												print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
												em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
												await ctx.send(embed=em)
												pass

										elif material == "Metal":
											mined_metal= random.randint(1, 2)
											userinfo["metal"] = userinfo["metal"] + mined_metal
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(mined_metal) + " Metal <:Metal:573574661108006915>", color=discord.Colour(0xffffff))
											try:
												await ctx.send(embed=em)
												pass
											except:
												userinfo["keys"] = userinfo["keys"] + 1
												userinfo["lootbag"] = userinfo["lootbag"] + 1
												db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
												print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
												em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
												await ctx.send(embed=em)
												pass

										elif material == "Wood":
											chopped = random.randint(1, 5)
											userinfo["wood"] = userinfo["wood"] + chopped
											db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
											em = discord.Embed(title="<:Crate:639425690072252426>You find some materials!", description="+" + str(chopped) + " Wood <:Wood:573574660185260042>", color=discord.Colour(0xffffff))
											try:
												await ctx.send(embed=em)
												pass
											except:
												userinfo["keys"] = userinfo["keys"] + 1
												userinfo["lootbag"] = userinfo["lootbag"] + 1
												db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
												print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has failed to open"+amount+"Crates, has been refunded 1 key and crate")
												em = discord.Embed(title="Crate Error", description="You have been refunded 1 crate and 1 key", color=discord.Colour(0xffffff))
												await ctx.send(embed=em)
												pass

					
						
								except:
									em = discord.Embed(description="<:Crate:639425690072252426> The crate didn't contain anything!", color=discord.Colour(0xffffff))
					
									try:
										await ctx.send(embed=em)
									except:
										try:
											await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
										except:
											pass
									pass
def setup(bot):
	n = loot(bot)
	bot.add_cog(n)