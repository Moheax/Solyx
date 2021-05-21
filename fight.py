import asyncio
import datetime
import random
from random import choice as randchoice

import discord
from discord.ext import commands

from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import userdata
from cogs.levelup import _level_up_check_user
from cogs.guild import _guild_mission_check
from cogs.quests import _quest_check

async def _heal_reaction(user, msg):
	userinfo = db.users.find_one({"_id": user.id})
	if userinfo["health"] == userinfo["MaxHealth"]:
		em = discord.Embed(description="<:HealingPotion:573577125064605706> You already have {} HP!".format(userinfo["MaxHealth"]), color=discord.Colour(0xffffff))
		await msg.edit(embed=em)
		return
	if userinfo["hp_potions"] > 0:
		gain = random.randint(25, 55)
		userinfo["health"] = userinfo["health"] + gain
		if userinfo["health"] > userinfo["MaxHealth"]:
			userinfo["health"] = userinfo["MaxHealth"]
		userinfo["hp_potions"] = userinfo["hp_potions"] - 1
		db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
		em = discord.Embed(title="<:HealingPotion:573577125064605706> You used a Minor Health Potion", description="+{} HP".format(gain), color=discord.Colour(0xffffff))
		try:
			await msg.edit(embed=em)
		except:
			return
	else:
		em = discord.Embed(description="<:HealingPotion:573577125064605706> You don't have any health potions!", color=discord.Colour(0xffffff))
		try:
			await msg.edit(embed=em)
		except:
			return


class fight(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
     
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

	# handles battle creation.

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def fight(self, ctx):

		languageinfo = db.servers.find_one({"_id": ctx.guild.id})
		language = languageinfo["language"]

		user = ctx.author
		userinfo = db.users.find_one({"_id": user.id})
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo["blacklisted"] == "True":
			return

		if userinfo["axelvl"] == 0:
			userinfo["axelvl"] = 1
		if userinfo["pickaxelvl"] == 0:
			userinfo["pickaxelvl"] = 1
		if userinfo["sawlvl"] == 0:
			userinfo["sawlvl"] = 1
		if userinfo["chisellvl"] == 0:
			userinfo["chisellvl"] = 1
		if userinfo["hammerlvl"] == 0:
			userinfo["hammerlvl"] = 1

		if userinfo["questname"] == "Basic C":
			userinfo["questprogress"] = userinfo["questprogress"] + 1
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
			if userinfo["questprogress"] >= 1:
				await _quest_check(self, ctx, user)
			pass

		if userinfo["questname"] == "Fight I":
			userinfo["questprogress"] = userinfo["questprogress"] + 1
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
			if userinfo["questprogress"] >= 25:
				await _quest_check(self, ctx, user)
			pass

		if userinfo["health"] <= 0:
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["fight"]["nohp"]["translation"])
			return
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator, "Started a fight")

		# IF PLAYER ISNT FIGHTING AN ENEMY, CHOOSE ONE BASED ON LOCATION
		if userinfo["selected_enemy"] == "None":
			if userinfo["location"] == "Golden Temple":
				chance = random.randint(1, 100)

				if chance >= 90:
					debi = randchoice(["Fire Golem"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Wyvern"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Rachi", "Debin", "Oofer"])


			elif userinfo["location"] == "Saker Keep":
				chance = random.randint(1, 100)

				if chance >= 90:
					debi = randchoice(["The Corrupted"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Souleater"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Draugr", "Stalker"])

		
			elif userinfo["location"] == "The Forest":
				chance = random.randint(1, 100)

				if chance >= 90:
					debi = randchoice(["Phantasm"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Zombie"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Wolf", "Goblin"])

				
			elif userinfo["location"] == "Ebony Mountains":
				chance = random.randint(1, 100)

				if chance >= 90:
					debi = randchoice(["The Accursed"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Ebony Guardian"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Elder Dragon", "Hades"])


			elif userinfo["location"] == "Township of Arkina":
				chance = random.randint(1, 100)

				if chance >= 90:
					debi = randchoice(["The Nameless King"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Harpy"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Ettin", "Dormammu"])


			elif userinfo["location"] == "Zulanthu":
				chance = random.randint(1, 100)

				if chance >= 90:
					debi = randchoice(["The Venomous"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Largos"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Saurian", "Deathclaw"])


			elif userinfo["location"] == "Lost City":
				chance = random.randint(1, 100)

				if chance >= 90:
					debi = randchoice(["Death Knight"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Giant"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Skeleton", "Lizardmen"])

				
			elif userinfo["location"] == "Drenheim":
				chance = random.randint(1, 100)

				if chance >= 90:
					debi = randchoice(["Frost Dragon"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Frost Orc"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Ice Wolves", "Frost Goblin"])

		
			
			difficulty = random.randint(1, 100)

			userinfo["enemydifficulty"] = "Common"
			if difficulty >= 99:
				difficulty = "<:Mythical:573784881386225694> Mythical " 
				userinfo["enemydifficulty"] = "Mythical"

			elif 99 >= difficulty >= 90:
				difficulty = "<:Legendary:639425368167809065> Legendary " 
				userinfo["enemydifficulty"] = "Legendary"

			elif 90 >= difficulty >= 70:
				difficulty = "<:Rare:573784880815538186> Rare " 
				userinfo["enemydifficulty"] = "Rare"

			elif 70 >= difficulty >= 50:
				difficulty = "<:Uncommon:641361853817159685> Uncommon "
				userinfo["enemydifficulty"] = "Uncommon"

			elif 50 >= difficulty >= 0:
				difficulty = "<:Common:573784881012932618> Common " 
				userinfo["enemydifficulty"] = "Common"	


			else:
				pass

			enemyname = difficulty + debi

			if debi == "Fire Golem" or debi == "Phantasm" or debi == "The Corrupted" or debi == "The Accursed" or debi == "The Nameless King" or debi == "The Venomous" or debi == "Death Knight" or debi == "Frost Dragon":
				enemyname = difficulty + ":trident: " + debi
			em = discord.Embed(title=fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["title"]["translation"].format(userinfo["location"], enemyname), description=fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["description"]["translation"], color=discord.Colour(0xffffff))
			if debi == "Phantasm":
				em.set_image(url="https://i.imgur.com/BbBmEOF.jpg")
			elif debi == "Fire Golem":
				em.set_image(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/c7f23f41-5bd8-4b82-a00c-d61b0cfb0160/d9p8w3t-e2e0278a-7b05-4d6b-9a69-c50f3f005126.png/v1/fill/w_700,h_331,q_70,strp/fire_golem_by_sourshade_d9p8w3t-350t.jpg")
			elif debi == "The Corrupted":
				em.set_image(url="https://i.imgur.com/oTi3K3q.jpg")
			elif debi == "Death Knight":
				em.set_image(url="https://i.imgur.com/ELd7Ll5.jpg")
			elif debi == "Frost Dragon":
				em.set_image(url="https://cdn.wallpapersafari.com/11/55/3hBQ9Z.jpg")
			em.set_footer(text="yes / no")
			await ctx.send(embed=em)
			options = ["y", "Y", "yes", "Yes", "n", "N", "No", "no", "-fight"]
			answer1 = await self.check_answer(ctx, options)
			
			if answer1 == "y" or answer1 == "Y" or answer1 == "Yes" or answer1 == "yes":
				userinfo["selected_enemy"] = debi
				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)


				# Hp steps increase 1 hard 2 boss pers monster kind (hard +2 steps) (boss (+2 extra steps)
				# hp steps increase by 1 per location

				# GOLDEN TEMPLE DONE
				# Normal monsters
				if userinfo["selected_enemy"] == "Rachi" or userinfo["selected_enemy"] == "Debin" or userinfo["selected_enemy"] == "Oofer": 
					userinfo["enemyhp"] = random.randint(10, 30)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))
	
					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					
						
				# Hard monsters
				elif userinfo["selected_enemy"] == "Wyvern":
					userinfo["enemyhp"] = random.randint(30, 50)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					

				# Boss
				elif userinfo["selected_enemy"] == "Fire Golem":
					userinfo["enemyhp"] = random.randint(40, 60)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))
	
					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					


				# SAKER KEEP DONE
				# Normal monsters
				elif userinfo["selected_enemy"] == "Draugr" or userinfo["selected_enemy"] == "Stalker":
					userinfo["enemyhp"] = random.randint(20, 40)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					


				# Hard monsters
				elif userinfo["selected_enemy"] == "Souleater":
					userinfo["enemyhp"] = random.randint(40, 60)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))
	
					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					
				# Boss	
				elif userinfo["selected_enemy"] == "The Corrupted":
					userinfo["enemyhp"] = random.randint(40, 60)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					
				

				# THE FOREST DONE
				# Normal monsters
				elif userinfo["selected_enemy"] == "Wolf" or userinfo["selected_enemy"] == "Goblin":
					userinfo["enemyhp"] = random.randint(50, 70)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					


				# Hard monsters
				elif userinfo["selected_enemy"] == "Zombie":
					userinfo["enemyhp"] = random.randint(60, 80)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					

				# Boss	
				elif userinfo["selected_enemy"] == "Phantasm":
					userinfo["enemyhp"] = random.randint(70, 90)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					

				# EBONY MOUNTAINS DONE
				# Normal monsters
				elif userinfo["selected_enemy"] == "Elder Dragon" or userinfo["selected_enemy"] == "Hades":
					userinfo["enemyhp"] = random.randint(70, 90)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					

				# Hard monsters
				elif userinfo["selected_enemy"] == "Ebony Guardian":
					userinfo["enemyhp"] = random.randint(80, 100)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical
					

				# Boss	
				elif userinfo["selected_enemy"] == "The Accursed":
					userinfo["enemyhp"] = random.randint(90, 110)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical


				# TOWN OF ARKINA DONE
				# Normal monsters
				elif userinfo["selected_enemy"] == "Ettin" or userinfo["selected_enemy"] == "Dormammu":
					userinfo["enemyhp"] = random.randint(90, 110)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical


				# Hard monsters
				elif userinfo["selected_enemy"] == "Harpy":
					userinfo["enemyhp"] = random.randint(100, 120)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical


				# Boss	
				elif userinfo["selected_enemy"] == "The Nameless King":
					userinfo["enemyhp"] = random.randint(110, 130)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical


				# Zulanthu DONE
				# Normal monsters
				elif userinfo["selected_enemy"] == "Saurian" or userinfo["selected_enemy"] == "Deathclaw":
					userinfo["enemyhp"] = random.randint(90, 110)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical


				# Hard monsters
				elif userinfo["selected_enemy"] == "Largos":
					userinfo["enemyhp"] = random.randint(100, 120)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical

				# Boss	
				elif userinfo["selected_enemy"] == "The Venomous":
					userinfo["enemyhp"] = random.randint(110, 130)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))
						
					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical


				# Lost City DONE
				# Normal monsters
				elif userinfo["selected_enemy"] == "Skeleton" or userinfo["selected_enemy"] == "Lizardmen":
					userinfo["enemyhp"] = random.randint(120, 140)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))
						
					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical


				# Hard monsters
				elif userinfo["selected_enemy"] == "Giant":
					userinfo["enemyhp"] = random.randint(130, 150)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical

				# Boss	
				elif userinfo["selected_enemy"] == "Death Knight":
					userinfo["enemyhp"] = random.randint(140, 160)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))
						
					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical


				# Drenheim Done
				# Normal monsters
				elif userinfo["selected_enemy"] == "Ice Wolves" or userinfo["selected_enemy"] == "Frost Goblin":
					userinfo["enemyhp"] = random.randint(150, 170)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))
						
					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical


				# Hard monsters
				elif userinfo["selected_enemy"] == "Frost Orc":
					userinfo["enemyhp"] = random.randint(160, 180)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))

					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical

				# Boss	
				elif userinfo["selected_enemy"] == "Frost Dragon":
					userinfo["enemyhp"] = random.randint(170, 190)

					uncommon = (int((userinfo["enemyhp"] / 100) * 20))
					rare = (int((userinfo["enemyhp"] / 100) * 30))
					legendary = (int((userinfo["enemyhp"] / 100) * 40))
					mythical = (int((userinfo["enemyhp"] / 100) * 50))
						
					if userinfo["enemydifficulty"] == "Uncommon":
						userinfo["enemyhp"] = userinfo["enemyhp"] + uncommon
						
					elif userinfo["enemydifficulty"] == "Rare":
						userinfo["enemyhp"] = userinfo["enemyhp"] + rare
						
					elif userinfo["enemydifficulty"] == "Legendary":
						userinfo["enemyhp"] = userinfo["enemyhp"] + legendary
							
					elif userinfo["enemydifficulty"] == "Mythical":
						userinfo["enemyhp"] = userinfo["enemyhp"] + mythical

				
				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			elif answer1 == "n" or answer1 == "N" or answer1 == "no" or answer1 == "No":
				funanswer = randchoice([fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["run"]["run1"]["translation"], fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["run"]["run2"]["translation"], fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["run"]["run3"]["translation"], fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["run"]["run4"]["translation"], fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["run"]["run5"]["translation"]])
				await ctx.send(funanswer)
				return

			else:
				return

	


		# YOUR DAMAGE BASED ON THE WEAPON YOURE HOLDING
