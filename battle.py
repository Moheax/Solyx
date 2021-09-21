import asyncio
import random
from time import time

import discord
from discord.ext import commands

from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import battledata
from cogs.levelup import _level_up_check_user

async def _create_battle(user):
	exists = db.battles.find_one({"_id": user.id})
	if not exists:
		data = battledata(user)
		db.battles.insert_one(data)


class battle(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.group()
	@commands.guild_only()
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def battle(self, ctx):
		servercolor = ctx.author.color

		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed = discord.Embed(colour=servercolor)
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)

			try:
				await ctx.send(embed=embed)
			except:
				return
		return


	@battle.command(name="invite")
	@commands.guild_only()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def battle_invite(self, ctx, user: discord.Member):
		languageinfo = db.servers.find_one({"_id": ctx.guild.id})
		language = languageinfo["language"]

		author = ctx.author

		# INVITER
		authorinfo = db.users.find_one({"_id": author.id})

		# USER
		userinfo = db.users.find_one({"_id": user.id})

		# CHECK IF USERS CHALLANGES ITSELF
		if authorinfo["_id"] == userinfo["_id"]:
			await ctx.send("<:Solyx:560809141766193152> **| You cant fight yourself.**")
			return

		# CHECK IF USERS EXIST
		if authorinfo["race"] == "None" or authorinfo["class"] == "None":
			await ctx.send(
				fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(
				fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		# CHECK IF USERS HAVE ENOUGH HP
		if authorinfo["health"] <= 0:
			await ctx.send("<:Solyx:560809141766193152> **| You cannot fight with 0 HP!**")
			return

		if userinfo["health"] <= 0:
			await ctx.send("<:Solyx:560809141766193152> **| {} does not have enough HP.**".format(user.name))
			return

		# CHECK IF USERS HAVE BATTLE INFO
		await _create_battle(author)
		await _create_battle(user)
		authorbattleinfo = db.battles.find_one({"_id": author.id})
		userbattleinfo = db.battles.find_one({"_id": user.id})

		# CHECK IF USERS ARE IN BATTLE
		if not authorbattleinfo["battle_enemy"] == "None":
			await ctx.send("<:Solyx:560809141766193152> **| You are currently in battle.**")
			return
		if not userbattleinfo["battle_enemy"] == "None":
			await ctx.send("<:Solyx:560809141766193152> **| {} is currently in battle.**".format(user.name))
			return

		await ctx.send("{}".format(user.mention))
		em = discord.Embed(title="Battle invite", description="{} (Rank: {}) has invited you to battle!\nDo you accept?".format(author.mention, authorbattleinfo["battle_rank"]), color=discord.Colour(0xffffff))
		em.set_footer(text="Say yes/no")
		# em.set_thumbnail(url=RankSwordsPLZ)
		await ctx.send(embed=em)
		answer1 = await self.check_answer_other_user(ctx, user, ["yes", "no", "n", "y", "Y", "Yes", "N", "No"])
		if answer1 in ["y", "yes", "Y", "Yes"]:
			userbattleinfo["battle_enemy"] = author.id
			userbattleinfo["battle_turn"] = "True"
			userbattleinfo["battle_active"] = "True"
			userbattleinfo["lastmove"] = round(time())
			db.battles.replace_one({"_id": user.id}, userbattleinfo, upsert=True)

			authorbattleinfo["battle_enemy"] = user.id
			authorbattleinfo["battle_turn"] = "False"
			authorbattleinfo["battle_active"] = "True"
			authorbattleinfo["lastmove"] = round(time())
			db.battles.replace_one({"_id": author.id}, authorbattleinfo, upsert=True)

			em = discord.Embed(title="Battle Accepted", description="{} and {} are now fighting!".format(user.mention, author.mention), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)

			try:
				await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, {}".format(user.mention))
			except:
				pass

		elif answer1 in ["n", "no", "N", "No"]:
			await ctx.send("<:CrossShield:560804112548233217> **| Battle ignored.**")
			return


	@battle.command(name="fight")
	@commands.guild_only()
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def battle_fight(self, ctx):
		languageinfo = db.servers.find_one({"_id": ctx.guild.id})
		language = languageinfo["language"]

		user = ctx.author
		userinfo = db.users.find_one({"_id": user.id})
		battleinfo = db.battles.find_one({"_id": user.id})
		enemyid = battleinfo["battle_enemy"]
		enemyinfo = db.users.find_one({"_id": enemyid})
		enemybattleinfo = db.battles.find_one({"_id": enemyid})
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(
				fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo["health"] <= 0:
			await ctx.send("You cannot fight with 0 HP")
			return

		if battleinfo["battle_active"] == "False":
			await ctx.send("You are not in a battle!")
			return

		if battleinfo["battle_enemy"] == "None":
			await ctx.send("You are not in a battle!")
			return

		if battleinfo["battle_turn"] == "False":
			lastmove = enemybattleinfo["lastmove"]
			now = round(time())
			if lastmove and ((now - lastmove) > 9000):
				battleinfo["battle_active"] = "False"
				battleinfo["battle_enemy"] = "None"
				battleinfo["battle_turn"] = "False"
				db.battles.replace_one({"_id": user.id}, battleinfo)

				enemybattleinfo["battle_active"] = "False"
				enemybattleinfo["battle_enemy"] = "None"
				enemybattleinfo["battle_turn"] = "False"
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo)
				await ctx.send("Battle terminated due to inactivity!")
				return
			else:
				try:
					await ctx.send("<:Solyx:560809141766193152> | It isn't your turn, {}!".format(user.mention))
				except:
					pass
				return

		# - - - - - - - - - - - - - - - USER STATS CHECKS - - - - - - - - - - - - - - -
		mindmg = userinfo["equip"]["stats_min"]
		maxdmg = userinfo["equip"]["stats_max"]
		youdmg = random.randint(mindmg, maxdmg)

		# YOUR PROTECTION IS BASED ON THE ARMOR YOURE HOLDING
		youdef = 0

		if userinfo["class"] == "Paladin":
			youdef += random.randint(5, 10)
		elif userinfo["class"] == "Knight":
			youdef += random.randint(8, 15)
		elif userinfo["class"] == "Grand Paladin":
			youdef += random.randint(11, 20)
		try:
			mindef = userinfo["wearing"]["stats_min"]
			maxdef = userinfo["wearing"]["stats_max"]
			youdef = random.randint(mindef, maxdef)
		except:
			pass
		# - - - - - - - - - - - - - - - ENEMY STATS CHECKS - - - - - - - - - - - - - - -
		mindmg = enemyinfo["equip"]["stats_min"]
		maxdmg = enemyinfo["equip"]["stats_max"]
		enemydmg = random.randint(mindmg, maxdmg)

		# YOUR PROTECTION IS BASED ON THE ARMOR YOURE HOLDING
		enemydef = 0

		if userinfo["class"] == "Knight":
			youdef += random.randint(5, 10)
		elif userinfo["class"] == "Paladin":
			youdef += random.randint(8, 15)
		elif userinfo["class"] == "Grand Paladin":
			youdef += random.randint(11, 20)

		try:
			mindef = enemyinfo["wearing"]["stats_min"]
			maxdef = enemyinfo["wearing"]["stats_max"]
			enemydef = random.randint(mindef, maxdef)
		except:
			pass

		# GUILD BOOST
		try:
			guild = ctx.guild
			guildinfo = db.servers.find_one({"_id": guild.id})
			guildbonus = guildinfo["bonus"]  # CHECK THIS - unused
		except:
			guildbonus = 0

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

		# iF FOR WHATEVER REASON THE USER DOES -fight AGAIN, RETURN
		em = discord.Embed(
			title=fileIO(f"data/languages/{language}.json", "load")["fight"]["skill"]["title"]["translation"],
			description="\n".join(show_list), color=discord.Colour(0xffffff))
		em.set_author(name=fileIO(f"data/languages/{language}.json", "load")["fight"]["skill"]["author"]["translation"],
					icon_url=ctx.message.author.avatar_url)
		skillmsg = await ctx.send(embed=em)
		monstercolor = discord.Colour(0xffffff)

		if userinfo["Stunned"] > 0:
			userhealth = userinfo["health"]
			enemydmg = 0
			enemyhp = enemyinfo["health"]
			enemyhp -= youdmg
			# If enemydmg is lower then 0 its 0
			if enemydmg < 0:
				enemydmg = 0
			# If User health is lower then 0 its 0
			if userhealth < 0:
				userhealth = 0
			# If enemyhealth is lower then 0 its 0
			if enemyhp < 0:
				enemyhp = 0
			em4 = discord.Embed(
				description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
					enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
					userinfo["Stunned"], enemyinfo["name"], userinfo["name"], enemydmg, enemyinfo["name"], enemyhp,
					userinfo["name"], userhealth), color=monstercolor)

			# if item has no image none gets added.
			if not userinfo["equip"]["image"] == "None":
				em4.set_thumbnail(url=userinfo["equip"]["image"])

			enemyinfo["Stunned"] = enemyinfo["Stunned"] - 1
			if enemyinfo["Stunned"] <= 0:
				enemyinfo["Stunned"] = 0

			userinfo["Stunned"] = userinfo["Stunned"] - 1
			if userinfo["Stunned"] <= 0:
				userinfo["Stunned"] = 0

			userinfo["pvpcooldown1"] = userinfo["pvpcooldown1"] - 1
			if userinfo["pvpcooldown1"] <= 0:
				userinfo["pvpcooldown1"] = 0

			userinfo["pvpcooldown2"] = userinfo["pvpcooldown2"] - 1
			if userinfo["pvpcooldown2"] <= 0:
				userinfo["pvpcooldown2"] = 0

			enemyinfo["pvpcooldown1"] = enemyinfo["pvpcooldown1"] - 1
			if enemyinfo["pvpcooldown1"] <= 0:
				enemyinfo["pvpcooldown1"] = 0

			enemyinfo["pvpcooldown2"] = enemyinfo["pvpcooldown2"] - 1
			if enemyinfo["pvpcooldown2"] <= 0:
				enemyinfo["pvpcooldown2"] = 0

			timestamp = round(time())
			enemybattleinfo["battle_turn"] = "True"
			enemybattleinfo["lastmove"] = timestamp
			battleinfo["battle_turn"] = "False"
			battleinfo["lastmove"] = timestamp

			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
			db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
			db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
			# Tries to send msg.
			try:
				await skillmsg.edit(embed=em4)
			except:
				try:
					await ctx.send(
						fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return

		answer2 = await self.check_answer(ctx, options)

		# DEFINE WHAT SKILL WE SELECTED
		# Done
		if answer2 == "cast" or answer2 == "Cast":

			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
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
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
				enemyhp = enemyinfo["health"]
				enemyhp -= youdmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)

				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["Debuff1"] == "Surge":
				youdmg = 0
				enemyhp = enemyinfo["health"]
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

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**you have been stunned for 1 turn**\n**{} Hits {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["Debuff1"] == "Arise" and userinfo["Debuff1Time"] > 0:

				enemyhp = enemyinfo["health"]
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

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n** {} uses {} and hits {} for {} damage.\n The army of skeletons attacks.\nDealing {} damage each\nDealing a total of {} damage.\n{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], youdmg, hit, totaldmg, enemyinfo["name"], userinfo["name"], enemydmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				enemyhp = enemyinfo["health"]
				userhealth = userinfo["health"]
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# Users HP after dmg taken.
				userhealth -= enemydmg
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg

				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp,
						userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		# Done
		elif answer2 == "shoot" or answer2 == "Shoot":

			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Shoot"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef

			enemyhp = enemyinfo["health"]
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
			if userinfo["Debuff1"] == "Corrupt" and userinfo["Debuff1Time"] > 0 and enemyinfo["Stunned"] > 0:
				youdmg = int((youdmg / 100) * 130)
				enemydmg = 0

				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} Has been corrupted for {} turns.**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], enemyinfo["name"], userinfo["Debuff1Time"], userinfo["name"], move, youdmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			# stunned
			elif enemyinfo["Stunned"] > 0:
				enemydmg = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			# Buffs
			elif userinfo["Debuff1"] == "Corrupt":
				youdmg = int((youdmg / 100) * 130)
				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				bufftime = userinfo["Debuff1Time"]
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has corrupted {} for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						enemyinfo["name"], bufftime, enemyinfo["name"], userinfo["name"], enemydmg, userinfo["name"],
						enemyinfo["name"], youdmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp,
						userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return


		# Done
		elif answer2 == "swing" or answer2 == "Swing":

			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Swing"
			# Users HP
			userhealth = userinfo["health"]

			# Lootbag chance.
			lootbag = random.randint(1, 30)

			enemyhp = enemyinfo["health"]
			# Acutal fight msg.
			if enemyinfo["Stunned"] > 0:
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
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			if userinfo["Debuff1"] == "Blockade":

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
				userinfo["pvpcooldown2"] = 5
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has the blockade buff doubling defense. {} uses {} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						userinfo["name"], move, enemyinfo["name"], youdmg, enemyinfo["name"], userinfo["name"], enemydmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			elif userinfo["Debuff1"] == "Slice":

				enemyhp = enemyinfo["health"]
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

				bufftime = userinfo["Debuff1Time"]
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n {} Has bleeding effect for {} turns.**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, enemyinfo["name"], bufftime, userinfo["name"], move, youdmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				# Users Defense
				enemydmg -= youdef
				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg
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
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp,
						userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return


		# Done
		elif answer2 == "stab" or answer2 == "Stab":

			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
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
			if enemyinfo["Stunned"] > 0:

				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg
				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			# Buffs
			elif userinfo["Debuff1"] == "Rupture":

				enemyhp = enemyinfo["health"]
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

				bufftime = userinfo["Debuff1Time"]
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n {} Has bleeding effect for {} turns.**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, enemyinfo["name"], bufftime, userinfo["name"], move, youdmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			# Warp Buff

			elif userinfo["Debuff1"] == "Warp" and userinfo["Debuff1Time"] > 0:

				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg
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
				userinfo["pvpcooldown1"] = 3
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, But {} has warp debuff.\n the enemy damage is lowered by 60%**\n**{} hits {} for {} damage\n{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], userinfo["name"], enemyinfo["name"], enemydmg, userinfo["name"],
						enemyinfo["name"], youdmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp,
						userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		# Done
		elif answer2 == "parry" or answer2 == "Parry":
			# Stun the enemy for 1 turn. 3 turns cooldown.

			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Parry"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef
			# Enemy Hp
			enemyhp = enemyinfo["health"]
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

			if userinfo["Debuff1"] == "Rupture" and userinfo["pvpcooldown1"] == 0:

				enemydmg = 0

				youdmg = 0
				enemyinfo["Stunned"] = 2
				userinfo["pvpcooldown1"] = 4
				stun = 1
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

				bufftime = userinfo["Debuff1Time"]
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turn\n {} Has bleeding effect for {} turns.**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], stun, enemyinfo["name"], bufftime, enemyinfo["name"], enemyhp,
						userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["pvpcooldown1"] == 0:
				enemydmg = 0

				youdmg = 0
				enemyinfo["Stunned"] = 2
				userinfo["pvpcooldown1"] = 4
				stun = 1

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turn**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], stun, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["Debuff1"] == "Rupture":

				enemydmg = 0

				youdmg = 0
				enemyinfo["Stunned"] = 2
				userinfo["pvpcooldown1"] = 4
				stun = 1
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

				bufftime = userinfo["Debuff1Time"]
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turn\n {} Has bleeding effect for {} turns.**\n**\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], stun, enemyinfo["name"], bufftime, enemyinfo["name"], enemyhp,
						userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown1"] = userinfo["pvpcooldown1"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown1"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		# Done
		elif answer2 == "distort" or answer2 == "Distort":
			# Distorts the enemy for 50% less dmg. 2 turns cooldown.

			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Distort"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef
			# Enemy Hp
			enemyhp = enemyinfo["health"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)
			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			if enemyinfo["Stunned"] > 0:
				enemydmg = 0

				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg

				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# If User health is lower then 0 its 0
				if userhealth < 0:
					userhealth = 0

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns Distort had no use.**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			elif userinfo["Debuff1"] == "Warp" and userinfo["Debuff1Time"] > 0:
				enemydmg = 0
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# set skill cooldown
				userinfo["pvpcooldown1"] = 3
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, But {} has warp debuff.\n the enemy damage is 0.**\n**{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], userinfo["name"], enemyinfo["name"], youdmg, enemyinfo["name"], enemyhp,
						userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["pvpcooldown1"] == 0:
				enemydmg = int((enemydmg / 100) * 50)

				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg
				# set skill cooldown
				userinfo["pvpcooldown1"] = 3
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, halving the damage**\n**{} hits {} for {} damage**\n**{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], userinfo["name"], enemydmg, userinfo["name"], enemyinfo["name"], youdmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown1"] = userinfo["pvpcooldown1"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown1"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
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
			enemyhp = enemyinfo["health"]
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

			if enemyinfo["Stunned"] > 0:
				enemydmg = 0

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			elif userinfo["Debuff1"] == "Arise" and userinfo["Debuff1Time"] > 0 and userinfo["pvpcooldown1"] == 0:
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

				# Set enemy dmg to 0 due to reap action
				0

				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# Set skill cooldown.
				userinfo["pvpcooldown1"] = 3
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and 30% of {} Health.\n{} Hp healed! The army of skeletons attacks.\nDealing {} damage each\nDealing a total of {} damage.\n{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], reap, hit, totaldmg, userinfo["name"], enemyinfo["name"], youdmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["pvpcooldown1"] == 0:
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
				# Set enemy dmg to 0 due to reap action
				enemydmg = 0
				# Set skill cooldown.
				userinfo["pvpcooldown1"] = 3
				em3 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Reaps 30% of {} Health.\n{} Hp healed!**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						enemyinfo["name"], reap, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em3.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em3)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown1"] = userinfo["pvpcooldown1"] + 1
				if userinfo["Debuff1"] == "Arise" and userinfo["Debuff1Time"] > 0:
					userinfo["Debuff1Time"] += 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown1"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
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
			enemyhp = enemyinfo["health"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			if enemyinfo["Stunned"] > 0:
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
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return


			elif userinfo["Debuff1"] == "Surge":
				youdmg = 0
				enemyhp = enemyinfo["health"]
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

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**you have been stunned for 1 turn**\n**{} Hits {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["pvpcooldown1"] == 0:
				overloaddmg = int((youdmg / 100) * 40)

				overloadselfdmg = int((overloaddmg / 100) * 50)

				youdmg += overloaddmg
				enemydmg += overloadselfdmg
				userhealth = userhealth - enemydmg - overloadselfdmg
				enemyhp = enemyinfo["health"] - youdmg

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
				userinfo["pvpcooldown1"] = 2
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} overloads {} for {} damage\nBut also deals {} self damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, userinfo["name"], enemyinfo["name"], youdmg, overloadselfdmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown1"] = userinfo["pvpcooldown1"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown1"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
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
			enemyhp = enemyinfo["health"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			if enemyinfo["Stunned"] > 0:
				enemydmg = 0

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			if userinfo["Debuff1"] == "Blockade":

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
				userinfo["pvpcooldown2"] = 5
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has the blockade buff doubling defense.\n{} hits {} for {} damage**\n**{} uses {} and does a series of hits.**\n**Dealing {} damage each**\n**Dealing a total of {} damage.**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						enemyinfo["name"], userinfo["name"], enemydmg, userinfo["name"], move, hit, totaldmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["pvpcooldown1"] == 0:
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
				userinfo["pvpcooldown1"] = 4
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and does a series of hits.**\n**Dealing {} damage each**\n**Dealing a total of {} damage.**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, userinfo["name"], move, hit, totaldmg, enemyinfo["name"], enemyhp,
						userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown1"] = userinfo["pvpcooldown1"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown1"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
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
			enemyhp = enemyinfo["health"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			if enemyinfo["Stunned"] > 0:
				enemydmg = 0

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			elif userinfo["Debuff1"] == "Slice":

				enemyhp = enemyinfo["health"]
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

				bufftime = userinfo["Debuff1Time"]
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage\n {} Has bleeding effect for {} turns.**\n**{} uses {}  and has a Critical hit! for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, enemyinfo["name"], bufftime, userinfo["name"], move, youdmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["pvpcooldown1"] == 0:
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
				userinfo["pvpcooldown1"] = 3
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and has a Critical hit! for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp,
						userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				userinfo["pvpcooldown1"] = userinfo["pvpcooldown1"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown1"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		# done
		elif answer2 == "strike" or answer2 == "Strike":
			# Strike Deals a critical hit to the knee immobilizing them for 2 turns while dealing 50% damage. has a 6 turn cooldown.

			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Strike"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef
			# Enemy Hp
			enemyhp = enemyinfo["health"]
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
			if userinfo["pvpcooldown1"] == 0:
				enemydmg = 0

				youdmg = int((youdmg / 100) * 50)
				enemyinfo["Stunned"] = 3

				stun = 2
				# deals dmg to enemy
				enemyhp = enemyhp - youdmg

				# If enemydmg is lower then 0 its 0
				if enemydmg < 0:
					enemydmg = 0
				# If enemyhealth is lower then 0 its 0
				if enemyhp < 0:
					enemyhp = 0
				# Set skill cooldown.
				userinfo["pvpcooldown1"] = 6
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and stuns {} for {} turns\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], stun, userinfo["name"], enemyinfo["name"], youdmg, enemyinfo["name"],
						enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown1"] = userinfo["pvpcooldown1"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown1"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		# done
		elif answer2 == "corrupt" or answer2 == "Corrupt":
			# Corrupts the enemy for 2 turns taking 30% damage extra, or ends when enemy dies. 4 turn cooldown.

			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Corrupt"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef
			# Enemy Hp
			enemyhp = enemyinfo["health"]
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
			if userinfo["pvpcooldown1"] == 0:
				# add buff and timer
				userinfo["Debuff1"] = "Corrupt"
				userinfo["Debuff1Time"] = 2
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
				userinfo["pvpcooldown1"] = 4
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and corrupts {} for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], bufftime, enemyinfo["name"], userinfo["name"], enemydmg, userinfo["name"],
						enemyinfo["name"], youdmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown1"] = userinfo["pvpcooldown1"] + 1
				userinfo["Debuff1Time"] = userinfo["Debuff1Time"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown1"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return


		elif answer2 == "Rupture" or answer2 == "rupture":
			# Rupture the enemy's artery 2 turns dealing 25% current hp bleeding dmg.  4 turn cooldown.

			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Rupture"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef
			# Enemy Hp
			enemyhp = enemyinfo["health"]
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
			if userinfo["pvpcooldown2"] == 0:
				# add buff and timer
				userinfo["Debuff1"] = "Rupture"
				userinfo["Debuff1Time"] = 2

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
				userinfo["pvpcooldown2"] = 4
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and Ruptures {} artery\n causing bleeding effect for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], bufftime, enemyinfo["name"], userinfo["name"], enemydmg, userinfo["name"],
						enemyinfo["name"], youdmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown2"] = userinfo["pvpcooldown2"] + 1
				userinfo["Debuff1Time"] = userinfo["Debuff1Time"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown2"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		elif answer2 == "Warp" or answer2 == "warp":
			# Warp the enemy's attacks for 2 turns dealing 60% Less damage.  5 turn cooldown.

			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Warp"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef
			# Enemy Hp
			enemyhp = enemyinfo["health"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			# Acutal fight msg.
			if userinfo["pvpcooldown2"] == 0:
				# add buff and timer
				userinfo["Debuff1"] = "Warp"
				userinfo["Debuff1Time"] = 2

				enemydmg = int((enemydmg / 100) * 60)

				# Users HP after dmg taken.
				userhealth = userhealth - enemydmg
				# Enemys Hp after userdmg
				enemyhp = enemyinfo["health"] - youdmg
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
				userinfo["pvpcooldown2"] = 5
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {}, Warping {} Attack dealing 60% less damage**\n**{} hits {} for {} damage**\n**{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], enemyinfo["name"], userinfo["name"], enemydmg, userinfo["name"],
						enemyinfo["name"], youdmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				userinfo["pvpcooldown2"] = userinfo["pvpcooldown2"] + 1
				userinfo["Debuff1Time"] = userinfo["Debuff1Time"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown2"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
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
			enemyhp = enemyinfo["health"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			if enemyinfo["Stunned"] > 0:
				enemydmg = 0

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["pvpcooldown2"] == 0:
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
				userinfo["Debuff1"] = "Arise"
				userinfo["Debuff1Time"] = 2
				# Set skill cooldown.
				userinfo["pvpcooldown2"] = 8
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and Raises a small army of skeletons!.**\n**Dealing {} damage each**\n**Dealing a total of {} damage.\n{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, userinfo["name"], move, hit, totaldmg, userinfo["name"],
						enemyinfo["name"], youdmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				userinfo["pvpcooldown2"] = userinfo["pvpcooldown2"] + 1
				userinfo["Debuff1Time"] = userinfo["Debuff1Time"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown2"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
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
			enemyhp = enemyinfo["health"]
			# Lootbag chance.
			lootbag = random.randint(1, 30)

			# If UserHealth is More then Maxhealth its Maxhealth
			if userhealth >= userinfo["MaxHealth"]:
				userhealth = userinfo["MaxHealth"]

			if enemyinfo["Stunned"] > 0:
				enemydmg = 0

				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} Has been stunned for {} turns**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						enemyinfo["Stunned"], userinfo["name"], move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				# if item has no image none gets added.
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				# Tries to send msg.
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			elif userinfo["pvpcooldown2"] == 0:

				youdmg = youdmg * 3

				userhealth = userhealth - enemydmg
				enemyhp = enemyinfo["health"] - youdmg

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
				userinfo["pvpcooldown2"] = 4
				userinfo["Debuff1"] = "Surge"
				userinfo["Debuff1Time"] = 2
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} gains a power surge and triples their damage.\n total damage {}Hp\nBut stun yourself for 1 turn.**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], enemyinfo["name"],
						userinfo["name"], enemydmg, userinfo["name"], youdmg, enemyinfo["name"], enemyhp, userinfo["name"],
						userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown2"] = userinfo["pvpcooldown2"] + 1
				userinfo["Debuff1Time"] = userinfo["Debuff1Time"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown2"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return


		elif answer2 == "Slice" or answer2 == "slice":
			# SLice causes 2 round bleeding effect(25% current health), 30% increased damage 4 turn cooldown.
			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Slice"
			# Users HP
			userhealth = userinfo["health"]
			# Users Defense
			enemydmg -= youdef
			# Enemy Hp
			enemyhp = enemyinfo["health"]
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
			if userinfo["pvpcooldown2"] == 0:
				# add buff and timer
				userinfo["Debuff1"] = "Slice"
				userinfo["Debuff1Time"] = 2
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
				userinfo["pvpcooldown2"] = 4
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and Slices {}\n causing bleeding effect for {} turns\n{} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], bufftime, enemyinfo["name"], userinfo["name"], enemydmg, userinfo["name"],
						enemyinfo["name"], youdmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown2"] = userinfo["pvpcooldown2"] + 1
				userinfo["Debuff1Time"] = userinfo["Debuff1Time"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown2"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return


		elif answer2 == "Blockade" or answer2 == "blockade":
			# Blockade Dubbles your armor for 2 turns! dealing 15% less damage. 5 turn cooldown.
			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Blockade"
			# Users HP
			userhealth = userinfo["health"]

			# Enemy Hp
			enemyhp = enemyinfo["health"]
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
			if userinfo["pvpcooldown2"] == 0:
				# add buff and timer
				userinfo["Debuff1"] = "Blockade"
				userinfo["Debuff1Time"] = 2
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
				userinfo["pvpcooldown2"] = 5
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and Dubbles their defense for 2 turns.\n{} hits {} for {} damage\n{} Hits {} for {} Damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], userinfo["name"], enemydmg, userinfo["name"], enemyinfo["name"], youdmg,
						enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			else:
				userinfo["pvpcooldown2"] = userinfo["pvpcooldown2"] + 1
				userinfo["Debuff1Time"] = userinfo["Debuff1Time"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown2"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		elif answer2 == "Sneak" or answer2 == "sneak":
			# Sneak around your enemy and delivering a critical hit dealing 150% and not taking any dmg! 4 turn cooldown.
			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Sneak"
			# Users HP
			userhealth = userinfo["health"]

			# Enemy Hp
			enemyhp = enemyinfo["health"]
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

			if userinfo["pvpcooldown2"] == 0:
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
				userinfo["pvpcooldown2"] = 4
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and comes out the shadows.\nYou deal a critical hit! for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, youdmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth), color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				userinfo["pvpcooldown2"] = userinfo["pvpcooldown2"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown2"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		elif answer2 == "Snipe" or answer2 == "snipe":
			# Snipe your enemy from afer taking no damage but headshotting the enemy dealing 250% of your base dmg. 6 turn cooldown.
			# If enemy stunned no dmg
			if enemyinfo["Stunned"] > 0:
				enemydmg = 0
			# Move user makes
			move = "Snipe"
			# Users HP
			userhealth = userinfo["health"]

			# Enemy Hp
			enemyhp = enemyinfo["health"]
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

			if userinfo["pvpcooldown2"] == 0:
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
				userinfo["pvpcooldown2"] = 5
				em4 = discord.Embed(
					description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and headshots {}.\nYou deal a critical hit! for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(
						enemyinfo["name"], enemyinfo["health"], userinfo["name"], userinfo["health"], userinfo["name"],
						move, enemyinfo["name"], youdmg, enemyinfo["name"], enemyhp, userinfo["name"], userhealth),
					color=monstercolor)
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)

				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
			else:
				userinfo["pvpcooldown2"] = userinfo["pvpcooldown2"] + 1
				em4 = discord.Embed(
					description="**Skill:**\n**{}** is on a **{} turn** cooldown.".format(move, userinfo["pvpcooldown2"]),
					color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em4.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em4)
				except:
					try:
						await ctx.send(
							fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

			# iF SELECTED A SKILL, FIGHT

			if enemyhp <= 0 and userhealth <= 0:
				em = discord.Embed(description=":skull: You both died!", color=discord.Colour(0x000000))
				await ctx.send(embed=em)
				userinfo["health"] = 0
				battleinfo["battle_active"] = "False"
				battleinfo["battle_enemy"] = "None"
				battleinfo["battle_streak"] = 0

				enemyinfo["health"] = 0
				enemybattleinfo["battle_active"] = "False"
				enemybattleinfo["battle_enemy"] = "None"
				enemybattleinfo["battle_streak"] = 0

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)

			elif userhealth <= 0:
				xpgain = random.randint(10, 15)
				em = discord.Embed(
					description=":crown: <@{}> **won!** :crown:\n:sparkles: +{} Exp".format(battleinfo["battle_enemy"],
																							xpgain),
					color=discord.Colour(0xffdf00))
				await ctx.send(embed=em)

				battleinfo["battle_active"] = "False"
				battleinfo["battle_enemy"] = "None"
				battleinfo["battle_streak"] = 0
				battleinfo["battle_losses"] = battleinfo["battle_losses"] + 1

				enemybattleinfo["battle_active"] = "False"
				enemybattleinfo["battle_enemy"] = "None"
				enemybattleinfo["battle_streak"] = enemybattleinfo["battle_streak"] + 1
				enemybattleinfo["battle_wins"] = enemybattleinfo["battle_wins"] + 1
				enemyinfo["exp"] = enemyinfo["exp"] + xpgain

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)

			elif enemyhp <= 0:
				xpgain = random.randint(10, 15)
				em = discord.Embed(
					description=":crown: {} **won!** :crown:\n:sparkles: +{} Exp".format(user.mention, xpgain),
					color=discord.Colour(0xffdf00))
				await asyncio.sleep(1)
				await ctx.send(embed=em)

				battleinfo["battle_active"] = "False"
				battleinfo["battle_enemy"] = "None"
				battleinfo["battle_streak"] = battleinfo["battle_streak"] + 1
				battleinfo["battle_wins"] = battleinfo["battle_wins"] + 1
				userinfo["exp"] = userinfo["exp"] + xpgain

				enemybattleinfo["battle_active"] = "False"
				enemybattleinfo["battle_enemy"] = "None"
				enemybattleinfo["battle_streak"] = 0
				enemybattleinfo["battle_losses"] = enemybattleinfo["battle_losses"] + 1

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)

			else:
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
					enemyinfo["Stunned"] = enemyinfo["Stunned"] - 1
					userinfo["Stunned"] = userinfo["Stunned"] - 1
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
					db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
					db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
					db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)
				except:
					pass

				timestamp = round(time())
				enemybattleinfo["battle_turn"] = "True"
				enemybattleinfo["lastmove"] = timestamp
				battleinfo["battle_turn"] = "False"
				battleinfo["lastmove"] = timestamp

				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
				db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
				db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)

				await self._level_up_check_user(ctx, user)

	@battle.command(name="quit")
	@commands.guild_only()
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def battle_quit(self, ctx):
		languageinfo = db.servers.find_one({"_id": ctx.guild.id})
		language = languageinfo["language"]

		user = ctx.author
		userinfo = db.users.find_one({"_id": user.id})
		battleinfo = db.battles.find_one({"_id": user.id})
		enemyid = battleinfo["battle_enemy"]
		enemyinfo = db.users.find_one({"_id": enemyid})
		enemybattleinfo = db.battles.find_one({"_id": enemyid})
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(
				fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(
					ctx.prefix))
			return

		if userinfo["health"] <= 0:
			await ctx.send("You cannot quit with 0 HP")
			return

		if battleinfo["battle_active"] == "False":
			await ctx.send("You are not in a battle!")
			return

		if battleinfo["battle_enemy"] == "None":
			await ctx.send("You are not in a battle!")
			return

		em = discord.Embed(description="**Are you sure you want to quit this battle?**",
						color=discord.Colour(0xffffff))
		em.set_footer(text="Type yes to quit.")
		await ctx.send(embed=em)

		answer1 = await self.check_answer(ctx, ["yes", "y", "Yes", "Y", "ja", "Ja", "j", "J"])

		if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "Ja" or answer1 == "ja" or answer1 == "j" or answer1 == "J":

			enemygold = 30  # CHECK THIS - unused
			xpgain = 15  # CHECK THIS - unused
			goldlost = 100

			em = discord.Embed(
				description=":crown: <@{}> **won!** :crown:\n:sparkles: +{} Exp and +{}Gold\n\n{} **Has quit the battle and gets a -{} gold penalty**".format(
					battleinfo["battle_enemy"], xpgain, enemygold, user.mention, goldlost),
				color=discord.Colour(0xffdf00))
			await ctx.send(embed=em)
			userinfo["gold"] = userinfo["gold"] - goldlost
			if userinfo["gold"] < 0:
				userinfo["gold"] = 0

			battleinfo["battle_active"] = "False"
			battleinfo["battle_enemy"] = "None"
			battleinfo["battle_streak"] = 0
			battleinfo["battle_losses"] = battleinfo["battle_losses"] + 1

			enemybattleinfo["battle_active"] = "False"
			enemybattleinfo["battle_enemy"] = "None"
			enemybattleinfo["battle_streak"] = enemybattleinfo["battle_streak"] + 1
			enemybattleinfo["battle_wins"] = enemybattleinfo["battle_wins"] + 1
			enemyinfo["exp"] = enemyinfo["exp"] + 15
			enemyinfo["gold"] = enemyinfo["gold"] + 30

			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			db.battles.replace_one({"_id": user.id}, battleinfo, upsert=True)
			db.users.replace_one({"_id": enemyid}, enemyinfo, upsert=True)
			db.battles.replace_one({"_id": enemyid}, enemybattleinfo, upsert=True)

			await _level_up_check_user(self, ctx, user)

	
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
	n = battle(bot)
	bot.add_cog(n)
