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

		if userinfo["questname"] == "Basic C":
			userinfo["questprogress"] += 1	
			if userinfo["questprogress"] >= 1:
				await _quest_check(self, ctx, user, userinfo)
			pass

		if userinfo["questname"] == "Fight I":
			userinfo["questprogress"] += 1
			if userinfo["questprogress"] >= 25:
				await _quest_check(self, ctx, user, userinfo)
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
			chance = random.randint(1, 100)
			if userinfo["location"] == "Golden Temple":
				if chance >= 90:
					debi = randchoice(["Fire Golem"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Wyvern"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Rachi", "Debin", "Oofer"])

			elif userinfo["location"] == "Saker Keep":
				if chance >= 90:
					debi = randchoice(["The Corrupted"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Souleater"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Draugr", "Stalker"])
		
			elif userinfo["location"] == "The Forest":
				if chance >= 90:
					debi = randchoice(["Phantasm"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Zombie"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Wolf", "Goblin"])
				
			elif userinfo["location"] == "Ebony Mountains":
				if chance >= 90:
					debi = randchoice(["The Accursed"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Ebony Guardian"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Elder Dragon", "Hades"])

			elif userinfo["location"] == "Township of Arkina":
				if chance >= 90:
					debi = randchoice(["The Nameless King"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Harpy"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Ettin", "Dormammu"])

			elif userinfo["location"] == "Zulanthu":
				if chance >= 90:
					debi = randchoice(["The Venomous"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Largos"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Saurian", "Deathclaw"])

			elif userinfo["location"] == "Lost City":
				if chance >= 90:
					debi = randchoice(["Death Knight"])
				elif 90 >= chance >= 60:
					debi = randchoice(["Giant"])
				elif 60 >= chance >= 0:
					debi = randchoice(["Skeleton", "Lizardmen"])
				
			elif userinfo["location"] == "Drenheim":
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
			em = discord.Embed(title="You wandered around {} and found\n{}".format(userinfo["location"], enemyname), description="Would you like to fight it?", color=discord.Colour(0xffffff))
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

			if userinfo["role"] == "Developer":
				eventinfo = db.users.find_one({ "_id": 387317544228487168 })
				if eventinfo["Gortac"] == True:
					eventspawn = random.randint(1, 100)
					if eventspawn >= 90:
						enemyname = "Gortac the Indestructible"
						userinfo["selected_enemy"] = "Gortac the Indestructible"
						debi = "Gortac"
						em = discord.Embed(title="You wandered around {} and found\n{}".format(userinfo["location"], enemyname), description="Would you like to fight it?", color=discord.Colour(0xffffff))
						em.set_footer(text="yes / no")
			await ctx.send(embed=em)

			options = ["y", "Y", "yes", "Yes", "n", "N", "No", "no", "-fight"]
			answer1 = await self.check_answer(ctx, options)
			
			if answer1 == "y" or answer1 == "Y" or answer1 == "Yes" or answer1 == "yes":
				userinfo["selected_enemy"] = debi
				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

				if userinfo["selected_enemy"] == "Rachi" or userinfo["selected_enemy"] == "Debin" or userinfo["selected_enemy"] == "Oofer": 
					userinfo["enemyhp"] = random.randint(10, 30)
				elif userinfo["selected_enemy"] == "Wyvern":
					userinfo["enemyhp"] = random.randint(30, 50)
				elif userinfo["selected_enemy"] == "Fire Golem":
					userinfo["enemyhp"] = random.randint(40, 60)
				elif userinfo["selected_enemy"] == "Draugr" or userinfo["selected_enemy"] == "Stalker":
					userinfo["enemyhp"] = random.randint(20, 40)
				elif userinfo["selected_enemy"] == "Souleater":
					userinfo["enemyhp"] = random.randint(40, 60)
				elif userinfo["selected_enemy"] == "The Corrupted":
					userinfo["enemyhp"] = random.randint(40, 60)
				elif userinfo["selected_enemy"] == "Wolf" or userinfo["selected_enemy"] == "Goblin":
					userinfo["enemyhp"] = random.randint(50, 70)
				elif userinfo["selected_enemy"] == "Zombie":
					userinfo["enemyhp"] = random.randint(60, 80)
				elif userinfo["selected_enemy"] == "Phantasm":
					userinfo["enemyhp"] = random.randint(70, 90)
				elif userinfo["selected_enemy"] == "Elder Dragon" or userinfo["selected_enemy"] == "Hades":
					userinfo["enemyhp"] = random.randint(70, 90)
				elif userinfo["selected_enemy"] == "Ebony Guardian":
					userinfo["enemyhp"] = random.randint(80, 100)
				elif userinfo["selected_enemy"] == "The Accursed":
					userinfo["enemyhp"] = random.randint(90, 110)
				elif userinfo["selected_enemy"] == "Ettin" or userinfo["selected_enemy"] == "Dormammu":
					userinfo["enemyhp"] = random.randint(90, 110)
				elif userinfo["selected_enemy"] == "Harpy":
					userinfo["enemyhp"] = random.randint(100, 120)
				elif userinfo["selected_enemy"] == "The Nameless King":
					userinfo["enemyhp"] = random.randint(110, 130)
				elif userinfo["selected_enemy"] == "Saurian" or userinfo["selected_enemy"] == "Deathclaw":
					userinfo["enemyhp"] = random.randint(90, 110)
				elif userinfo["selected_enemy"] == "Largos":
					userinfo["enemyhp"] = random.randint(100, 120)
				elif userinfo["selected_enemy"] == "The Venomous":
					userinfo["enemyhp"] = random.randint(110, 130)
				elif userinfo["selected_enemy"] == "Skeleton" or userinfo["selected_enemy"] == "Lizardmen":
					userinfo["enemyhp"] = random.randint(120, 140)
				elif userinfo["selected_enemy"] == "Giant":
					userinfo["enemyhp"] = random.randint(130, 150)
				elif userinfo["selected_enemy"] == "Death Knight":
					userinfo["enemyhp"] = random.randint(140, 160)
				elif userinfo["selected_enemy"] == "Ice Wolves" or userinfo["selected_enemy"] == "Frost Goblin":
					userinfo["enemyhp"] = random.randint(150, 170)
				elif userinfo["selected_enemy"] == "Frost Orc":
					userinfo["enemyhp"] = random.randint(160, 180)
				elif userinfo["selected_enemy"] == "Frost Dragon":
					userinfo["enemyhp"] = random.randint(170, 190)

				uncommon = (int((userinfo["enemyhp"] / 100) * 20))
				rare = (int((userinfo["enemyhp"] / 100) * 30))
				legendary = (int((userinfo["enemyhp"] / 100) * 40))
				mythical = (int((userinfo["enemyhp"] / 100) * 50))
					
				if userinfo["enemydifficulty"] == "Uncommon":
					userinfo["enemyhp"] += uncommon
				elif userinfo["enemydifficulty"] == "Rare":
					userinfo["enemyhp"] += rare
				elif userinfo["enemydifficulty"] == "Legendary":
					userinfo["enemyhp"] += legendary
				elif userinfo["enemydifficulty"] == "Mythical":
					userinfo["enemyhp"] += mythical

				elif userinfo["selected_enemy"] == "Gortac the Indestructible":
					# define hp
					minhp = (int(userinfo["MaxHealth"] * 4))
					maxhp = (int(userinfo["MaxHealth"] * 4)) + userinfo["MaxHealth"]
					userinfo["enemyhp"] = random.randint(minhp, maxhp)
					# define enemydmg
					mindmg = userinfo["equip"]["stats_min"]
					maxdmg = userinfo["equip"]["stats_max"]
					bossdmg = random.randint(mindmg, maxdmg)
					enemydmg = (int((bossdmg / 100) * 120))
					# define loot
					enemygold = 0
					xpgain = 0
					goldlost = 0

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
		polar_bear_bonus = 0
		polar_bear_bonus_text = ""
		small_cerberus_bonus = 0
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

		for i in userinfo["pet_list"]:
			petinfo = i
			pet_name = petinfo["name"]
			pet_level = petinfo["level"]
			pet_type = petinfo["type"]
			if pet_type == "Polar Bear":
				if pet_level <= 10:
					polar_bear_bonus = (int((youdmg / 100) * 5))
					polar_bear_bonus_text = "\n{} hits for {}.".format(pet_name, polar_bear_bonus)
				elif pet_level <= 20:
					polar_bear_bonus = (int((youdmg / 100) * 10))						
					polar_bear_bonus_text = "\n{} hits for {}.".format(pet_name, polar_bear_bonus)
				elif pet_level <= 30:
					polar_bear_bonus = (int((youdmg / 100) * 15))							
					polar_bear_bonus_text = "\n{} hits for {}.".format(pet_name, polar_bear_bonus)
				elif pet_level <= 40:
					polar_bear_bonus = (int((youdmg / 100) * 20))							
					polar_bear_bonus_text = "\n{} hits for {}.".format(pet_name, polar_bear_bonus)
				elif pet_level <= 50:
					polar_bear_bonus = (int((youdmg / 100) * 25))
					polar_bear_bonus_text = "\n{} hits for {}.".format(pet_name, polar_bear_bonus)
				elif pet_level >= 51:
					polar_bear_bonus = (int((youdmg / 100) * 30))
					polar_bear_bonus_text = "\n{} hits for {}.".format(pet_name, polar_bear_bonus)
			
			if pet_type == "Small Cerberus":
				if pet_level <= 10:
					small_cerberus_bonus = (int((youdef / 100) * 5))
				elif pet_level <= 20:
					small_cerberus_bonus = (int((youdef / 100) * 10))						
				elif pet_level <= 30:
					small_cerberus_bonus = (int((youdef / 100) * 15))							
				elif pet_level <= 40:
					small_cerberus_bonus = (int((youdef / 100) * 20))							
				elif pet_level <= 50:
					small_cerberus_bonus = (int((youdef / 100) * 25))
				elif pet_level >= 51:
					small_cerberus_bonus = (int((youdef / 100) * 30))

				youdef += small_cerberus_bonus
		# ENEMY DAMAGE BASED ON ENEMY GROUPS
		enemydmg = 0
		enemygold = 0
		xpgain = 0
		goldlost = 0
		guild = ctx.guild
		guildinfo = db.servers.find_one({"_id": guild.id})
		effectiveguildbonus = guildinfo["bonus"]

		if effectiveguildbonus >= 200:
			effectiveguildbonus = 200
		attack = ""
		if userinfo["selected_enemy"] == "Rachi" or userinfo["selected_enemy"] == "Debin" or userinfo["selected_enemy"] == "Oofer":
			attack = randchoice(["chomp and", "dash and", "bite and"])
			enemydmg += random.randint(5, 10)
			enemygold = random.randint(10, 30) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(5, 25)

		elif userinfo["selected_enemy"] == "Wyvern":
			attack = randchoice(["slash and", "scratch and", "bite and"])
			enemydmg += random.randint(10, 15)
			enemygold = random.randint(15, 35) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(10, 30)
			
		elif userinfo["selected_enemy"] == "Fire Golem":
			attack = randchoice(["smash and", "throw and throw's a rock.\nFire Golem", "hot head and spews lava.\nFire Golem"])
			enemydmg += random.randint(20, 30)
			enemygold = random.randint(25, 50) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(20, 40)

		elif userinfo["selected_enemy"] == "Draugr" or userinfo["selected_enemy"] == "Stalker":
			attack = randchoice(["swing and", "chase and", "stab and"])
			enemydmg += random.randint(15, 20)
			enemygold = random.randint(20, 40) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(15, 35)

		elif userinfo["selected_enemy"] == "Souleater":
			attack = randchoice(["devour and", "shatter and", "rip and"])
			enemydmg += random.randint(20, 25)
			enemygold = random.randint(25, 45) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(20, 40)
			
		elif userinfo["selected_enemy"] == "The Corrupted":
			attack = randchoice(["toxicity and breathes toxic flames\nThe Corrupted", "sense and hits a weak spot\nThe Corrupted", "flash appreaing right infront of you.\nThe Corrupted"])
			enemydmg += random.randint(30, 40)
			enemygold = random.randint(35, 55) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(30, 50)
			
		elif userinfo["selected_enemy"] == "Wolf" or userinfo["selected_enemy"] == "Goblin":
			attack = randchoice(["chase and", "impact and", "gauge and"])
			enemydmg += random.randint(25, 30)
			enemygold = random.randint(30, 50) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(25, 45)

		elif userinfo["selected_enemy"] == "Zombie":
			attack = randchoice(["devour and", "bite and", "sratch and"])
			enemydmg += random.randint(30, 35)
			enemygold = random.randint(35, 55) + effectiveguildbonus
			goldlost = (int((int(enemygold * 2))))
			xpgain = random.randint(30, 50)

		elif userinfo["selected_enemy"] == "Phantasm":
			attack = randchoice(["lighting and striking you\nPhantasm", "storm cloud and hides in the storm to attack you.\nPhantasm", "lightning guide and charges up and guides the energy towards you.\nPhantasm"])
			enemydmg += random.randint(40, 50)
			enemygold = random.randint(45, 65) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(40, 60)

		elif userinfo["selected_enemy"] == "Elder Dragon" or userinfo["selected_enemy"] == "Hades":
			attack = randchoice(["decay and", "rage and", "mutilate and"])
			enemydmg += random.randint(35, 40)
			enemygold = random.randint(40, 60) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(35, 55)

		elif userinfo["selected_enemy"] == "Ebony Guardian":
			attack = randchoice(["oblitirate and", "pounce and", "impair and"])
			enemydmg += random.randint(40, 45)
			enemygold = random.randint(45, 65) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(40, 60)

		elif userinfo["selected_enemy"] == "The Accursed":
			attack = randchoice(["soul burn and making u feel pain withing.\nThe Accursed", "Agony making your mind flooded with Agony.\nThe Accursed", "chain and furiously attacks you with its chains.\nThe Accursed"])
			enemydmg += random.randint(50, 60)
			enemygold = random.randint(55, 75) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(50, 70)

		elif userinfo["selected_enemy"] == "Ettin" or userinfo["selected_enemy"] == "Dormammu":
			attack = randchoice(["charge and", "whack and", "revenge and"])
			enemydmg += random.randint(45, 50)
			enemygold = random.randint(50, 70) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(45, 65)
			
		elif userinfo["selected_enemy"] == "Harpy":
			attack = randchoice(["backstab and", "rage and", "grasp and"])
			enemydmg += random.randint(50, 55)
			enemygold = random.randint(55, 75) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(50, 70)
			
		elif userinfo["selected_enemy"] == "The Nameless King":
			attack = randchoice(["DOOM and deals a deadly critical strike.\nThe Nameless king", "Nightmare vanishing from view and attacking you from behind scaring you.\nThe Nameless king", "Overpower making you see why they call him a king...\nThe Namelss King"])
			enemydmg += random.randint(60, 70)
			enemygold = random.randint(65, 85) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(60, 80)
			
		elif userinfo["selected_enemy"] == "Deathclaw" or userinfo["selected_enemy"] == "Saurian":
			attack = randchoice(["lacerate and", "cauterize and", "torment and"])
			enemydmg += random.randint(55, 65)
			enemygold = random.randint(60, 80) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(55, 75)
			
		elif userinfo["selected_enemy"] == "Largos":
			attack = randchoice(["curse and", "reckoning and", "exterminate and"])
			enemydmg += random.randint(60, 70)
			enemygold = random.randint(65, 85) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(60, 80)

		elif userinfo["selected_enemy"] == "The Venomous":
			attack = randchoice(["poise  biting you and temporarily poisoning you for 1 turn\n The Venomous", "spoil creates this spoiled food smell in the air making you feel unwell.\n The Venomous", "Headbutt simple but harmfull attack.\n The Venomous"])
			enemydmg += random.randint(70, 80)
			enemygold = random.randint(75, 95) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(70, 90)

		elif userinfo["selected_enemy"] == "Skeleton" or userinfo["selected_enemy"] == "Lizardmen":
			attack = randchoice(["dread and", "pierce and", "whip and"])
			enemydmg += random.randint(65, 75)
			enemygold = random.randint(70, 90) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(65, 85)

		elif userinfo["selected_enemy"] == "Giant":
			attack = randchoice(["fracture and", "embrace and", "avalanche and"])
			enemydmg += random.randint(70, 80)
			enemygold = random.randint(75, 95) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(70, 90)

		elif userinfo["selected_enemy"] == "Death Knight":
			attack = randchoice(["swift strike and strikes you with out noticing. \nDeath Knight", "sidestep and hits yu in the side by surprise.\nDeath Knight", "devastate swings his massive sword down on top of you devestating your armor.\nDeath Knight"])
			enemydmg += random.randint(80, 90)
			enemygold = random.randint(85, 105) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(80, 100)

		elif userinfo["selected_enemy"] == "Ice Wolves" or userinfo["selected_enemy"] == "Frost Goblin":
			attack = randchoice(["freeze and", "fake hibernate and", "bolt and"])
			enemydmg += random.randint(75, 85)
			enemygold = random.randint(80, 100) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(75, 95)

		elif userinfo["selected_enemy"] == "Frost Orc":
			attack = randchoice(["terror and", "maul and", "smite and"])
			enemydmg += random.randint(80, 90)
			enemygold = random.randint(85, 105) + effectiveguildbonus
			goldlost = (int(enemygold * 2))
			xpgain = random.randint(80, 100)

		elif userinfo["selected_enemy"] == "Frost Dragon":
			attack = randchoice(["snow storm hiding its appearance while attacking you from all sides. \nFrost dragon.", "Icy breath slowing you down and giving you slight frostbite.\nFrost Dragon", "Cold Fire breathe icy cold fire at you instead of burning you freezing you.\nFrost dragon"])
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

		elif userinfo["selected_enemy"] == "Gortac the Indestructible":
			# define enemydmg
			mindmg = userinfo["equip"]["stats_min"]
			maxdmg = userinfo["equip"]["stats_max"]
			bossdmg = random.randint(mindmg, maxdmg)
			enemydmg = (int((bossdmg / 100) * 120))
			# define loot
			enemygold = 0
			xpgain = 0
			goldlost = 0

		elif userinfo["selected_enemy"] == "None":
			return 

			# YOUR SKILL OPTIONS LIST
		skill_list = [i for i in userinfo["skills_learned"]]
		show_list = []
		options = []

		all_skills = [
			"Shoot", # archer, assassin, ranger, night assassin, skilled ranger
			"Swing", # knight, samurai, paladin, master samurai, grand paladin
			"Cast", # cast, necromancer, elementalist, developed necromancer, adequate elementalist
			"Stab", # thief, rogue, mesmer, high rogue, adept mesmer
			"Corrupt", # assassin, night assassin
			"Strike", # ranger, skilled ranger
			"Protrude", # samurai, master samurai
			"Fusillade", # paladin, grand paladin
			"Reap", # necromancer, developed necromancer
			"Overload", # elementalist, adequate elementalist
			"Parry", # rogue, high rogue
			"Distort", # mesmer, adept mesmer
			"Sneak", # night assassin
			"Slice", # master samurai
			"Blockade", # grand paladin
			"Snipe", # skilled ranger
			"Arise", # developed necromancer
			"Surge", # adequate elementalist
			"Rupture", # high rogue
			"Warp" # adept mesmer
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

		# DEFINE REOCCUREING DEFINITIONS
		eventinfo = db.users.find_one({ "_id": 387317544228487168 })
		
		# If enemy stunned no dmg
		if userinfo["EnemyStun"] > 0:
			enemydmg = 0
		# Users HP
		userhealth = userinfo["health"]
		# Users Defense
		enemydmg -= youdef
		# Enemy HP
		enemyhp = userinfo["enemyhp"]
		# Lootbag chance.
		lootbag = random.randint(1, 100)
		# If UserHealth is More then Maxhealth its Maxhealth
		if userhealth >= userinfo["MaxHealth"]:
			userhealth = userinfo["MaxHealth"]
		# If enemydmg is lower then 0 its 0
		if enemydmg < 0:
			enemydmg = 0

		if userinfo["role"] == "Developer":
			enemyname = userinfo["selected_enemy"]
			enemyhp = userinfo["enemyhp"]
			username = userinfo["name"]
			userhealth = userinfo["health"]
			totaldmg = 0
			bleeding = 0
			reap = 0
			overloadselfdmg = 0

			if userinfo["EnemyStun"] > 0:
				enemydmg = 0
			enemydmg -= youdef
			lootbag = random.randint(1, 100)
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]
			if enemydmg < 0:
				enemydmg = 0

			list = ""
			list += "{} has {} HP\n{} has {} HP\n\n".format(enemyname, enemyhp , username, userhealth)

			if answer2 == "Corrupt" or answer2 == "Strike" or answer2 == "Protrude" or answer2 == "Fusillade" or answer2 == "Reap" or answer2 == "Overload" or answer2 == "Parry" or answer2 == "Distort" or answer2 == "corrupt" or answer2 == "strike" or answer2 == "protrude" or answer2 == "fusillade" or answer2 == "reap" or answer2 == "overload" or answer2 == "parry" or answer2 == "distort":
				if userinfo["SkillCooldown1"] > 0:
					list = "This skill is on a **{} turn** cooldown.".format(userinfo["SkillCooldown1"])
					em = discord.Embed(description=list, color=monstercolor)
					await skillmsg.edit(embed=em)
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
					return

			if answer2 == "Sneak" or answer2 == "Slice" or answer2 == "Blockade" or answer2 == "Snipe" or answer2 == "Arise" or answer2 == "Surge" or answer2 == "Rupture" or answer2 == "Warp" or answer2 == "sneak" or answer2 == "slice" or answer2 == "blockade" or answer2 == "snipe" or answer2 == "arise" or answer2 == "surge" or answer2 == "rupture" or answer2 == "warp":
				if userinfo["SkillCooldown2"] > 0:
					list = "This skill is on a **{} turn** cooldown.".format(userinfo["SkillCooldown2"])
					em = discord.Embed(description=list, color=monstercolor)
					await skillmsg.edit(embed=em)
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
					return

			if answer2 == "cast" or answer2 == "Cast":
				orb = "a small orb"
				if userinfo["lvl"] >= 30:
					orb = "an orb"
				if userinfo["lvl"] >= 90:
					orb = "a large orb"
				if userinfo["Buff1"] == "Surge":
					list += "**you have been stunned for 1 turn**"
				else:
					list += "**{} casts {} and hits {} for {} damage.**".format(username, orb, enemyname, youdmg)
				if userinfo["Buff1"] == "Arise":
					hit = int((youdmg / 100) * 25)
					totaldmg = hit + hit + hit + hit + hit
					list += "\nThe army of skeletons attacks.\nDealing {} damage each\nDealing a total of {} damage.".format(hit, totaldmg)

			elif answer2 == "shoot" or answer2 == "Shoot":
				arrow = randchoice(["You shoot a normal arrow", "You fire a normal arrow"])
				if userinfo["lvl"] >= 30:
					arrow = randchoice(["You shoot an iron arrow", "You fire an iron arrow"])
				if userinfo["lvl"] >= 90:
					arrow = randchoice(["You shoot a steel arrow", "You fire a steel arrow"])
				if userinfo["Buff1"] == "Corrupt":
					youdmg = int((youdmg / 100) * 130)
					list += "**{} Has been corrupted for {} turns.\n{} dealing {} damage.**".format(enemyname, userinfo["Buff1Time"], arrow, youdmg)
					if userinfo["Buff1"] == "Corrupt" and userinfo["EnemyStun"] > 0:
						list += "**{} Has been stunned for {} turns**\n**{} Has been corrupted for {} turns.\n{} dealing {} damage.**".format(enemyname, userinfo["EnemyStun"], enemyname, userinfo["Buff1Time"], arrow, youdmg)
				else:
					list += "**{} dealing {} damage.**".format(arrow, youdmg)
			
			elif answer2 == "swing" or answer2 == "Swing":
				move = randchoice(["You swing your weapon and hit a light blow", "You strike a light blow"])
				if userinfo["lvl"] >= 30:
					move = randchoice(["You swing your weapon and hit a strong blow", "You strike a strong blow"])
				if userinfo["lvl"] >= 90:
					move = randchoice(["You swing your weapon and hit a heavy blow", "You strike a heavy blow"])
				if userinfo["Buff1"] == "Blockade":
					youdmg = int((youdmg / 100) * 85)
					youdef = youdef * 2
					list += "**{} has the blockade buff doubling defense.\n{} dealing {} damage.**".format(username, move, youdmg)
				elif userinfo["Buff1"] == "Slice":
					bleeding = int((enemyhp / 100) * 25)
					list += "**{} is still bleeding and losing health.\nTaking {} bleeding damage\n{} dealing {} damage.**".format(enemyname, bleeding, move, youdmg)
				else:
					list += "**{} dealing {} damage.**".format(move, youdmg)

			elif answer2 == "stab" or answer2 == "Stab":
				stab = randchoice(["You hit a quick stab", "You quickly hit their weakspot"])
				if userinfo["lvl"] >= 30:
					stab = randchoice(["You stab a weakspot", "You deal a precise stab"])
				if userinfo["lvl"] >= 90:
					stab = randchoice(["You critically stab a weakspot", "You deal a deadly stab"])
				if userinfo["EnemyStun"] > 0:
					list += "**{} is stunned and can't attack.\n{} dealing {} damage.**".format(enemydmg, stab, youdmg)
				elif userinfo["Buff1"] == "Rupture":
					bleeding = int((enemyhp / 100) * 25)
					list += "**{} is still bleeding and losing health.\nTaking {} bleeding damage\n{} dealing {} damage.**".format(enemyname, bleeding, stab, youdmg)
				elif userinfo["Buff1"] == "Warp":
					enemydmg = int((enemydmg / 100) * 60)
					list += "**{} has warp debuff.\n the enemy damage is lowered by 60%**\n{} dealing {} damage.**".format(enemyname, stab, youdmg)
				else:
					list += "**{} dealing {} damage.**".format(stab, youdmg)

			elif answer2 == "parry" or answer2 == "Parry" and userinfo["SkillCooldown1"] == 0:
				userinfo["EnemyStun"] = 2
				userinfo["SkillCooldown1"] = 4
				parry = randchoice(["You parry {}'s {} stunning them".format(enemyname, attack), "You parry their attack and stun them", "You parry the attack and stun {}".format(enemyname)])
				if userinfo["Buff1"] == "Rupture":
					bleeding = int((enemyhp / 100) * 25)
					list += "**{} is still bleeding and losing health.\nTaking {} bleeding damage\n{}.**".format(enemyname, bleeding, parry)
				else:
					list += "**{}.**".format(parry)

			elif answer2 == "distort" or answer2 == "Distort":
				userinfo["SkillCooldown1"] = 3
				if userinfo["Buff1"] == "Warp":
					enemydmg = int((enemydmg / 100) * 60)
					list += "**Distort makes enemy's deal 50% less damage.\n{} tries to fight but their attacks are still warped.\nThey deal less damage, Distort had no effect.\nYour attack deals {} damage.**".format(enemyname, youdmg)
				else:
					enemydmg = int((enemydmg / 100) * 50)
					list += "**Distort makes enemy's deal 50% less damage.\n{} tries to fight but their attacks are distorded.\nTheir attack scrapes you for {} damage.\nYour attack deals {} damage.**".format(enemyname, enemydmg, youdmg)

			elif answer2 == "reap" or answer2 == "Reap":
				reap = int((enemyhp / 100) * 30)
				list += randchoice(["**You reap 30% of {}'s health and add it to yourself.\n healing for {} hp.**".format(enemyname, reap),"**You reap {} hp from the enemy to heal yourself.**".format(reap)])
				if userinfo["Buff1"] == "Arise":
					hit = int((youdmg / 100) * 25)
					totaldmg = hit + hit + hit + hit + hit
					list += "\nThe army of skeletons attacks.\nDealing {} damage each\nDealing a total of {} damage.".format(hit, totaldmg)

			elif answer2 == "overload" or answer2 == "Overload":
				if userinfo["Buff1"] == "Surge":
					list += "**you have been stunned for 1 turn**"
				else:
					overloaddmg = int((youdmg / 100) * 40)
					overloadselfdmg = int((overloaddmg / 100) * 50)
					youdmg += overloaddmg
					userinfo["SkillCooldown1"] = 2
					list += randchoice(["**{} overloads {} for {} damage\nBut also deals 50% self damage**".format(username, enemyname, youdmg), "**{} overloads {} for {} damage\nBut also deals {} self damage**".format(username, enemyname, youdmg, overloadselfdmg), "you overload yourself increasing your damage to {} damage total but end up hurting yourself for {} hp.".format(youdmg, overloadselfdmg)])
			
			elif answer2 == "fusillade" or answer2 == "Fusillade":
				userinfo["SkillCooldown2"] = 5
				hit = int((youdmg / 100) * 50)
				youdmg = int((youdmg / 100) * 150)
				combo = randchoice(["You deal a series of 3 hits.", "You deal a series of 3 precise hits.", "You deal a series of 3 critical hits."])
				if userinfo["Buff1"] == "Blockade":
					youdmg = int((youdmg / 100) * 85)
					youdef = youdef * 2
					list += "**{} has the blockade buff doubling defense.\nbBut lowering the damage.\n{} Dealing {} damage.**".format(username, combo, youdmg)
				else:
					list += "**{} dealing {} per hit and doing a total of {} damage.**".format( combo, hit, youdmg)

			elif answer2 == "protrude" or answer2 == "Protrude":
				youdmg = int((youdmg / 100) * 140)
				combo = randchoice(["You hit the enemy on a critical spot.", "You stab the enemy on a critical spot.", "You pierce the enemy on a critical spot."])
				if userinfo["Buff1"] == "Slice":
					bleeding = int((enemyhp / 100) * 25)
					list += "**{} is still bleeding and losing health.\nTaking {} bleeding damage\n{}\n Dealing {} damage.**".format(enemyname, bleeding, combo, youdmg)
				else:
					list += "**{}\n dealing {} damage**".format(combo , youdmg)

			elif answer2 == "strike" or answer2 == "Strike":
				youdmg = int((youdmg / 100) * 50)
				userinfo["EnemyStun"] = 3.
				userinfo["SkillCooldown1"] = 6
				list += randchoice(["**You strike a blunt blow to the head immobilizing the enemy for 2 turns,\nbut dealing less damage.\nYou deal {} damage.**".format(youdmg), "**You strike a heavy hit to the chest stunning the enemy for 2 turns.\nYou deal {} damage.**".format(youdmg), "**You strike a fierce blow to the knee making the enemy incapable of moving for 2 turns.\nbut dealing less damage.\nYou deal {} damage.**".format(youdmg)])

			elif answer2 == "corrupt" or answer2 == "Corrupt":
				userinfo["Buff1"] = "Corrupt"
				userinfo["Buff1Time"] = 2
				userinfo["SkillCooldown1"] = 4	
				youdmg = int((youdmg / 100) * 130)
				list += randchoice(["**You corrupt the enemies body making them more vulnerable\nYou deal {} damage.**".format(youdmg), "**You corrupt the enemies mind making them defend less against your attacks\nYou deal {} damage.**".format(youdmg), "**You corrupt the enemies soul they become more fragile \nYou deal {} damage.**".format(youdmg)])

			elif answer2 == "Rupture" or answer2 == "rupture":
				userinfo["Buff1"] = "Rupture"
				userinfo["Buff1Time"] = 2
				bleeding = int((enemyhp / 100) * 25)
				userinfo["SkillCooldown2"] = 4
				list +=randchoice(["**You slice your weapon and rupture {}'s artery.\nCausing bleeding effect for 2 turns dealing {} damage.\nYou deal {} damage.**".format(enemyname, bleeding, youdmg), "**You hit the enemy with a blunt force rupturing an artery.\nCausing an internal bleeding for {} damage.\nYou deal {} damage.**".format(bleeding, youdmg), "**You stab the enemy in the neck rupturing their artery.\nCausing bleeding for 2 turns dealing {} damage\nYou deal {} damage.**".format(bleeding, youdmg)])

			elif answer2 == "Warp" or answer2 == "warp":
				userinfo["Buff1"] = "Warp"
				userinfo["Buff1Time"] = 2
				enemydmg = int((enemydmg / 100) * 60)
				userinfo["SkillCooldown2"] = 5
				list += "**Distort makes enemy's deal 50% less damage.\n{} tries to fight but their attacks are distorded.\nTheir attack scrapes you for {} damage.\nYour attack deals {} damage.**".format(enemyname, enemydmg, youdmg)
				list += randchoice(["**You warp the enemies movement.\nMaking their attack hit you in the shoulder.\nthey deal {} damage\nYou deal {} damage.**".format(enemydmg, youdmg), "**You warp the enemies attack.\ntheir attack hits you in the leg.\nthey deal {} damage\nYou deal {} damage.**".format(enemydmg, youdmg), "**You warp the enemies vision.\nMaking their attack hit you in foot.\nthey deal {} damage\nYou deal {} damage.**".format(enemydmg, youdmg)])

			elif answer2 == "Arise" or answer2 == "arise":
				hit = int((youdmg / 100) * 25)
				userinfo["Buff1"] = "Arise"
				userinfo["Buff1Time"] = 2
				userinfo["SkillCooldown2"] = 8
				totaldmg = hit + hit + hit + hit + hit
				list += randchoice(["**You focus all your power and raise a few skeletons to do your fighting.\nThey each deal {} damage for a total of {}  damage.**".format(hit, totaldmg), "**You raise a group of skeletons that will fight for you.\nthey all hit {} for {} total damage.**".format(enemyname, totaldmg), "**You raise a small army of skeletons to do your bidding.\n you command them to attack the enemy.\nthey each hit for {} and a total of {} damage.**".format(hit, totaldmg)])

			elif answer2 == "Surge" or answer2 == "surge":
				youdmg = youdmg * 3
				userinfo["SkillCooldown2"] = 4
				userinfo["Buff1"] = "Surge"
				userinfo["Buff1Time"] = 2
				list += randchoice(["**You gain a sudden mana boost tripling your damage!\nDealing a total of {} damage.\nThe amount of mana was too much to handle and you cant cast another spell for a duration.**".format(youdmg), "**You overload yourself with power and triple the magic output but stunning yourself in the process.\nYou deal a *stunning* {} damage!**".format(youdmg), "**You get a power surge, triple your damage but immobilizing yourself.\nYou deal {} damage.**".format(youdmg)])

			elif answer2 == "Slice" or answer2 == "slice":
				userinfo["Buff1"] = "Slice"
				userinfo["Buff1Time"] = 2
				youdmg += int((youdmg / 100) * 30)
				bleeding = int((enemyhp / 100) * 25)
				userinfo["SkillCooldown2"] = 4
				list += randchoice(["**You slice your weapon and cut open {}'s leg.\nCausing bleeding effect for 2 turns dealing {} damage.\nYou deal {} damage.**".format(enemyname, bleeding, youdmg), "**You slice their artery.\nCausing an internal bleeding for {} damage.\nYou deal {} damage.**".format(bleeding, youdmg), "**You slice the enemy in the neck rupturing their artery.\nCausing bleeding for 2 turns dealing {} damage\nYou deal {} damage.**".format(bleeding, youdmg)])

			elif answer2 == "Blockade" or answer2 == "blockade":
				userinfo["Buff1"] = "Blockade"
				userinfo["Buff1Time"] = 2
				youdmg = int((youdmg / 100) * 85)
				list += "**You clash your shields together doubling defense.\nBut lowering the damage.\n{} Dealing {} damage.**".format(username, youdmg)

			elif answer2 == "Sneak" or answer2 == "sneak":
				youdmg = int((youdmg / 100) * 150)
				userinfo["SkillCooldown2"] = 4
				list += randchoice(["**You come out the shadows and surprise {}.\nYou deal a critical strike to them!\nYou deal {} damage.**".format(enemyname, youdmg), "**You ambush {} and attack them with a critical hit!\nYou deal {} damage.**".format(enemyname, youdmg), "**You emerge from the darkness..\n Taking the enemy by surprise and dealing a critical hit.\nYou deal {} damage.**".format(youdmg)])

			elif answer2 == "Snipe" or answer2 == "snipe":
				youdmg = int((youdmg / 100) * 250)
				userinfo["SkillCooldown2"] = 5
				list += randchoice(["**You come out the shadows and shoot your shot at {}.\nYou land a headshot!\nYou deal {} damage.**".format(enemyname, youdmg), "**You hide and snipe {} BOOM! Headshot.\nYou deal {} damage.**".format(enemyname, youdmg), "**You confuse the enemy and hit them from behind\nLucky headshot!\nYou deal {} damage.**".format(youdmg)])

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

			if not userinfo["EnemyStun"] > 0:
				if not answer2 == "distort" or answer2 == "Distort":
					list += "\n**{} uses {} hits {} for {} damage.**".format(enemyname, attack, username, enemydmg)
			else:
				list += "\n**{} is stunned and can't fight.**".format(enemyname)
			list +="{}".format(polar_bear_bonus_text)

			userhealth = userhealth - enemydmg - overloadselfdmg 
			userhealth += reap
			enemyhp = enemyhp - youdmg - polar_bear_bonus - totaldmg - bleeding

			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]
			if enemyhp < 0:
				enemyhp = 0
			if userhealth < 0:
				userhealth = 0

			list += "\n\n{} has {} HP\n{} has {} HP\n\n".format(enemyname, enemyhp , username, userhealth)
			em = discord.Embed(description=list, color=monstercolor)
			if not userinfo["equip"]["image"] == "None":
				em.set_thumbnail(url=userinfo["equip"]["image"])

			em = discord.Embed(description=list, color=monstercolor)
			await skillmsg.edit(embed=em)

		# DEFINE WHAT SKILL WE SELECTED
		# Done
		else:
			if answer2 == "cast" or answer2 == "Cast":
				# Move user makes
				move = "Cast"
				# Acutal fight msg.
				if userinfo["Buff1"] == "Surge":
					if userinfo["selected_enemy"] == "Gortac the Indestructible":
						skill = random.randint(1, 100)
						if skill >= 60:
							# buff enemy strike
							enemydmg += youdef
							# Users HP after dmg taken.
							userhealth -= enemydmg
							# If User health is lower then 0 its 0
							if userhealth < 0:
								userhealth = 0
							em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} stabs you with the tip of the polearm piercing your armor dealing {} damage**\n**you have been stunned for 1 turn**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], enemydmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
							userhealth -= enemydmg
							# Enemys Hp after userdmg
							enemyhp = enemyhp - youdmg - polar_bear_bonus

							# If User health is lower then 0 its 0
							if userhealth < 0:
								userhealth = 0
							# If enemyhealth is lower then 0 its 0
							if enemyhp < 0:
								enemyhp = 0
							# If UserHealth is More then Maxhealth its Maxhealth
							if userhealth >= userinfo["MaxHealth"]:
								userhealth = userinfo["MaxHealth"]
							em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Swings his polearm towards you and deals {} damage**\n**you have been stunned for 1 turn**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], enemydmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**you have been stunned for 1 turn**\n**{} Hits {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)

					# Users HP after dmg taken.
					userhealth -= enemydmg
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0

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
					hit = int((youdmg / 100) * 25)

					# deals dmg to enemy
					totaldmg = hit + hit + hit + hit + hit
					enemyhp = enemyhp - totaldmg - youdmg - polar_bear_bonus	
					# Users HP after dmg taken.
					userhealth -= enemydmg

					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0

					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n** {} uses {} and hits {} for {} damage.\n The army of skeletons attacks.\nDealing {} damage each\nDealing a total of {} damage.{}\n{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], youdmg, hit, totaldmg, polar_bear_bonus_text, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					if userinfo["selected_enemy"] == "Gortac the Indestructible":
						skill = random.randint(1, 100)
						if skill >= 60:
							# buff enemy strike
							enemydmg += youdef
							# Users HP after dmg taken.
							userhealth -= enemydmg
							# Enemys Hp after userdmg
							enemyhp = enemyhp - youdmg - polar_bear_bonus

							# If User health is lower then 0 its 0
							if userhealth < 0:
								userhealth = 0
							# If enemyhealth is lower then 0 its 0
							if enemyhp < 0:
								enemyhp = 0
							# If UserHealth is More then Maxhealth its Maxhealth
							if userhealth >= userinfo["MaxHealth"]:
								userhealth = userinfo["MaxHealth"]
							em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} stabs you with the tip of the polearm piercing your armor dealing {} damage**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
							userhealth -= enemydmg
							# Enemys Hp after userdmg
							enemyhp = enemyhp - youdmg - polar_bear_bonus

							# If User health is lower then 0 its 0
							if userhealth < 0:
								userhealth = 0
							# If enemyhealth is lower then 0 its 0
							if enemyhp < 0:
								enemyhp = 0
							# If UserHealth is More then Maxhealth its Maxhealth
							if userhealth >= userinfo["MaxHealth"]:
								userhealth = userinfo["MaxHealth"]
							em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Swings his polearm towards you and deals {} damage**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					# Users HP after dmg taken.
					userhealth -= enemydmg
					# Enemys Hp after userdmg
					enemyhp = enemyhp - youdmg - polar_bear_bonus

					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0

					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text,  userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
					
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
				# Move user makes
				move = "Shoot"

				# stunned and buff
				if userinfo["Buff1"] == "Corrupt" and userinfo["Buff1Time"] > 0 and userinfo["EnemyStun"] > 0:
					youdmg = int((youdmg / 100) * 130)
					
					# Enemys Hp after Dmg
					enemyhp = userinfo["enemyhp"] - youdmg - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0

					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} Has been corrupted for {} turns.**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["selected_enemy"], userinfo["Buff1Time"], userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userhealth -= enemydmg
					# Enemys Hp after userdmg
					enemyhp = userinfo["enemyhp"] - youdmg - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					bufftime = userinfo["Buff1Time"]
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has corrupted {} for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					if userinfo["selected_enemy"] == "Gortac the Indestructible":
						skill = random.randint(1, 100)
						if skill >= 60:
							# buff enemy strike
							enemydmg += youdef
							# Users HP after dmg taken.
							userhealth -= enemydmg
							# Enemys Hp after userdmg
							enemyhp = enemyhp - youdmg - polar_bear_bonus

							# If User health is lower then 0 its 0
							if userhealth < 0:
								userhealth = 0
							# If enemyhealth is lower then 0 its 0
							if enemyhp < 0:
								enemyhp = 0
							# If UserHealth is More then Maxhealth its Maxhealth
							if userhealth >= userinfo["MaxHealth"]:
								userhealth = userinfo["MaxHealth"]
							em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} stabs you with the tip of the polearm piercing your armor dealing {} damage**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
							userhealth -= enemydmg
							# Enemys Hp after userdmg
							enemyhp = enemyhp - youdmg - polar_bear_bonus

							# If User health is lower then 0 its 0
							if userhealth < 0:
								userhealth = 0
							# If enemyhealth is lower then 0 its 0
							if enemyhp < 0:
								enemyhp = 0
							# If UserHealth is More then Maxhealth its Maxhealth
							if userhealth >= userinfo["MaxHealth"]:
								userhealth = userinfo["MaxHealth"]
							em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Swings his polearm towards you and deals {} damage**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					# Users HP after dmg taken.
					userhealth -= enemydmg
					# Enemys Hp after userdmg
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
				# Move user makes
				move = "Swing"
				# Acutal fight msg.
				if userinfo["Buff1"] == "Blockade":
					# debuff
					youdmg = int((youdmg / 100) * 85)
					# deals dmg to enemy
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# Users Defense
					youdef = youdef * 2
					enemydmg -= youdef	
					
					# If enemydmg is lower then 0 its 0
					if enemydmg < 0:
						enemydmg = 0
					# user dmg 
					userhealth -= enemydmg
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has the blockade buff doubling defense.\n {} uses {} hits {} for {} damage{}\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"],  userinfo["name"], move, userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					enemyhp = enemyhp - youdmg - bleeding - polar_bear_bonus
					# user dmg 
					userhealth -= enemydmg
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
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n {} Has bleeding effect for {} turns.**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], bufftime, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					if userinfo["selected_enemy"] == "Gortac the Indestructible":
						skill = random.randint(1, 100)
						if skill >= 60:
							# buff enemy strike
							enemydmg += youdef
							# Users HP after dmg taken.
							userhealth -= enemydmg
							# Enemys Hp after userdmg
							enemyhp = enemyhp - youdmg - polar_bear_bonus

							# If User health is lower then 0 its 0
							if userhealth < 0:
								userhealth = 0
							# If enemyhealth is lower then 0 its 0
							if enemyhp < 0:
								enemyhp = 0
							# If UserHealth is More then Maxhealth its Maxhealth
							if userhealth >= userinfo["MaxHealth"]:
								userhealth = userinfo["MaxHealth"]
							em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} stabs you with the tip of the polearm piercing your armor dealing {} damage**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
							userhealth -= enemydmg
							# Enemys Hp after userdmg
							enemyhp = enemyhp - youdmg - polar_bear_bonus

							# If User health is lower then 0 its 0
							if userhealth < 0:
								userhealth = 0
							# If enemyhealth is lower then 0 its 0
							if enemyhp < 0:
								enemyhp = 0
							# If UserHealth is More then Maxhealth its Maxhealth
							if userhealth >= userinfo["MaxHealth"]:
								userhealth = userinfo["MaxHealth"]
							em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Swings his polearm towards you and deals {} damage**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
						userhealth -= enemydmg
						# Enemys Hp after userdmg
						enemyhp = enemyhp - youdmg - polar_bear_bonus

						# If User health is lower then 0 its 0
						if userhealth < 0:
							userhealth = 0
						# If enemyhealth is lower then 0 its 0
						if enemyhp < 0:
							enemyhp = 0
						# If UserHealth is More then Maxhealth its Maxhealth
						if userhealth >= userinfo["MaxHealth"]:
							userhealth = userinfo["MaxHealth"]
						em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
				# Move user makes
				move = "Stab"

				# Acutal fight msg.
				if userinfo["EnemyStun"] > 0:
					# Users HP after dmg taken.
					userhealth -= enemydmg
					# Enemys Hp after userdmg
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["EnemyStun"], userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					# Bleeding dmg
					bleeding = int((enemyhp / 100) * 25)
					# deals dmg to enemy
					enemyhp = enemyhp - youdmg - bleeding - polar_bear_bonus
					# user dmg 
					userhealth -= enemydmg
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0

					bufftime = userinfo["Buff1Time"]
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n {} Has bleeding effect for {} turns.**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], bufftime, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					enemydmg = int((enemyhp / 100) * 40)
					# user dmg 
					userhealth -= enemydmg
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, But {} has warp debuff.\n the enemy damage is lowered by 60%**\n**{} hits {} for {} damage{}\n{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userhealth -= enemydmg
					# Enemys Hp after userdmg
					enemyhp = enemyhp - youdmg
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
				# Move user makes
				move = "Parry"
				# Acutal fight msg.
				if userinfo["Buff1"] == "Rupture" and userinfo["SkillCooldown1"] == 0:
					userinfo["EnemyStun"] = 2
					userinfo["SkillCooldown1"] = 4
					stun = 1
					# Bleeding dmg
					bleeding = int((enemyhp / 100) * 25)
					# deals dmg to enemy
					enemyhp = enemyhp - bleeding - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					bufftime = userinfo["Buff1Time"]
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turn\n {} Has bleeding effect for {} turn(s).\nBleeding does {} damage{}**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], stun, userinfo["selected_enemy"], bufftime, bleeding, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					enemyhp = enemyhp - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turn**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], stun,polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					
					userinfo["EnemyStun"] = 2
					userinfo["SkillCooldown1"] = 4
					stun = 1
					# Bleeding dmg
					bleeding = int((enemyhp / 100) * 25)
					# deals dmg to enemy
					enemyhp = enemyhp - bleeding - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					bufftime = userinfo["Buff1Time"]
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turn\n {} Has bleeding effect for {} turn(s).{}**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], stun, polar_bear_bonus_text, userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown1"] += 1
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
				# Move user makes
				move = "Distort"
				if userinfo["Buff1"] == "Warp" and userinfo["Buff1Time"] > 0:

					# Enemys Hp after userdmg
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# Users HP after dmg taken.
					userhealth -= enemydmg
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# set skill cooldown
					userinfo["SkillCooldown1"] = 3
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, But {} has warp debuff.\n the enemy damage is 0.**\n**{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"],  userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userhealth -= enemydmg
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# Enemys Hp after userdmg
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# set skill cooldown
					userinfo["SkillCooldown1"] = 3
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, halving the damage**\n**{} hits {} for {} damage**\n**{} hits {} for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], userinfo["name"], enemydmg,  userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown1"] += 1
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
				if userinfo["Buff1"] == "Arise" and userinfo["Buff1Time"] > 0 and userinfo["SkillCooldown1"] == 0:
					# takes 30% of enemyhp 
					reap = int((enemyhp / 100) * 30)

					hit = int((youdmg / 100) * 25)

					# deals dmg to enemy
					totaldmg = hit + hit + hit + hit + hit
					enemyhp = enemyhp - reap - totaldmg - polar_bear_bonus
					# Adds 25% enemy hp to user
					userhealth += reap
					if userhealth >= userinfo["MaxHealth"]:
						userhealth = userinfo["MaxHealth"]
					userhealth -= enemydmg
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# Set skill cooldown.
					userinfo["SkillCooldown1"] = 3
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and 30% of {} Health.\n{} Hp healed! \nThe army of skeletons attacks.\nDealing {} damage each\nDealing a total of {} damage.\n**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], reap, hit, totaldmg, polar_bear_bonus, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					enemyhp = enemyhp - reap - polar_bear_bonus
					if enemyhp < 0:
						enemyhp = 0
					# Adds 25% enemy hp to user
					userhealth += reap
					if userhealth >= userinfo["MaxHealth"]:
						userhealth = userinfo["MaxHealth"]
					# Set skill cooldown.
					userinfo["SkillCooldown1"] = 3
					em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Reaps 30% of {} Health.\n{} Hp healed!**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], userinfo["selected_enemy"], reap, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown1"] += 1
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
				if userinfo["Buff1"] == "Surge":

					enemyhp = userinfo["enemyhp"]
					# user dmg 
					userhealth -= enemydmg
					enemyhp = enemyhp - polar_bear_bonus
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**you have been stunned for 1 turn**\n**{} Hits {} and hits for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["selected_enemy"], userinfo["name"], enemydmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userhealth = userhealth - enemydmg - overloadselfdmg 
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# Set skill cooldown.
					userinfo["SkillCooldown1"] = 3
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} overloads {} for {} damage\nBut also deals {} self damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, overloadselfdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown1"] += 1
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
				if userinfo["Buff1"] == "Blockade":
					# debuff
					youdmg = int((youdmg / 100) * 85)
					hit = int((youdmg / 100) * 50)
					# deals dmg to enemy
					totaldmg = hit + hit + hit
					enemyhp = enemyhp - totaldmg - polar_bear_bonus
					# Users Defense (first already did this now agiann for the X2 bonus)
					enemydmg -= youdef
					# If enemydmg is lower then 0 its 0
					if enemydmg < 0:
						enemydmg = 0
					# user dmg 
					userhealth -= enemydmg
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# Set skill cooldown.
					userinfo["SkillCooldown2"] = 5
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Has the blockade buff doubling defense.\n{} hits {} for {} damage**\n**{} uses {} and does a series of hits.**\n**Dealing {} damage each**\n**Dealing a total of {} damage.**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, hit, totaldmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					enemyhp = enemyhp - totaldmg - polar_bear_bonus
					# user dmg 
					userhealth -= enemydmg
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# Set skill cooldown.
					userinfo["SkillCooldown1"] = 4
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and does a series of hits.**\n**Dealing {} damage each**\n**Dealing a total of {} damage.**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, hit, totaldmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown1"] += 1
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
				if userinfo["Buff1"] == "Slice":
					enemyhp = userinfo["enemyhp"]
					# Bleeding dmg
					bleeding = int((enemyhp / 100) * 25)
					youdmg = int((youdmg / 100) * 140)
					# deals dmg to enemy
					enemyhp = enemyhp - youdmg - bleeding - polar_bear_bonus
					# user dmg 
					userhealth -= enemydmg
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0

					bufftime = userinfo["Buff1Time"]
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n {} Has bleeding effect for {} turns.**\n**{} uses {} and has a Critical hit! for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["selected_enemy"], bufftime, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# user dmg 
					userhealth -= enemydmg
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# Set skill cooldown.
					userinfo["SkillCooldown1"] = 3
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and has a Critical hit!\n for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown1"] += 1
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
				# Move user makes
				move = "Strike"
				# Acutal fight msg.
				if userinfo["SkillCooldown1"] == 0:
					youdmg = int((youdmg / 100) * 50)
					userinfo["EnemyStun"] = 3
					stun = 2
					# deals dmg to enemy
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# Set skill cooldown.
					userinfo["SkillCooldown1"] = 6
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turns\n{} Hits {} for {} Damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], stun, userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown1"] += 1
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
				# Move user makes
				move = "Corrupt"
				# Acutal fight msg.
				if userinfo["SkillCooldown1"] == 0:
					# add buff and timer
					userinfo["Buff1"] = "Corrupt"
					userinfo["Buff1Time"] = 2
					# Corrupt dmg	
					youdmg = int((youdmg / 100) * 130)
					bufftime = 2
					# deals dmg to enemy
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# user dmg 
					userhealth -= enemydmg
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# Set skill cooldown.
					userinfo["SkillCooldown1"] = 4
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and corrupts {} for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown1"] += 1
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
			# done
			elif answer2 == "Rupture" or answer2 == "rupture":
				# Rupture the enemy's artery 2 turns dealing 25% current hp bleeding dmg.  4 turn cooldown.
				# Move user makes
				move = "Rupture"
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
					enemyhp = enemyhp - youdmg - bleeding - polar_bear_bonus
					# user dmg 
					userhealth -= enemydmg
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# Set skill cooldown.
					userinfo["SkillCooldown2"] = 4
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and Ruptures {} artery\n causing bleeding effect for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown2"] += 1 
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
			# done
			elif answer2 == "Warp" or answer2 == "warp":
				# Warp the enemy's attacks for 2 turns dealing 60% Less damage.  5 turn cooldown.
				# Move user makes
				move = "Warp"
				# Acutal fight msg.
				if userinfo["SkillCooldown2"] == 0:
					# add buff and timer
					userinfo["Buff1"] = "Warp"
					userinfo["Buff1Time"] = 2
					enemydmg = int((enemydmg / 100) * 60)
					# Users HP after dmg taken.
					userhealth -= enemydmg
					# Enemys Hp after userdmg
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# Set skill cooldown.
					userinfo["SkillCooldown2"] = 5
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, Warping {} Attack dealing 60% less damage**\n**{} hits {} for {} damage**\n**{} hits {} for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], userinfo["selected_enemy"], userinfo["name"], enemydmg,  userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown2"] += 1 
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
			# done
			elif answer2 == "Arise" or answer2 == "arise":
				# Arise A small army of 5 Skeletons dealing 30% your dmg for 2 turns, Has a 5 turn cooldown 
				# Move user makes
				move = "Arise"
				
				if userinfo["SkillCooldown2"] == 0:
					hit = int((youdmg / 100) * 25)
					# deals dmg to enemy
					totaldmg = hit + hit + hit + hit + hit
					enemyhp = enemyhp - totaldmg - youdmg - polar_bear_bonus
					# user dmg 
					userhealth -= enemydmg
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
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and Raises a small army of skeletons!.**\n**Dealing {} damage each**\n**Dealing a total of {} damage.\n{} hits {} for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, hit, totaldmg, userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown2"] += 1 
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
			# done
			elif answer2 == "Surge" or answer2 == "surge":
				# Surge Causes the user to get a massice power surge dealing 3 times normal damage but stunning themself after the attack for 1 turn.
				# Move user makes
				move = "Surge"		
				if userinfo["SkillCooldown2"] == 0:
					youdmg = youdmg * 3
					userhealth -= enemydmg 
					enemyhp = enemyhp - youdmg - polar_bear_bonus
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
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} gains a power surge and triples their damage.\n total damage {}Hp\nBut stun yourself for 1 turn.**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown2"] += 1 
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
			# done
			elif answer2 == "Slice" or answer2 == "slice":
				# SLice causes 2 round bleeding effect(25% current health), 30% increased damage 4 turn cooldown.
				# Move user makes
				move = "Slice"
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
					enemyhp = enemyhp - youdmg - bleeding - polar_bear_bonus
					# user dmg 
					userhealth -= enemydmg
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# Set skill cooldown.
					userinfo["SkillCooldown2"] = 4
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and Slices {}\n causing bleeding effect for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], bufftime, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown2"] += 1 
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
			# done
			elif answer2 == "Blockade" or answer2 == "blockade":
				# Blockade Dubbles your armor for 2 turns! dealing 15% less damage. 5 turn cooldown.
				# Move user makes
				move = "Blockade"
				# Acutal fight msg.
				if userinfo["SkillCooldown2"] == 0:
					# add buff and timer
					userinfo["Buff1"] = "Blockade"
					userinfo["Buff1Time"] = 2
					# debuff
					youdmg = int((youdmg / 100) * 85)
					# deals dmg to enemy
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# Users Defense
					enemydmg -= youdef	
					
					# If enemydmg is lower then 0 its 0
					if enemydmg < 0:
						enemydmg = 0
					# user dmg 
					userhealth -= enemydmg
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# Set skill cooldown.
					userinfo["SkillCooldown2"] = 5
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and Dubbles their defense for 2 turns.\n{} hits {} for {} damage\n{} Hits {} for {} Damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown2"] += 1 
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
			# done
			elif answer2 == "Sneak" or answer2 == "sneak":
				# Sneak around your enemy and delivering a critical hit dealing 150% and not taking any dmg! 4 turn cooldown.
				# Move user makes
				move = "Sneak"
				if userinfo["SkillCooldown2"] == 0:
					youdmg = int((youdmg / 100) * 150)
					# deals dmg to enemy
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# user dmg 
					userhealth -= enemydmg
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# Set skill cooldown.
					userinfo["SkillCooldown2"] = 4
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and comes out the shadows.\nYou deal a critical hit! for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
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
					userinfo["SkillCooldown2"] += 1 
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
			# snipe
			elif answer2 == "Snipe" or answer2 == "snipe":
				# Snipe your enemy from afer taking no damage but headshotting the enemy dealing 250% of your base dmg. 6 turn cooldown.
				# Move user makes
				move = "Snipe"
				if userinfo["SkillCooldown2"] == 0:
					youdmg = int((youdmg / 100) * 250)
					# deals dmg to enemy
					enemyhp = enemyhp - youdmg - polar_bear_bonus
					# If User health is lower then 0 its 0
					if userhealth < 0:
						userhealth = 0
					# If enemyhealth is lower then 0 its 0
					if enemyhp < 0:
						enemyhp = 0
					# Set skill cooldown.
					userinfo["SkillCooldown2"] = 5
					em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and headshots {}.\nYou deal a critical hit! for {} damage**{}\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"],  userinfo["name"], move, userinfo["selected_enemy"], youdmg, polar_bear_bonus_text, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
					if not userinfo["equip"]["image"] == "None":
						em4.set_thumbnail(url=userinfo["equip"]["image"])
					await skillmsg.edit(embed=em4)
				else:
					userinfo["SkillCooldown2"] += 1 
					em4 = discord.Embed(description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["SkillCooldown2"]), color=discord.Colour(0xffffff))
					if not userinfo["equip"]["image"] == "None":
						em4.set_thumbnail(url=userinfo["equip"]["image"])
					await skillmsg.edit(embed=em4)

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
		userinfo["EnemyStun"] -= 1
		if userinfo["EnemyStun"] <= 0:
			userinfo["EnemyStun"] = 0
		userinfo["SkillCooldown1"] -= 1
		if userinfo["SkillCooldown1"] <= 0:
			userinfo["SkillCooldown1"] = 0
		userinfo["SkillCooldown2"] -= 1
		if userinfo["SkillCooldown2"] <= 0:
			userinfo["SkillCooldown2"] = 0
		if not userinfo["Buff1"] == "None":
			userinfo["Buff1Time"] -= 1 
		if userinfo["Buff1Time"] <= 0:
			userinfo["Buff1"] = "None"
			userinfo["Buff1Time"] = 0
		
		userinfo["health"] = userhealth
		userinfo["enemyhp"] = enemyhp
		
		if enemyhp <= 0 and userhealth <= 0:
			em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["bothdied"]["translation"].format(userinfo["name"], goldlost), color=discord.Colour(0x000000))
			await ctx.send(embed=em)
			userinfo["gold"] -= goldlost
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
			userinfo["enemieskilled"] += 1
			userinfo["deaths"] += 1

		elif userhealth <= 0:
			em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["playerdied"]["translation"].format(userinfo["selected_enemy"], userinfo["name"], userinfo["name"], goldlost), color=discord.Colour(0xff0000))
			await ctx.send(embed=em)
			userinfo["gold"] -= goldlost
			if userinfo["gold"] < 0:
				userinfo["gold"] = 0
			if userinfo["health"] < 0:
				userinfo["health"] = 0
			if userinfo["Buff1"] == "Corrupt":
				userinfo["Buff1"] = "None"
				userinfo["Buff1Time"] = 0
			userinfo["selected_enemy"] = "None"
			userinfo["enemydifficulty"] = "None"
			userinfo["deaths"] += 1
		
		elif enemyhp <= 0:
			lootbag_chance = 3
			try:
				pterodactyl_bonus = 0
				pterodactyl_bonus_text = ""
				fox_bonus_text = ""
				goose_bonus_text = ""
				goose_bonus = 0
				for i in userinfo["pet_list"]:
					petinfo = i
					pet_level = petinfo["level"]
					pet_type = petinfo["type"]
					if pet_type == "Goose":
						if pet_level <= 10:
							goose_bonus = (int((enemygold / 100) * 5))
							goose_bonus_text = "\n<:Gold:639484869809930251> +{} pet bonus.".format(goose_bonus)
						elif pet_level <= 20:
							goose_bonus = (int((enemygold / 100) * 10))						
							goose_bonus_text = "\n<:Gold:639484869809930251> +{} pet bonus.".format(goose_bonus)
						elif pet_level <= 30:
							goose_bonus = (int((enemygold / 100) * 15))							
							goose_bonus_text = "\n<:Gold:639484869809930251> +{} pet bonus.".format(goose_bonus)
						elif pet_level <= 40:
							goose_bonus = (int((enemygold / 100) * 20))							
							goose_bonus_text = "\n<:Gold:639484869809930251> +{} pet bonus.".format(goose_bonus)
						elif pet_level <= 50:
							goose_bonus = (int((enemygold / 100) * 25))
							goose_bonus_text = "\n<:Gold:639484869809930251> +{} pet bonus.".format(goose_bonus)
						elif pet_level >= 51:
							goose_bonus = (int((enemygold / 100) * 30))
							goose_bonus_text = "\n<:Gold:639484869809930251> +{} pet bonus.".format(goose_bonus)

					if pet_type == "Pterodactyl":
						if pet_level <= 10:
							pterodactyl_bonus = (int((xpgain / 100) * 2.5))
							pterodactyl_bonus_text = "\n:sparkles: +{} pet bonus.".format(pterodactyl_bonus)
						elif pet_level <= 20:
							pterodactyl_bonus = (int((xpgain / 100) * 5))						
							pterodactyl_bonus_text = "\n:sparkles: +{} pet bonus.".format(pterodactyl_bonus)
						elif pet_level <= 30:
							pterodactyl_bonus = (int((xpgain / 100) * 7.5))							
							pterodactyl_bonus_text = "\n:sparkles: +{} pet bonus.".format(pterodactyl_bonus)
						elif pet_level <= 40:
							pterodactyl_bonus = (int((xpgain / 100) * 10))							
							pterodactyl_bonus_text = "\n:sparkles: +{} pet bonus.".format(pterodactyl_bonus)
						elif pet_level <= 50:
							pterodactyl_bonus = (int((xpgain / 100) * 12.5))
							pterodactyl_bonus_text = "\n:sparkles: +{} pet bonus.".format(pterodactyl_bonus)
						elif pet_level >= 51:
							pterodactyl_bonus = (int((xpgain / 100) * 15))
							pterodactyl_bonus_text = "\n:sparkles: +{} pet bonus.".format(pterodactyl_bonus)

					if pet_type == "Fox":
						if pet_level <= 10:
							lootbag_chance = 8
							fox_bonus_text = "\n:sparkles: +5% pet bonus chance."
						elif pet_level <= 20:
							lootbag_chance = 13
							fox_bonus_text = "\n:sparkles: +10% pet bonus chance."
						elif pet_level <= 30:
							lootbag_chance = 18
							fox_bonus_text = "\n:sparkles: +15% pet bonus chance."
						elif pet_level <= 40:	
							lootbag_chance = 23
							fox_bonus_text = "\n:sparkles: +20% pet bonus chance."
						elif pet_level <= 50:
							lootbag_chance = 28
							fox_bonus_text = "\n:sparkles: +25% pet bonus chance."
						elif pet_level >= 51:
							lootbag_chance = 33
							fox_bonus_text = "\n:sparkles: +30% pet bonus chance."
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

					friend_info["gold"] += shared_gold
					friend_info["exp"] += shared_xpgain
				
					flist = ("**{}**: <:Gold:639484869809930251>{}  Shared gold, :sparkles: {} Shared Exp\n".format(friend_info["name"], int(shared_gold), int(shared_xpgain)))
					party_reward_list += flist
					
					if friend_info["exp"] >= 100 + ((friend_info["lvl"] + 1) * 3.5):
						friend_info["exp"] = friend_info["exp"] - (100 + ((friend_info["lvl"] + 1) * 3.5))
						friend_info["lvl"] = friend_info["lvl"] + 1
						friend_info["health"] = friend_info["MaxHealth"]
						em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(friend_info["name"]), color=discord.Colour(0xffd700))
						await ctx.send(embed=em)	
				
					if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
						userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
						userinfo["lvl"] = userinfo["lvl"] + 1
						userinfo["health"] = userinfo["MaxHealth"]
						em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
						await ctx.send(embed=em)
						
					db.users.replace_one({"_id": friend_id}, friend_info, upsert=True)

				try:
					em2 = discord.Embed(description=":dagger:{} Killed the {}\n<:PvP:573580993055686657>The Party gets \n {}".format(userinfo["name"], userinfo["selected_enemy"], party_reward_list), color=discord.Colour(0x00ff00))
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
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user, userinfo)
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
				userinfo["Rachikilled"] += 1
				if userinfo["questname"] == "Rachi I":
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user, userinfo)
					pass
					
			elif userinfo["selected_enemy"] == "Draugr":
				userinfo["Draugrkilled"] += 1
				if userinfo["questname"] == "Draugr I":
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user, userinfo)
					pass

			elif userinfo["selected_enemy"] == "Debin":
				userinfo["Debinkilled"] += 1
				if userinfo["questname"] == "Debin I":
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user, userinfo)
					pass

			elif userinfo["selected_enemy"] == "Stalker":
				userinfo["Stalkerkilled"] += 1
				if userinfo["questname"] == "Stalker I":
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user, userinfo)
					pass


			elif userinfo["selected_enemy"] == "Fire Golem":
				userinfo["FireGolemkilled"] += 1
				pet_spawn = random.randint(1, 100)
				if userinfo["role"] == "Developer":
					pet_spawn = 95
				if pet_spawn >= 90:
					if userinfo["pet_stage"] == "Golden Goose":
						em = discord.Embed(title="A pet!", description="A tameable pet has spawned! It's a goose.\nTo tame it type `{}pet tame`".format(ctx.prefix), color=discord.Colour(0xbb4424))
						em.set_image(url="")
						await ctx.send(embed=em)
						userinfo["pet_find"] = "Golden Goose"		
				if userinfo["questname"] == "Fire Golem I":
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 5:
						await _quest_check(self, ctx, user, userinfo)
					pass

			elif userinfo["selected_enemy"] == "Wyvern":
				userinfo["Wyvernkilled"] += 1
				if userinfo["questname"] == "Wyvern I":
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user, userinfo)
					pass
				elif userinfo["questname"] == "On the hunt!" and userinfo["enemydifficulty"] == "Rare":
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 1:
						await _quest_check(self, ctx, user, userinfo)
					pass

			elif userinfo["selected_enemy"] == "Oofer":
				userinfo["Ooferkilled"]  += 1
				if userinfo["questname"] == "Oofer I":
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user, userinfo)
					pass

			elif userinfo["selected_enemy"] == "Souleater":
				userinfo["Souleaterkilled"] += 1
				if userinfo["questname"] == "Souleater I":
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 10:
						await _quest_check(self, ctx, user, userinfo)
					pass

			elif userinfo["selected_enemy"] == "Wolf":
				userinfo["Wolfkilled"] += 1
			elif userinfo["selected_enemy"] == "Goblin":
				userinfo["Goblinkilled"] += 1
			elif userinfo["selected_enemy"] == "Zombie":
				userinfo["Zombiekilled"] += 1
			elif userinfo["selected_enemy"] == "Phantasm":
				userinfo["Phantasmkilled"] += 1
				pet_spawn = random.randint(1, 100)
				if userinfo["role"] == "Developer":
					pet_spawn = 95
				if pet_spawn >= 90:
					if userinfo["pet_stage"] == "Polar Bear":
						em = discord.Embed(title="A pet!", description="A tameable pet has spawned! It's a polar bear.\nTo tame it type `{}pet tame`".format(ctx.prefix), color=discord.Colour(0xD4D8D7))
						em.set_image(url="")
						await ctx.send(embed=em)
						userinfo["pet_find"] = "Polar Bear"
						

			elif userinfo["selected_enemy"] == "The Corrupted":
				userinfo["TheCorruptedkilled"] += 1
				if userinfo["questname"] == "The Corrupted I":
					userinfo["questprogress"] += 1
					if userinfo["questprogress"] >= 5:
						await _quest_check(self, ctx, user, userinfo)
					pass
				pet_spawn = random.randint(1, 100)
				if userinfo["role"] == "Developer":
					pet_spawn = 95
				if pet_spawn >= 90:
					if userinfo["pet_stage"] == "Fox":
						em = discord.Embed(title="A pet!", description="A tameable pet has spawned! It's a fox.\nTo tame it type `{}pet tame`".format(ctx.prefix), color=discord.Colour(0x7a2c05))
						em.set_image(url="")
						await ctx.send(embed=em)
						userinfo["pet_find"] = "Fox"

			elif userinfo["selected_enemy"] == "The Accursed":
				userinfo["TheAccursedkilled"] += 1
				pet_spawn = random.randint(1, 100)
				if userinfo["role"] == "Developer":
					pet_spawn = 95
				if pet_spawn >= 90:
					if userinfo["pet_stage"] == "Small Cerberus":
						em = discord.Embed(title="A pet!", description="A tameable pet has spawned! It's a small cerberus.\nTo tame it type `{}pet tame`".format(ctx.prefix), color=discord.Colour(0xcb2004))
						em.set_image(url="")
						await ctx.send(embed=em)
						userinfo["pet_find"] = "Small Cerberus"
						

			elif userinfo["selected_enemy"] == "Elder Dragon":
				userinfo["ElderDragonkilled"] += 1
			elif userinfo["selected_enemy"] == "Hades":
				userinfo["Hadeskilled"] += 1
			elif userinfo["selected_enemy"] == "Ebony Guardian":
				userinfo["EbonyGuardiankilled"] += 1
			elif userinfo["selected_enemy"] == "Harpy":
				userinfo["Harpykilled"] += 1
			elif userinfo["selected_enemy"] == "Dormammu":
				userinfo["Dormammukilled"] += 1
			elif userinfo["selected_enemy"] == "Ettin":
				userinfo["Ettinkilled"] += 1
			elif userinfo["selected_enemy"] == "The Nameless King":
				userinfo["TheNamelessKingkilled"] += 1
			elif userinfo["selected_enemy"] == "Largos":
				userinfo["Largoskilled"] += 1
			elif userinfo["selected_enemy"] == "Deathclaw":
				userinfo["Deathclawkilled"] += 1
			elif userinfo["selected_enemy"] == "Saurian":
				userinfo["Sauriankilled"] += 1
			elif userinfo["selected_enemy"] == "The venemous":
				userinfo["TheVenomouskilled"] += 1
			elif userinfo["selected_enemy"] == "Skeleton":
				userinfo["Skeletonkilled"] += 1
			elif userinfo["selected_enemy"] == "Lizardmen":
				userinfo["Lizardmenkilled"] += 1
			elif userinfo["selected_enemy"] == "Giant":
				userinfo["Giantkilled"] += 1
			elif userinfo["selected_enemy"] == "Death Knight":
				userinfo["DeathKnightkilled"] += 1
			elif userinfo["selected_enemy"] == "Ice Wolves":
				userinfo["IceWolveskilled"] += 1
			elif userinfo["selected_enemy"] == "Frost Orc":
				userinfo["FrostOrckilled"] += 1
			elif userinfo["selected_enemy"] == "Frost Goblin":
				userinfo["FrostGoblinkilled"] += 1
			elif userinfo["selected_enemy"] == "Frost Dragon":
				userinfo["FrostDragonkilled"] += 1
			
			em = discord.Embed(description=":dagger: {} killed the {}\n<:GoldBars:573781770709893130> {} gained {} gold{}\n:sparkles: {} gained {} experience{}".format(userinfo["name"], userinfo["selected_enemy"], userinfo["name"], int(enemygold), goose_bonus_text, userinfo["name"], xpgain, pterodactyl_bonus_text), color=discord.Colour(0x00ff00))
			await ctx.send(embed=em)	

			userinfo["selected_enemy"] = "None"
			userinfo["enemydifficulty"] = "None"
			userinfo["gold"] += int(enemygold + goose_bonus)
			userinfo["exp"]+= int(xpgain + pterodactyl_bonus)	
			if lootbag <= lootbag_chance:
				chance2 = random.randint(1, 100)
				if chance2 >= 50:
					em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["crate"]["translation"].format(userinfo["name"], fox_bonus_text), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
					userinfo["lootbag"] += 1
				else:			
					em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["key"]["translation"].format(userinfo["name"], fox_bonus_text), color=discord.Colour(0xffffff))
					await ctx.send(embed=em)
					userinfo["keys"] += 1

			
			userinfo["enemieskilled"] += 1
		db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
		try:
			await _level_up_check_user(self, ctx, user)
		except:
			return
			


def setup(bot):
	n = fight(bot)
	bot.add_cog(n)