# - - Starting weapons - -
		mindmg = userinfo["equip"]["stats_min"]
		maxdmg = userinfo["equip"]["stats_max"]
		youdmg = random.randint(mindmg, maxdmg)


		# YOUR PROTECTION IS BASED ON THE ARMOR YOURE HOLDING
		youdef = 0

		if userinfo["class"] == "Knight":
			youdef += random.randint(5, 10)
		elif userinfo["class"] == "Paladin":
			youdef += random.randint(8, 15)
		elif userinfo["class"] == "Grand Paladin":
			youdef += random.randint(11, 20)

		try:
			mindef = userinfo["wearing"]["stats_min"]
			maxdef = userinfo["wearing"]["stats_max"]
			youdef = random.randint(mindef, maxdef)
		except:
			pass

		# ENEMY DAMAGE BASED ON ENEMY GROUPS
		enemydmg = 0
		enemygold = random.randint(30, 60)
		xpgain = random.randint(10, 15)

	

		guild = ctx.guild
		guildinfo = db.servers.find_one({"_id": guild.id})
		effectiveguildbonus = guildinfo["bonus"]

		if effectiveguildbonus >= 200:
			effectiveguildbonus = 200

		# DMG goes up by 2 with dificulty
		# gold goes up by 3 with difficulty
		# goldlost goes up with 5 with difficulty
		# exp gopes up by 2 with dicciculty
		# each stat goes up with 2 per locaiton
		# soo location 2 everything goes up with 4  


		# GOLDEN TEMPLE
		if userinfo["selected_enemy"] == "Rachi" or userinfo["selected_enemy"] == "Debin" or userinfo["selected_enemy"] == "Oofer":
			enemydmg += random.randint(5, 10)
			enemygold = random.randint(10, 30) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(5, 25)
			
			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg += random.randint(5, 10)
				enemygold = random.randint(10, 30) + effectiveguildbonus
				goldlost = (int(enemygold * 2))
				xpgain = random.randint(5, 25)

				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			if userinfo["enemydifficulty"] == "Rare":
				enemydmg += random.randint(5, 10)
				enemygold = random.randint(10, 30) + effectiveguildbonus
				goldlost = (int(enemygold * 2))
				xpgain = random.randint(5, 25)

				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			if userinfo["enemydifficulty"] == "Legendary":
				enemydmg += random.randint(5, 10)
				enemygold = random.randint(10, 30) + effectiveguildbonus
				goldlost = (int(enemygold * 2))
				xpgain = random.randint(5, 25)

				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))	

			if userinfo["enemydifficulty"] == "Mythical":
				enemydmg += random.randint(5, 10)
				enemygold = random.randint(10, 30) + effectiveguildbonus
				goldlost = (int(enemygold * 2))
				xpgain = random.randint(5, 25)

				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))


		# GOLDEN TEMPLE
		elif userinfo["selected_enemy"] == "Wyvern":
			enemydmg += random.randint(10, 15)
			enemygold = random.randint(15, 35) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(10, 30)
			
			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))


		# GOLDEN TEMPLE
		elif userinfo["selected_enemy"] == "Fire Golem":
			enemydmg += random.randint(20, 30)
			enemygold = random.randint(25, 50) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(20, 40)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# SAKER KEEP
		elif userinfo["selected_enemy"] == "Draugr" or userinfo["selected_enemy"] == "Stalker":
			enemydmg += random.randint(15, 20)
			enemygold = random.randint(20, 40) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(15, 35)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# SAKER KEEP
		elif userinfo["selected_enemy"] == "Souleater":
			enemydmg += random.randint(20, 25)
			enemygold = random.randint(25, 45) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(20, 40)
			
			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# SAKER KEEP
		elif userinfo["selected_enemy"] == "The Corrupted":
			enemydmg += random.randint(30, 40)
			enemygold = random.randint(35, 55) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(30, 50)
			
			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# THE FOREST
		elif userinfo["selected_enemy"] == "Wolf" or userinfo["selected_enemy"] == "Goblin":
			enemydmg += random.randint(25, 30)
			enemygold = random.randint(30, 50) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(25, 45)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# THE FOREST
		elif userinfo["selected_enemy"] == "Zombie":
			enemydmg += random.randint(30, 35)
			enemygold = random.randint(35, 55) + effectiveguildbonus
			goldlost = (int((int(enemygold * 2))))
			xpgain = random.randint(30, 50)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# THE FOREST
		elif userinfo["selected_enemy"] == "Phantasm":
			enemydmg += random.randint(40, 50)
			enemygold = random.randint(45, 65) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(40, 60)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# EBONY MOUNTAINS
		elif userinfo["selected_enemy"] == "Elder Dragon" or userinfo["selected_enemy"] == "Hades":
			enemydmg += random.randint(35, 40)
			enemygold = random.randint(40, 60) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(35, 55)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			if userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

			# EBONY MOUNTAINS
		elif userinfo["selected_enemy"] == "Ebony Guardian":
			enemydmg += random.randint(40, 45)
			enemygold = random.randint(45, 65) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(40, 60)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# EBONY MOUNTAINS
		elif userinfo["selected_enemy"] == "The Accursed":
			enemydmg += random.randint(50, 60)
			enemygold = random.randint(55, 75) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(50, 70)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# TOWNSHIP OF ARKINA
		elif userinfo["selected_enemy"] == "Ettin" or userinfo["selected_enemy"] == "Dormammu":
			enemydmg += random.randint(45, 50)
			enemygold = random.randint(50, 70) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(45, 65)
			
			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# TOWNSHIP OF ARKINA
		elif userinfo["selected_enemy"] == "Harpy":
			enemydmg += random.randint(50, 55)
			enemygold = random.randint(55, 75) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(50, 70)
			
			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# TOWNSHIP OF ARKINA
		elif userinfo["selected_enemy"] == "The Nameless King":
			enemydmg += random.randint(60, 70)
			enemygold = random.randint(65, 85) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(60, 80)
			
			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# ZULANTHU
		elif userinfo["selected_enemy"] == "Deathclaw" or userinfo["selected_enemy"] == "Saurian":
			enemydmg += random.randint(55, 65)
			enemygold = random.randint(60, 80) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(55, 75)
			
			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# ZULANTHU
		elif userinfo["selected_enemy"] == "Largos":
			enemydmg += random.randint(60, 70)
			enemygold = random.randint(65, 85) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(60, 80)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# ZULANTHU
		elif userinfo["selected_enemy"] == "The Venomous":
			enemydmg += random.randint(70, 80)
			enemygold = random.randint(75, 95) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(70, 90)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# LOST CITY
		elif userinfo["selected_enemy"] == "Skeleton" or userinfo["selected_enemy"] == "Lizardmen":
			enemydmg += random.randint(65, 75)
			enemygold = random.randint(70, 90) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(65, 85)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# LOST CITY
		elif userinfo["selected_enemy"] == "Giant":
			enemydmg += random.randint(70, 80)
			enemygold = random.randint(75, 95) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(70, 90)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# LOST CITY
		elif userinfo["selected_enemy"] == "Death Knight": 
			enemydmg += random.randint(80, 90)
			enemygold = random.randint(85, 105) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(80, 100)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# DRENHEIM
		elif userinfo["selected_enemy"] == "Ice Wolves" or userinfo["selected_enemy"] == "Frost Goblin":
			enemydmg += random.randint(75, 85)
			enemygold = random.randint(80, 100) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(75, 95)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# DRENHEIM
		elif userinfo["selected_enemy"] == "Frost Orc":
			enemydmg += random.randint(80, 90)
			enemygold = random.randint(85, 105) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(80, 100)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		# DRENHEIM
		elif userinfo["selected_enemy"] == "Frost Dragon":
			enemydmg += random.randint(90, 100)
			enemygold = random.randint(95, 115) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(90, 110)

			if userinfo["enemydifficulty"] == "Uncommon":
				enemydmg = (int((enemydmg / 100) * 120))
				enemygold = (int((enemygold / 100) * 120))
				goldlost = (int((goldlost / 100) * 120))
				xpgain = (int((xpgain / 100) * 120))

			elif userinfo["enemydifficulty"] == "Rare":
				enemydmg = (int((enemydmg / 100) * 130))
				enemygold = (int((enemygold / 100) * 130))
				goldlost = (int((goldlost / 100) * 130))
				xpgain = (int((xpgain / 100) * 130))

			elif userinfo["enemydifficulty"] == "Legendary":
				enemydmg = (int((enemydmg / 100) * 140))
				enemygold = (int((enemygold / 100) * 140))
				goldlost = (int((goldlost / 100) * 140))
				xpgain = (int((xpgain / 100) * 140))

			elif userinfo["enemydifficulty"] == "Mythical":
				enemydmg = (int((enemydmg / 100) * 150))
				enemygold = (int((enemygold / 100) * 150))
				goldlost = (int((goldlost / 100) * 150))
				xpgain = (int((xpgain / 100) * 150))

		

		elif userinfo["selected_enemy"] == "None":
			return 



			# YOUR SKILL OPTIONS LIST
		skill_list = [i for i in userinfo["skills_learned"]]
		show_list = []
		options = []

		all_skills = [
			"Swing", "Stab", "Shoot",
			"Cast", "Parry", "Distort",
			"Reap", "Overload", "Fusillade",
			"Protrude", "Strike", "Corrupt",
			"Rupture", "Warp", "Arise",
			"Surge", "Slice", "Blockade",
			"Sneak", "Snipe"
		]

		for skill in all_skills:
			if skill in skill_list:
				options.append(skill)
				options.append(skill.lower())
				show_list.append(skill)

		options.append("Heal")
		options.append("heal")
		show_list.append("Heal")

		# IF FOR WHATEVER REASON THE USER DOES -fight AGAIN, RETURN
		em = discord.Embed(title=fileIO(f"data/languages/{language}.json", "load")["fight"]["skill"]["title"]["translation"], description="\n".join(show_list), color=discord.Colour(0xffffff))
		em.set_author(name=fileIO(f"data/languages/{language}.json", "load")["fight"]["skill"]["author"]["translation"], icon_url=ctx.message.author.avatar_url)
		skillmsg = await ctx.send(embed=em)
		answer2 = await self.check_answer(ctx, options)

		monstercolor = discord.Colour(0xffffff)

		if userinfo["enemydifficulty"] == "Common":
			monstercolor = discord.Colour(0x26b644)

		if userinfo["enemydifficulty"] == "Uncommon":
			monstercolor = discord.Colour(0x7bd0e9)
						
		if userinfo["enemydifficulty"] == "Rare":
			monstercolor = discord.Colour(0x3f6fe4)
						
		if userinfo["enemydifficulty"] == "Legendary":
			monstercolor = discord.Colour(0xe79e14)
							
		if userinfo["enemydifficulty"] == "Mythical":
			monstercolor = discord.Colour(0xe57744)

		# DEFINE WHAT SKILL WE SELECTED
		# Done
		if answer2 == "cast" or answer2 == "Cast":
			
			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Cast"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			# Acutal fight msg.
			if userinfo["EnemyStun"] > 0:
				
				enemyhp = userinfo["enemyhp"]
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0

				
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)

				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["Buff1"] == "Surge":
				
				enemyhp = userinfo["enemyhp"]
				# user dmg 
				userhealth = userhealth - enemydmg

				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**you have been stunned for 1 turn**\n**{} Hits {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["Buff1"] == "Arise" and userinfo["Buff1Time"] > 0:
				
				enemyhp = userinfo["enemyhp"]
				hit = int((youdmg / 100) * 25)
				
				# deals dmg to enemy
				totaldmg = hit + hit + hit + hit + hit
				enemyhp = enemyhp - totaldmg - youdmg		
				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0

			
				# Set skill cooldown.
				
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n** {} uses {} and hits {} for {} damage.\n The army of skeletons attacks.\nDealing {} damage each\nDealing a total of {} damage.\n{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], youdmg, hit, totaldmg, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else: 
				
				userhealth = userinfo["health"]
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# Users HP after dmg taken.
				userhealth -= enemydmg
				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		# Done
		elif answer2 == "shoot" or answer2 == "Shoot":
			
			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Shoot"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If enemydmg is lower then 0 its 0
			if enemydmg < 0:
				enemydmg = 0
			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			# Actual fight msg.

			# stunned and buff
			if userinfo["Buff1"] == "Corrupt" and userinfo["Buff1Time"] > 0 and userinfo["EnemyStun"] > 0:
				youdmg = int((youdmg / 100) * 130)
				enemydmg = 0

				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} Has been corrupted for {} turns.**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["selected_enemy"], userinfo["Buff1Time"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			# stunned
			elif userinfo["EnemyStun"] > 0:
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			# Buffs
			elif userinfo["Buff1"] == "Corrupt":
				youdmg = int((youdmg / 100) * 130)
				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				bufftime = userinfo["Buff1Time"]
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has corrupted {} for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return


		# Done
		elif answer2 == "swing" or answer2 == "Swing":
			
			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Swing"
			# Users HP
			userhealth = userinfo["health"]
			
			# Lootbag chance.
			lootbag = random.randint(1, 30)
	
			enemyhp = userinfo["enemyhp"]
			# Acutal fight msg.
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			if userinfo["Buff1"] == "Blockade":
				
				
				# debuff
				youdmg = int((youdmg / 100) * 85)
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg 
				# Users Defense
				youdef = youdef * 2
				enemydmg -= youdef	
				
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# Set skill cooldown.
				userinfo["SkillCooldown2"] = 5
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has the blockade buff doubling defense. {} uses {} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"],  userinfo["name"], move, userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			elif userinfo["Buff1"] == "Slice":

				enemyhp = userinfo["enemyhp"]
				# Bleeding dmg
				bleeding = int((enemyhp / 100) * 25)
				
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg - bleeding
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0

				bufftime = userinfo["Buff1Time"]
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n {} Has bleeding effect for {} turns.**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], bufftime, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				# Users Defense
				enemydmg -= youdef	
				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If UserHealth is More then Maxhealth its Maxhealth
				if userhealth >= userinfo["MaxHealth"]:
					userhealth = userinfo["MaxHealth"]
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return


		# Done
		elif answer2 == "stab" or answer2 == "Stab":


			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Stab"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			

			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If enemydmg is lower then 0 its 0
			if enemydmg < 0:
				enemydmg = 0

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]
	
			# Acutal fight msg.
			if userinfo["EnemyStun"] > 0:
				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			# Buffs
			elif userinfo["Buff1"] == "Rupture":

				enemyhp = userinfo["enemyhp"]
				# Bleeding dmg
				bleeding = int((enemyhp / 100) * 25)
				
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg - bleeding
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0

				bufftime = userinfo["Buff1Time"]
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n {} Has bleeding effect for {} turns.**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], bufftime, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			
			# Warp Buff

			elif userinfo["Buff1"] == "Warp" and userinfo["Buff1Time"] > 0:

				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				enemydmg = int((enemyhp / 100) * 40)
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# set skill cooldown
				userinfo["SkillCooldown1"] = 3
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, But {} has warp debuff.\n the enemy damage is lowered by 60%**\n**{} hits {} for {} damage\n{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"],  userinfo["name"], userinfo["selected_enemy"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		# Done
		elif answer2 == "parry" or answer2 == "Parry":
			# Stun the enemy for 1 turn. 3 turns cooldown.

			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0 
			# Move user makes
			move = "Parry"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			# Acutal fight msg.

			if userinfo["Buff1"] == "Rupture" and userinfo["SkillCooldown1"] == 0:

				enemydmg = 0

				youdmg = 0
				userinfo["EnemyStun"] = 2
				userinfo["SkillCooldown1"] = 4
				stun = 1
				# Bleeding dmg
				bleeding = int((enemyhp / 100) * 25)
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg - bleeding
				# user dmg 
				userhealth = userhealth - enemydmg

				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0

				bufftime = userinfo["Buff1Time"]
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turn\n {} Has bleeding effect for {} turns.**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], stun, userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["SkillCooldown1"] == 0:
				userinfo["EnemyStun"] = 2
				userinfo["SkillCooldown1"] = 4
				stun = 1
				
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turn**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], stun, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["Buff1"] == "Rupture":

				enemydmg = 0

				youdmg = 0
				userinfo["EnemyStun"] = 2
				userinfo["SkillCooldown1"] = 4
				stun = 1
				# Bleeding dmg
				bleeding = int((enemyhp / 100) * 25)
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg - bleeding
				# user dmg 
				userhealth = userhealth - enemydmg
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0

				bufftime = userinfo["Buff1Time"]
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turn\n {} Has bleeding effect for {} turns.**\n**\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], stun, userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["SkillCooldown1"] = userinfo["SkillCooldown1"] + 1 
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown1"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		# Done
		elif answer2 == "distort" or answer2 == "Distort":
			# Distorts the enemy for 50% less dmg. 2 turns cooldown.
			
			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0 
			# Move user makes
			move = "Distort"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]
			
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0

				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0

				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns Distort had no use.**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			elif userinfo["Buff1"] == "Warp" and userinfo["Buff1Time"] > 0:

				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# set skill cooldown
				userinfo["SkillCooldown1"] = 3
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, But {} has warp debuff.\n the enemy damage is 0.**\n**{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"],  userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["SkillCooldown1"] == 0:
				enemydmg = int((enemydmg / 100) * 50)

				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				# set skill cooldown
				userinfo["SkillCooldown1"] = 3
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, halving the damage**\n**{} hits {} for {} damage**\n**{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], userinfo["name"], enemydmg,  userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["SkillCooldown1"] = userinfo["SkillCooldown1"] + 1 
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown1"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return	
				

		# Done
		elif answer2 == "reap" or answer2 == "Reap":
			# Reaps the enemy of 30% their Hp and adds it to their own health!

			# Move user makes
			move = "Reap"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			
			
			if userinfo["EnemyStun"] > 0:

				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			elif userinfo["Buff1"] == "Arise" and userinfo["Buff1Time"] > 0 and userinfo["SkillCooldown1"] == 0:
				# takes 30% of enemyhp 
				reap = int((enemyhp / 100) * 30)
				# Fixs enemy hp
				enemyhp = enemyhp - reap

				hit = int((youdmg / 100) * 25)
				

				# deals dmg to enemy
				totaldmg = hit + hit + hit + hit + hit
				enemyhp = enemyhp - totaldmg - youdmg
				# Adds 25% enemy hp to user
				userhealth += reap
				if userhealth >= userinfo["MaxHealth"]:
					userhealth = userinfo["MaxHealth"]
			
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# Set skill cooldown.
				userinfo["SkillCooldown1"] = 3
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and 30% of {} Health.\n{} Hp healed! The army of skeletons attacks.\nDealing {} damage each\nDealing a total of {} damage.\n{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], reap, hit, totaldmg, userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["SkillCooldown1"] == 0:
				# takes 30% of enemyhp 
				reap = int((enemyhp / 100) * 30)
				# Fixs enemy hp
				enemyhp = enemyhp - reap
				if enemyhp < 0:
					enemyhp = 0
				# Adds 25% enemy hp to user
				userhealth += reap
				if userhealth >= userinfo["MaxHealth"]:
					userhealth = userinfo["MaxHealth"]
				# Set skill cooldown.
				userinfo["SkillCooldown1"] = 3
				em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Reaps 30% of {} Health.\n{} Hp healed!**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], userinfo["selected_enemy"], reap, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em3.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em3)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
						
			else:
				userinfo["SkillCooldown1"] = userinfo["SkillCooldown1"] + 1 
				if userinfo["Buff1"] == "Arise" and userinfo["Buff1Time"] > 0:
					userinfo["Buff1Time"] += 1
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown1"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return	

		# Done
		elif answer2 == "overload" or answer2 == "Overload":
			# Overload Causes to deal 40% extra dmg to enemies but damages the user 50% of overload damage.

			# Move user makes
			move = "overload"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]
			
		

		
			if userinfo["EnemyStun"] > 0:
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			
			elif userinfo["Buff1"] == "Surge":

				enemyhp = userinfo["enemyhp"]
				# user dmg 
				userhealth = userhealth - enemydmg

				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**you have been stunned for 1 turn**\n**{} Hits {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["SkillCooldown1"] == 0:
				overloaddmg = int((youdmg / 100) * 40)
				
				
				overloadselfdmg = int((overloaddmg / 100) * 50)
				

				youdmg += overloaddmg
				enemydmg += overloadselfdmg
				userhealth = userhealth - enemydmg - overloadselfdmg 
				enemyhp = userinfo["enemyhp"] - youdmg

				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# Set skill cooldown.
				userinfo["SkillCooldown1"] = 2
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} overloads {} for {} damage\nBut also deals {} self damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, overloadselfdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["SkillCooldown1"] = userinfo["SkillCooldown1"] + 1 
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown1"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return	
		# done
		elif answer2 == "fusillade" or answer2 == "Fusillade":
			# Fusillade deals a series hits 3x 50% original damage doing 150% dmg total


			# Move user makes
			move = "fusillade"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0

				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			if userinfo["Buff1"] == "Blockade":
				
				# debuff
				youdmg = int((youdmg / 100) * 85)
				hit = int((youdmg / 100) * 50)
				# deals dmg to enemy
				totaldmg = hit + hit + hit
				enemyhp = enemyhp - totaldmg
				# Users Defense
				youdef = youdef * 2
				enemydmg -= youdef	
				
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# Set skill cooldown.
				userinfo["SkillCooldown2"] = 5
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has the blockade buff doubling defense.\n{} hits {} for {} damage**\n**{} uses {} and does a series of hits.**\n**Dealing {} damage each**\n**Dealing a total of {} damage.**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, hit, totaldmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["SkillCooldown1"] == 0:
				hit = int((youdmg / 100) * 50)
				

				# deals dmg to enemy
				totaldmg = hit + hit + hit
				enemyhp = enemyhp - totaldmg
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# Set skill cooldown.
				userinfo["SkillCooldown1"] = 4
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and does a series of hits.**\n**Dealing {} damage each**\n**Dealing a total of {} damage.**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, hit, totaldmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			
			else:
				userinfo["SkillCooldown1"] = userinfo["SkillCooldown1"] + 1 
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown1"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return	

# done
		elif answer2 == "protrude" or answer2 == "Protrude":
			# Protrude Deals a critical strike to the enemy core dealing 140% damage.

			# Move user makes
			move = "Protrude"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]
			
			if userinfo["EnemyStun"] > 0:
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			elif userinfo["Buff1"] == "Slice":

				enemyhp = userinfo["enemyhp"]
				# Bleeding dmg
				bleeding = int((enemyhp / 100) * 25)
				youdmg = int((youdmg / 100) * 140)
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg - bleeding
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0

				bufftime = userinfo["Buff1Time"]
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n {} Has bleeding effect for {} turns.**\n**{} uses {}  and has a Critical hit! for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], bufftime, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["SkillCooldown1"] == 0:
				youdmg = int((youdmg / 100) * 140)
				
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# Set skill cooldown.
				userinfo["SkillCooldown1"] = 3
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and has a Critical hit! for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				userinfo["SkillCooldown1"] = userinfo["SkillCooldown1"] + 1 
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown1"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return	

# done
		elif answer2 == "strike" or answer2 == "Strike":
			# Strike Deals a critical hit to the knee immobilizing them for 2 turns while dealing 50% damage. has a 6 turn cooldown.

			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0 
			# Move user makes
			move = "Strike"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			# Acutal fight msg.
			if userinfo["SkillCooldown1"] == 0:
				youdmg = int((youdmg / 100) * 50)
				userinfo["EnemyStun"] = 3
				
				stun = 2
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# Set skill cooldown.
				userinfo["SkillCooldown1"] = 6
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turns\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], stun, userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["SkillCooldown1"] = userinfo["SkillCooldown1"] + 1 
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown1"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

# done
		elif answer2 == "corrupt" or answer2 == "Corrupt":
			# Corrupts the enemy for 2 turns taking 30% damage extra, or ends when enemy dies. 4 turn cooldown.

			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0 
			# Move user makes
			move = "Corrupt"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If enemydmg is lower then 0 its 0
			if enemydmg < 0:
				enemydmg = 0
			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			# Acutal fight msg.
			if userinfo["SkillCooldown1"] == 0:
				# add buff and timer
				userinfo["Buff1"] = "Corrupt"
				userinfo["Buff1Time"] = 2
				# Corrupt dmg
				
				youdmg = int((youdmg / 100) * 130)
				bufftime = 2
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# Set skill cooldown.
				userinfo["SkillCooldown1"] = 4
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and corrupts {} for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["SkillCooldown1"] = userinfo["SkillCooldown1"] + 1 
				userinfo["Buff1Time"] = userinfo["Buff1Time"] + 1
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown1"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return


		elif answer2 == "Rupture" or answer2 == "rupture":
			# Rupture the enemy's artery 2 turns dealing 25% current hp bleeding dmg.  4 turn cooldown.

			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0 
			# Move user makes
			move = "Rupture"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If enemydmg is lower then 0 its 0
			if enemydmg < 0:
				enemydmg = 0
			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			# Acutal fight msg.
			if userinfo["SkillCooldown2"] == 0:
				# add buff and timer
				userinfo["Buff1"] = "Rupture"
				userinfo["Buff1Time"] = 2
			
				# Bleeding dmg
				bleeding = int((enemyhp / 100) * 25)
				# Bleeding time
				bufftime = 2
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg - bleeding
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# Set skill cooldown.
				userinfo["SkillCooldown2"] = 4
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and Ruptures {} artery\n causing bleeding effect for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["SkillCooldown2"] = userinfo["SkillCooldown2"] + 1 
				userinfo["Buff1Time"] = userinfo["Buff1Time"] + 1
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown2"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		elif answer2 == "Warp" or answer2 == "warp":
			# Warp the enemy's attacks for 2 turns dealing 60% Less damage.  5 turn cooldown.

			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0 
			# Move user makes
			move = "Warp"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			# Acutal fight msg.
			if userinfo["SkillCooldown2"] == 0:
				# add buff and timer
				userinfo["Buff1"] = "Warp"
				userinfo["Buff1Time"] = 2
			
				enemydmg = int((enemydmg / 100) * 60)

				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = userinfo["enemyhp"] - youdmg
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg 
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# Set skill cooldown.
				userinfo["SkillCooldown2"] = 5
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, Warping {} Attack dealing 60% less damage**\n**{} hits {} for {} damage**\n**{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], userinfo["selected_enemy"], userinfo["name"], enemydmg,  userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				userinfo["SkillCooldown2"] = userinfo["SkillCooldown2"] + 1 
				userinfo["Buff1Time"] = userinfo["Buff1Time"] + 1
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown2"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
		

		elif answer2 == "Arise" or answer2 == "arise":
			# Arise A small army of 5 Skeletons dealing 30% your dmg for 2 turns, Has a 5 turn cooldown 


			# Move user makes
			move = "Arise"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			
			if userinfo["EnemyStun"] > 0:
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			
			elif userinfo["SkillCooldown2"] == 0:
				hit = int((youdmg / 100) * 25)
				

				# deals dmg to enemy
				totaldmg = hit + hit + hit + hit + hit
				enemyhp = enemyhp - totaldmg - youdmg
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# set buff
				userinfo["Buff1"] = "Arise"
				userinfo["Buff1Time"] = 2
				# Set skill cooldown.
				userinfo["SkillCooldown2"] = 8
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and Raises a small army of skeletons!.**\n**Dealing {} damage each**\n**Dealing a total of {} damage.\n{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, hit, totaldmg, userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				userinfo["SkillCooldown2"] = userinfo["SkillCooldown2"] + 1 
				userinfo["Buff1Time"] = userinfo["Buff1Time"] + 1
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown2"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return	
			

		elif answer2 == "Surge" or answer2 == "surge":
			# Surge Causes the user to get a massice power surge dealing 3 times normal damage but stunning themself after the attack for 1 turn.

			# Move user makes
			move = "Surge"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			
			if userinfo["EnemyStun"] > 0:
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			
			elif userinfo["SkillCooldown2"] == 0:
				
				

				youdmg = youdmg * 3
			
				userhealth = userhealth - enemydmg 
				enemyhp = userinfo["enemyhp"] - youdmg

				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# Set skill cooldown.
				userinfo["SkillCooldown2"] = 4
				userinfo["Buff1"] = "Surge"
				userinfo["Buff1Time"] = 2
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} gains a power surge and triples their damage.\n total damage {}Hp\nBut stun yourself for 1 turn.**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], youdmg,   userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["SkillCooldown2"] = userinfo["SkillCooldown2"] + 1 
				userinfo["Buff1Time"] = userinfo["Buff1Time"] + 1
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown2"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return	


		elif answer2 == "Slice" or answer2 == "slice":
			# SLice causes 2 round bleeding effect(25% current health), 30% increased damage 4 turn cooldown.
			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0 
			# Move user makes
			move = "Slice"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef	
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If enemydmg is lower then 0 its 0
			if enemydmg < 0:
				enemydmg = 0
			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			# Acutal fight msg.
			if userinfo["SkillCooldown2"] == 0:
				# add buff and timer
				userinfo["Buff1"] = "Slice"
				userinfo["Buff1Time"] = 2
				# crit
				youdmg += int((youdmg / 100) * 30)
				# Bleeding dmg
				bleeding = int((enemyhp / 100) * 25)
				# Bleeding time
				bufftime = 2
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg - bleeding
				
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# Set skill cooldown.
				userinfo["SkillCooldown2"] = 4
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and Slices {}\n causing bleeding effect for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["SkillCooldown2"] = userinfo["SkillCooldown2"] + 1 
				userinfo["Buff1Time"] = userinfo["Buff1Time"] + 1
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown2"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return


		elif answer2 == "Blockade" or answer2 == "blockade":
			# Blockade Dubbles your armor for 2 turns! dealing 15% less damage. 5 turn cooldown.
			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0 
			# Move user makes
			move = "Blockade"
			# Users HP
			userhealth = userinfo["health"]
			
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If enemydmg is lower then 0 its 0
			if enemydmg < 0:
				enemydmg = 0
			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			# Acutal fight msg.
			if userinfo["SkillCooldown2"] == 0:
				# add buff and timer
				userinfo["Buff1"] = "Blockade"
				userinfo["Buff1Time"] = 2
				# debuff
				youdmg = int((youdmg / 100) * 85)
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg 
				# Users Defense
				youdef = youdef * 2
				enemydmg -= youdef	
				
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# user dmg 
				userhealth = userhealth - enemydmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# Set skill cooldown.
				userinfo["SkillCooldown2"] = 5
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and Dubbles their defense for 2 turns.\n{} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["SkillCooldown2"] = userinfo["SkillCooldown2"] + 1 
				userinfo["Buff1Time"] = userinfo["Buff1Time"] + 1
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown2"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		elif answer2 == "Sneak" or answer2 == "sneak":
			# Sneak around your enemy and delivering a critical hit dealing 150% and not taking any dmg! 4 turn cooldown.
			# If enemy stunned no dmg
			if userinfo["EnemyStun"] > 0:
				enemydmg = 0 
			# Move user makes
			move = "Sneak"
			# Users HP
			userhealth = userinfo["health"]
			
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If enemydmg is lower then 0 its 0
			if enemydmg < 0:
				enemydmg = 0
			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]


			if userinfo["SkillCooldown2"] == 0:
				youdmg = int((youdmg / 100) * 150)
				
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg
				# user dmg 
				userhealth = userhealth - enemydmg
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# Set skill cooldown.
				userinfo["SkillCooldown2"] = 4
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and comes out the shadows.\nYou deal a critical hit! for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				userinfo["SkillCooldown2"] = userinfo["SkillCooldown2"] + 1 
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown2"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return	

		elif answer2 == "Snipe" or answer2 == "snipe":
			# Snipe your enemy from afer taking no damage but headshotting the enemy dealing 250% of your base dmg. 6 turn cooldown.
			# Move user makes
			move = "Snipe"
			# Users HP
			userhealth = userinfo["health"]
			
			# Enemy Hp
			enemyhp = userinfo["enemyhp"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]


			if userinfo["SkillCooldown2"] == 0:
				youdmg = int((youdmg / 100) * 250)
				
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg
				

				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# Set skill cooldown.
				userinfo["SkillCooldown2"] = 5
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and headshots {}.\nYou deal a critical hit! for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				userinfo["SkillCooldown2"] = userinfo["SkillCooldown2"] + 1 
				em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown2"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return	




		elif answer2 == "heal" or answer2 == "Heal":
			battleinfo = db.battles.find_one({"_id": user.id})
			if battleinfo["battle_active"] == "True":
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["heal"]["inbattle"]["translation"])
				return
			else:
				await _heal_reaction(user, skillmsg)
				return

		else:
			return

		await asyncio.sleep(0.4)
		if userhealth >= userinfo["MaxHealth"]:
			userhealth = userinfo["MaxHealth"]
		userinfo["EnemyStun"] = userinfo["EnemyStun"] - 1
		if userinfo["EnemyStun"] <= 0:
			userinfo["EnemyStun"] = 0
		userinfo["SkillCooldown1"] = userinfo["SkillCooldown1"] - 1
		if userinfo["SkillCooldown1"] <= 0:
			userinfo["SkillCooldown1"] = 0
		userinfo["SkillCooldown2"] = userinfo["SkillCooldown2"] - 1
		if userinfo["SkillCooldown2"] <= 0:
			userinfo["SkillCooldown2"] = 0
		if not userinfo["Buff1"] == "None":
			userinfo["Buff1Time"] = userinfo["Buff1Time"] - 1
		if userinfo["Buff1Time"] <= 0:
			userinfo["Buff1"] = "None"
			userinfo["Buff1Time"] = 0
		
		userinfo["health"] = userhealth
		userinfo["enemyhp"] = enemyhp

		if enemyhp <= 0 and userhealth <= 0:
			em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["bothdied"]["translation"].format(userinfo["name"], goldlost), color=discord.Colour(0x000000))
			await ctx.send(embed=em)
			userinfo["gold"] = userinfo["gold"] - goldlost
			if userinfo["gold"] < 0:
				userinfo["gold"] = 0
			if userinfo["health"] < 0:
				userinfo["health"] = 0
			if userinfo["Buff1"] == "Corrupt":
				userinfo["Buff1"] = "None"
				userinfo["Buff1Time"] = 0
			userinfo["health"] = 0
			userinfo["selected_enemy"] = "None"
			userinfo["enemydifficulty"] = "None"
			userinfo["enemieskilled"] = userinfo["enemieskilled"] + 1
			userinfo["deaths"] = userinfo["deaths"] + 1
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

		elif userhealth <= 0:
			em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["playerdied"]["translation"].format(userinfo["selected_enemy"], userinfo["name"], userinfo["name"], goldlost), color=discord.Colour(0xff0000))
			await ctx.send(embed=em)
			userinfo["gold"] = userinfo["gold"] - goldlost
			if userinfo["gold"] < 0:
				userinfo["gold"] = 0
			if userinfo["health"] < 0:
				userinfo["health"] = 0
			if userinfo["Buff1"] == "Corrupt":
				userinfo["Buff1"] = "None"
				userinfo["Buff1Time"] = 0
			userinfo["selected_enemy"] = "None"
			userinfo["enemydifficulty"] = "None"
			userinfo["deaths"] = userinfo["deaths"] + 1
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

		elif enemyhp <= 0:
			

			try: 
				goose_bonus_text = "" 
				for i in userinfo["pet_list"]:
					petinfo = i
					pet_level = petinfo["level"]
					pet_type = petinfo["type"]

					if pet_type == "Goose":
						if pet_level <= 10:
							enemygold = enemygold + (int((enemygold / 100) * 5))
							goose_bonus_text = "\n<:Gold:639484869809930251> 5% Goose gold bonus."
						elif pet_level <= 20:
							enemygold = enemygold + (int((enemygold / 100) * 10))
							goose_bonus_text = "\n<:Gold:639484869809930251> 10% Goose gold bonus."
						elif pet_level <= 30:
							enemygold = enemygold + (int((enemygold / 100) * 15))
							goose_bonus_text = "\n<:Gold:639484869809930251> 15% Goose gold bonus."
						elif pet_level <= 40:
							enemygold = enemygold + (int((enemygold / 100) * 20))
							goose_bonus_text = "\n<:Gold:639484869809930251> 20% Goose gold bonus."
						elif pet_level <= 50:
							enemygold = enemygold + (int((enemygold / 100) * 25))
							goose_bonus_text = "\n<:Gold:639484869809930251> 25% Goose gold bonus."
						elif pet_level >= 51:
							enemygold = enemygold + (int((enemygold / 100) * 30))
							goose_bonus_text = "\n<:Gold:639484869809930251> 30% Golden Goose gold bonus."
			except:
				pass
					

			if userinfo["party"] != "None":
				partyinfo = db.party.find_one({"_id": userinfo["party"]})
				party_reward_list = " " 
				for i in range(partyinfo["amount"]):
					
					shared_gold = 0
					shared_xpgain = 0
					friend_id = partyinfo["members"][i]
					friend_info = db.users.find_one({"_id": friend_id})
		
					if friend_info["role"] == "Player":
						shared_gold = (int((enemygold / 100) * 10))
						shared_xpgain = (int((xpgain / 100) * 10))

					if friend_info["role"] == "Developer":
						shared_gold = (int((enemygold / 100) * 10))
						shared_xpgain = (int((xpgain / 100) * 10))

					if friend_info["role"] == "patreon1":
						shared_gold = (int((enemygold / 100) * 15))
						shared_xpgain = (int((xpgain / 100) * 15))

					if friend_info["role"] == "patreon2":
						shared_gold = (int((enemygold / 100) * 20))
						shared_xpgain = (int((xpgain / 100) * 20))

					if friend_info["role"] == "patreon3":
						shared_gold = (int((enemygold / 100) * 25))
						shared_xpgain = (int((xpgain / 100) * 25))

					if friend_info["role"] == "patreon4":
						shared_gold = (int((enemygold / 100) * 30))
						shared_xpgain = (int((xpgain / 100) * 30))

					

					friend_info["gold"] = friend_info["gold"] + shared_gold
					friend_info["exp"] = friend_info["exp"] + shared_xpgain
					
				

					flist = ("**{}**: <:Gold:639484869809930251>{}  Shared gold, :sparkles: {} Shared Exp\n".format(friend_info["name"], int(shared_gold), int(shared_xpgain)))

					party_reward_list += flist
					
					if friend_info["exp"] >= 100 + ((friend_info["lvl"] + 1) * 3.5):
						friend_info["exp"] = friend_info["exp"] - (100 + ((friend_info["lvl"] + 1) * 3.5))
						friend_info["lvl"] = friend_info["lvl"] + 1
						friend_info["health"] = friend_info["MaxHealth"]
						em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(friend_info["name"]), color=discord.Colour(0xffd700))
						await ctx.send(embed=em)	
					
						db.users.replace_one({"_id": friend_id}, friend_info, upsert=True)


					if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
						userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
						userinfo["lvl"] = userinfo["lvl"] + 1
						userinfo["health"] = userinfo["MaxHealth"]
						em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
						await ctx.send(embed=em)

				try:
					em2 = discord.Embed(description=":dagger:{} Killed the {}\n<:PvP:573580993055686657>The Party gets \n {}".format(userinfo["name"], userinfo["selected_enemy"], party_reward_list), color=discord.Colour(0x00ff00))
					em2.set_footer(text="Want more shared bonus? become a patreon!")
					await ctx.send(embed=em2)
				except Exception as e: 
					print(e)
					pass

			
			if userinfo["Buff1"] == "Corrupt":
				userinfo["Buff1"] = "None"
				userinfo["Buff1Time"] = 0

			if userinfo["selected_enemy"] == "Oofer":
				try:
					mission = "Kill 100 Oofers"
					add = 1
					await _guild_mission_check(self, user, mission, guild, add)
				except:
					
					pass

				if userinfo["questname"] == "Oofer I":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user)
					pass

			elif userinfo["selected_enemy"] == "Goblin":
				try:
					mission = "Kill 100 Goblins"
					add = 1
					await _guild_mission_check(self, user, mission, guild, add)
				except:
					print("Error while trying to check '" + mission + "' mission")
					pass


			elif userinfo["selected_enemy"] == "Rachi":
				try:
					userinfo["Rachikilled"] = userinfo["Rachikilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

				if userinfo["questname"] == "Rachi I":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user)
					pass
					
			elif userinfo["selected_enemy"] == "Draugr":
				try:
					userinfo["Draugrkilled"] = userinfo["Draugrkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

				if userinfo["questname"] == "Draugr I":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user)
					pass

			elif userinfo["selected_enemy"] == "Debin":
				try:
					userinfo["Debinkilled"] = userinfo["Debinkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

				if userinfo["questname"] == "Debin I":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user)
					pass

			elif userinfo["selected_enemy"] == "Stalker":
				try:
					userinfo["Stalkerkilled"] = userinfo["Stalkerkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

				if userinfo["questname"] == "Stalker I":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user)
					pass


			elif userinfo["selected_enemy"] == "Fire Golem":
				try:
					userinfo["FireGolemkilled"] = userinfo["FireGolemkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass
				if userinfo["role"] == "Developer":
					pet_spawn = 99
					# random.randint(99, 99)

					if pet_spawn == 99:

						if userinfo["pet_stage"] == "Golden Goose":
							em = discord.Embed(title="A pet!", description="a tameable pet has spawned!, its a goose.\n to tame it type {}pet tame".format(ctx.prefix), color=discord.Colour(0xff0000))
							em.set_image(url="")
							await ctx.send(embed=em)
							userinfo["pet_find"] = "Golden Goose"
							userinfo["pet_stage"] = "Fox"
							db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
								
						
				if userinfo["questname"] == "Fire Golem I":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 5:
						await _quest_check(self, ctx, user)
					pass

			elif userinfo["selected_enemy"] == "Wyvern":
				try:
					userinfo["Wyvernkilled"] = userinfo["Wyvernkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

				if userinfo["questname"] == "Wyvern I":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user)
					pass

				elif userinfo["questname"] == "On the hunt!" and userinfo["enemydifficulty"] == "Rare":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user)
					pass

			elif userinfo["selected_enemy"] == "Oofer":
				try:
					userinfo["Ooferkilled"] = userinfo["Ooferkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

				if userinfo["questname"] == "Oofer I":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user)
					pass

			elif userinfo["selected_enemy"] == "Souleater":
				try:
					userinfo["Souleaterkilled"] = userinfo["Souleaterkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

				if userinfo["questname"] == "Souleater I":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user)
					pass

			elif userinfo["selected_enemy"] == "Wolf":
				try:
					userinfo["Wolfkilled"] = userinfo["Wolfkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Goblin":
				try:
					userinfo["Goblinkilled"] = userinfo["Goblinkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Zombie":
				try:
					userinfo["Zombiekilled"] = userinfo["Zombiekilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Phantasm":
				try:
					userinfo["Phantasmkilled"] = userinfo["Phantasmkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

				if userinfo["role"] == "Developer":
					pet_spawn = 99
					# random.randint(99, 99)

					if pet_spawn == 99:

						if userinfo["pet_stage"] == "Fox":
							em = discord.Embed(title="A pet!", description="a tameable pet has spawned!, its a fox.\n to tame it type {}pet tame".format(ctx.prefix), color=discord.Colour(0xff0000))
							em.set_image(url="")
							await ctx.send(embed=em)
							userinfo["pet_find"] = "Fox"
							userinfo["pet_stage"] = "Polar Bear"
							db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				
			elif userinfo["selected_enemy"] == "The Corrupted":
				try:
					userinfo["TheCorruptedkilled"] = userinfo["TheCorruptedkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

				if userinfo["questname"] == "The Corrupted I":
					userinfo["questprogress"] = userinfo["questprogress"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True) 
					if userinfo["questprogress"] >= 5:
						await _quest_check(self, ctx, user)
					pass

				if userinfo["role"] == "Developer":
					pet_spawn = 99
					# random.randint(99, 99)

					if pet_spawn == 99:


						if userinfo["pet_stage"] == "Polar Bear":
							em = discord.Embed(title="A pet!", description="a tameable pet has spawned!, its a polar bear.\n to tame it type {}pet tame".format(ctx.prefix), color=discord.Colour(0xff0000))
							em.set_image(url="")
							await ctx.send(embed=em)
							userinfo["pet_find"] = "Polar Bear"
							userinfo["pet_stage"] = "Small Cerberus"
							db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

						

			elif userinfo["selected_enemy"] == "The Accursed":
				try:
					userinfo["TheAccursedkilled"] = userinfo["TheAccursedkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			
				if userinfo["role"] == "Developer":
					pet_spawn = 99
					# random.randint(99, 99)

					if pet_spawn == 99:
			
						if userinfo["pet_stage"] == "Small Cerberus":
							em = discord.Embed(title="A pet!", description="a tameable pet has spawned!, its a small cerberus.\n to tame it type {}pet tame".format(ctx.prefix), color=discord.Colour(0xff0000))
							em.set_image(url="")
							await ctx.send(embed=em)
							userinfo["pet_find"] = "Small Cerberus"
							userinfo["pet_stage"] = "None"
							db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

			elif userinfo["selected_enemy"] == "Elder Dragon":
				try:
					userinfo["ElderDragonkilled"] = userinfo["ElderDragonkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Hades":
				try:
					userinfo["Hadeskilled"] = userinfo["Hadeskilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Ebony Guardian":
				try:
					userinfo["EbonyGuardiankilled"] = userinfo["EbonyGuardiankilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Harpy":
				try:
					userinfo["Harpykilled"] = userinfo["Harpykilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Dormammu":
				try:
					userinfo["Dormammukilled"] = userinfo["Dormammukilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Ettin":
				try:
					userinfo["Ettinkilled"] = userinfo["Ettinkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "The Nameless King":
				try:
					userinfo["TheNamelessKingkilled"] = userinfo["TheNamelessKingkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Largos":
				try:
					userinfo["Largoskilled"] = userinfo["Largoskilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Death Claw":
				try:
					userinfo["Deathclawilled"] = userinfo["Deathclawilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Saurian":
				try:
					userinfo["Sauriankilled"] = userinfo["Sauriankilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "The venemous":
				try:
					userinfo["TheVenomouskilled"] = userinfo["TheVenomouskilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Skeleton":
				try:
					userinfo["Skeletonkilled"] = userinfo["Skeletonkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Lizardmen":
				try:
					userinfo["Lizardmenkilled"] = userinfo["Lizardmenkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Giant":
				try:
					userinfo["Giantkilled"] = userinfo["Giantkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Death Knight":
				try:
					userinfo["DeathKnightkilled"] = userinfo["DeathKnightkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Ice Wolves":
				try:
					userinfo["IceWolveskilled"] = userinfo["IceWolveskilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Frost Orc":
				try:
					userinfo["FrostOrckilled"] = userinfo["FrostOrckilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Frost Goblin":
				try:
					userinfo["FrostGoblinkilled"] = userinfo["FrostGoblinkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass

			elif userinfo["selected_enemy"] == "Frost Dragon":
				try:
					userinfo["FrostDragonkilled"] = userinfo["FrostDragonkilled"] + 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass
			
			em = discord.Embed(description=":dagger: {} killed the {}\n<:GoldBars:573781770709893130> {} gained {} gold{}\n:sparkles: {} gained {} experience".format(userinfo["name"], userinfo["selected_enemy"], userinfo["name"], int(enemygold), goose_bonus_text, userinfo["name"], xpgain), color=discord.Colour(0x00ff00))
			em.set_footer(text="want more benefits, become a patreon!")
			await ctx.send(embed=em)	


			userinfo["selected_enemy"] = "None"
			userinfo["enemydifficulty"] = "None"
			userinfo["gold"] = userinfo["gold"] + int(enemygold)
			userinfo["exp"] = userinfo["exp"] + xpgain
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

			if lootbag == 2:
				userinfo = db.users.find_one({"_id": user.id})
				em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["crate"]["translation"].format(userinfo["name"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				userinfo["lootbag"] = userinfo["lootbag"] + 1
			elif lootbag == 1:
				userinfo = db.users.find_one({"_id": user.id})
				em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["key"]["translation"].format(userinfo["name"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				userinfo["keys"] = userinfo["keys"] + 1

			
			userinfo["enemieskilled"] = userinfo["enemieskilled"] + 1
		db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
		try:
			await _level_up_check_user(self, ctx, user)
		except:
			return
		


def setup(bot):
	n = fight(bot)
	bot.add_cog(n)