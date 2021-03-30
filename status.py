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


class status(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

	
	@commands.command(pass_context=True, aliases=["stats 2"], no_pm=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def equipment(self, ctx):	
		
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has Checked their status")

		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return


		if userinfo["role"] == "Developer":

			maxexp = 100 + ((userinfo["lvl"] + 1) * 3.5)
			if not userinfo["guild"] == "None":
				try:
					guildid = userinfo["guild"]
					userguild = self.bot.get_guild(guildid)
				except:
					userguild = guild
			else:
				userguild = guild

			
			if not userinfo["equip"] == "None":
				type = userinfo["equip"]["type"]
				if type == "sword":
					weapon = "<:Sword:573576884688781345>"
				if type == "bow":
					weapon = "<:Bow:573576981791113218>"
				if type == "staff":
					weapon = "<:Staff:573578258419810335>"
				if type == "mace":
					weapon = "<:Mace:761025040145186846>"
				if type == "dagger":
					weapon = "<:Dagger:761025864422916096>"
				if type == "gun":
					weapon = "<:Gun:573578066853494830>"
				
				weaponequipped = userinfo["equip"]["name"]
				item = userinfo["equip"]["stats_min"]
				item2 = userinfo["equip"]["stats_max"]
			else:
				weaponequipped = "None"
				item = ""
				item2 = ""
				weapon = ":crossed_swords:"

			if not userinfo["neck"] == "None":
				neckequipped = userinfo["neck"]["name"]
				neckstats1 = userinfo["neck"]["stats_min"]
				neckstats2 = userinfo["neck"]["stats_max"]
			else:
				neckequipped = "None"
				neckstats1 = ""
				neckstats2 = ""
			
			if not userinfo["head"] == "None":
				headequipped = userinfo["head"]["name"]
				headstats1 = userinfo["head"]["stats_min"]
				headstats2 = userinfo["head"]["stats_max"]
			else:
				headequipped = "None"
				headstats1 = ""
				headstats2 = ""
			
			if not userinfo["body"] == "None":
				bodyequipped = userinfo["body"]["name"]
				bodystats1 = userinfo["body"]["stats_min"]
				bodystats2 = userinfo["body"]["stats_max"]
			else:
				bodyequipped = "None"
				bodystats1 = ""
				bodystats2 = ""
			
			if not userinfo["finger"] == "None":
				fingerequipped = userinfo["finger"]["name"]
				fingerstats1 = userinfo["finger"]["stats_min"]
				fingerstats2 = userinfo["finger"]["stats_max"]
			else:
				fingerequipped = "None"
				fingerstats1 = ""
				fingerstats2 = ""

			if not userinfo["legs"] == "None":
				legsequipped = userinfo["legs"]["name"]
				legsstats1 = userinfo["legs"]["stats_min"]
				legsstats2 = userinfo["legs"]["stats_max"]
			else:
				legsequipped = "None"
				legsstats1 = ""
				legsstats2 = ""

			if not userinfo["feet"] == "None":
				feetequipped = userinfo["feet"]["name"]
				feetstats1 = userinfo["feet"]["stats_min"]
				feetstats2 = userinfo["feet"]["stats_max"]
			else:
				feetequipped = "None"
				feetstats1 = ""
				feetstats2 = ""

			

		

			em = discord.Embed(color=discord.Colour(0xffffff))
			em.add_field(name="Weapon", value="{} {}\n{} **Weapon Damage:** {}-{}\n".format(weapon, weaponequipped, weapon, item, item2 ), inline=False)
			em.add_field(name="Head", value=":military_helmet: *{}*\n :military_helmet: **Stats:** {} - {}<:Shield:573576333863682064>\n".format(headequipped, headstats1, headstats2), inline=False)
			em.add_field(name="Neck", value=":prayer_beads: *{}*\n :prayer_beads: **Stats:** {} - {}<:Shield:573576333863682064>\n".format(neckequipped, neckstats1, neckstats2 ), inline=False)
			em.add_field(name="Body", value=":shirt:*{}*\n :shirt:**Stats:** {} - {}<:Shield:573576333863682064>\n".format(bodyequipped, bodystats1, bodystats2), inline=False)
			em.add_field(name="Finger", value=":ring: *{}*\n :ring: **Stats:** {} - {}:crossed_swords:\n".format(fingerequipped, fingerstats1, fingerstats2), inline=False)
			em.add_field(name="Legs", value=":jeans:*{}*\n :jeans:**Stats:** {} - {}<:Shield:573576333863682064>\n".format(legsequipped, legsstats1, legsstats2), inline=False)
			em.add_field(name="Feet", value=":boot: *{}*\n :boot: **Stats:** {} - {}<:Shield:573576333863682064>\n".format(feetequipped, feetstats1, feetstats2), inline=False)
			em.set_author(name="{}'s Equipment".format(userinfo["name"]), icon_url=user.avatar_url)
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return




# - - - User info - - - WORKS

	@commands.command(pass_context=True, aliases=["stats"], no_pm=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def status(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has Checked their status")

		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["questname"] == "Basic A":
			userinfo["questprogress"] = userinfo["questprogress"] + 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			if userinfo["questprogress"] >= 1:
				await ctx.send("Quest Updated! Type **{}quests** To check quest progress!".format(ctx.prefix))
			pass








		if userinfo["role"] == "Developer":
			try:
				maxexp = 100 + ((userinfo["lvl"] + 1) * 3.5)
				if not userinfo["guild"] == "None":
					try:
						guildid = userinfo["guild"]
						userguild = self.bot.get_guild(guildid)
					except:
						userguild = guild
				else:
					userguild = guild

				if not userinfo["equip"] == "None":
					weaponequipped = userinfo["equip"]["name"]
					item = userinfo["equip"]["stats_min"]
					item2 = userinfo["equip"]["stats_max"]
				else:
					weaponequipped = "None"
					item = ""
					item2 = ""


				if not userinfo["neck"] == "None":
					neckequipped = userinfo["neck"]["name"]
					neckstats1 = userinfo["neck"]["stats_min"]
					neckstats2 = userinfo["neck"]["stats_max"]
				else:
					neckequipped = "None"
					neckstats1 = 0
					neckstats2 = 0
			
				if not userinfo["head"] == "None":
					headequipped = userinfo["head"]["name"]
					headstats1 = userinfo["head"]["stats_min"]
					headstats2 = userinfo["head"]["stats_max"]
				else:
					headequipped = "None"
					headstats1 = 0
					headstats2 = 0
			
				if not userinfo["body"] == "None":
					bodyequipped = userinfo["body"]["name"]
					bodystats1 = userinfo["body"]["stats_min"]
					bodystats2 = userinfo["body"]["stats_max"]
				else:
					bodyequipped = "None"
					bodystats1 = 0
					bodystats2 = 0
			
				if not userinfo["finger"] == "None":
					fingerequipped = userinfo["finger"]["name"]
					fingerstats1 = userinfo["finger"]["stats_min"]
					fingerstats2 = userinfo["finger"]["stats_max"]
				else:
					fingerequipped = "None"
					fingerstats1 = 0
					fingerstats2 = 0

				if not userinfo["legs"] == "None":
					legsequipped = userinfo["legs"]["name"]
					legsstats1 = userinfo["legs"]["stats_min"]
					legsstats2 = userinfo["legs"]["stats_max"]
				else:
					legsequipped = "None"
					legsstats1 = 0
					legsstats2 = 0

				if not userinfo["feet"] == "None":
					feetequipped = userinfo["feet"]["name"]
					feetstats1 = userinfo["feet"]["stats_min"]
					feetstats2 = userinfo["feet"]["stats_max"]
				else:
					feetequipped = "None"
					feetstats1 = 0
					feetstats2 = 0
				damage_bonus_min = fingerstats1
				damage_bonus_max = fingerstats2
				total_defense_min = neckstats1  +  headstats1  + bodystats1  + legsstats1 + feetstats1
				total_defense_max = neckstats2  +  headstats2  + bodystats2  + legsstats2 + feetstats2
				try:
					icon = ""
					Class = userinfo["class"]
					if Class == "Mage":
						icon = "<:Mage:752633441626882058> "
					if Class == "Elementalist":
						icon = "<:Elementalist:752638205584474164> "
					if Class == "Necromancer":
						icon = "<:Necromancer:752638205832069191> "
					if Class == "Developed Necromancer":
						icon = "<:Necromancer:752638205832069191> "
					if Class == "Adequate Elementalist":
						icon = "<:Elementalist:752638205584474164> "
					if Class == "Paladin":
						icon = "<:Paladin:752638205869949168> "
					if Class == "Samurai":
						icon = "<:Samurai:752638205920018603> "
					if Class == "Knight":
						icon = "<:Knight:752633441362903120> "
					if Class == "Master Samurai":
						icon = "<:Samurai:752638205920018603> "
					if Class == "Grand Paladin":
						icon = "<:Paladin:752638205869949168> "
					if Class == "Thief":
						icon = "<:Thief:752633441811693638> "
					if Class == "Mesmer":
						icon = "<:Mesmer:752638205697851413> "
					if Class == "Rogue":
						icon = "<:Rogue:752638205928538252> "
					if Class == "High Rogue":
						icon = "<:Rogue:752638205928538252> "
					if Class == "Adept Mesmer":
						icon = "<:Mesmer:752638205697851413> "
					if Class == "Archer":
						icon = "<:Archer:752633441282949222> "
					if Class == "Ranger":
						icon = "<:Ranger:752638206285185116> "
					if Class == "Assassin":
						icon = "<:Assassin:639473417791209472> "
					if Class == "Night Assassin":
						icon = "<:Assassin:639473417791209472> "
					if Class == "Skilled Ranger":
						icon = "<:Ranger:752638206285185116> "
				except:
					pass

			
				try:
					Race = ""
					Race = userinfo["race"]
					if Race == "Elf":
						ricon = "<:Elf:639474564023189554> "
					if Race == "Human":
						ricon = "<:Human:639474561355874304> "
					if Race == "Orc":
						ricon = "<:Orc:639474558109483028> "
					if Race == "Demon":
						ricon = "<:Demon:639474562463170590> "
				except:
					pass

				em = discord.Embed(description="**Name:** {}\n{}**Race:** {}\n{}**Class:** {}\n:scroll: **Title:** {}\n<:Guild:560844076967002112> **Guild:** {}\n\n<:Magic:560844225839890459> **Level:** {}\n<:Experience:560809103346368522> **Exp:** {} / {}\n<:HealthHeart:560845406750375937> **Health:** {} / {}\n\n**Pet:** {}".format(userinfo["name"], ricon, userinfo["race"], icon, userinfo["class"], userinfo["title"], userguild.name, userinfo["lvl"], userinfo["exp"], maxexp, userinfo["health"], userinfo["MaxHealth"], userinfo["equipped_pet"][0]["name"]), color=discord.Colour(0xffffff))
				em.add_field(name="Equipment", value=":crossed_swords: **Weapon:** {}\n:crossed_swords: **Weapon Damage:** {}-{}\n:crossed_swords: **Bonus Damage:** {}-{}\n\n <:Shield:573576333863682064>**Total defense:** *{} - {}*\n ".format(weaponequipped, item, item2, damage_bonus_min, damage_bonus_max, total_defense_min, total_defense_max ), inline=False)
				em.add_field(name="Tools", value="<:Axe:573574740220969007> **Axe level:** {}\n<:Pickaxe:573574740640530471> **Pickaxe level:** {}\n**Saw level:** {}\n**Chisel level:** {}\n**Hammer level:** {}".format(userinfo["axelvl"], userinfo["pickaxelvl"], userinfo["sawlvl"], userinfo["chisellvl"], userinfo["hammerlvl"]), inline=False)
				em.add_field(name="History", value="<:PvP:573580993055686657> **Kills:** {}\n:mouse_trap: **Trap Kills:** {}\n<:Skull:560844645991710740> **Deaths:** {}".format(userinfo["enemieskilled"], userinfo["TrapKills"], userinfo["deaths"]), inline=False)
				em.set_author(name="{}'s Statistics".format(userinfo["name"]), icon_url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			except:
					
				maxexp = 100 + ((userinfo["lvl"] + 1) * 3.5)
			if not userinfo["guild"] == "None":
				try:
					guildid = userinfo["guild"]
					userguild = self.bot.get_guild(guildid)
				except:
					userguild = guild
			else:
				userguild = guild

			if not userinfo["equip"] == "None":
				weaponequipped = userinfo["equip"]["name"]
				item = userinfo["equip"]["stats_min"]
				item2 = userinfo["equip"]["stats_max"]
			else:
				weaponequipped = "None"
				item = ""
				item2 = ""

			if not userinfo["wearing"] == "None":
				armorequipped = userinfo["wearing"]["name"]
				item3 = userinfo["wearing"]["stats_min"]
				item4 = userinfo["wearing"]["stats_max"]
			else:
				armorequipped = "None"
				item3 = ""
				item4 = ""

			

			
			try:
				icon = ""
				Class = userinfo["class"]
				if Class == "Mage":
					icon = "<:Mage:752633441626882058> "
				if Class == "Elementalist":
					icon = "<:Elementalist:752638205584474164> "
				if Class == "Necromancer":
					icon = "<:Necromancer:752638205832069191> "
				if Class == "Developed Necromancer":
					icon = "<:Necromancer:752638205832069191> "
				if Class == "Adequate Elementalist":
					icon = "<:Elementalist:752638205584474164> "
				if Class == "Paladin":
					icon = "<:Paladin:752638205869949168> "
				if Class == "Samurai":
					icon = "<:Samurai:752638205920018603> "
				if Class == "Knight":
					icon = "<:Knight:752633441362903120> "
				if Class == "Master Samurai":
					icon = "<:Samurai:752638205920018603> "
				if Class == "Grand Paladin":
					icon = "<:Paladin:752638205869949168> "
				if Class == "Thief":
					icon = "<:Thief:752633441811693638> "
				if Class == "Mesmer":
					icon = "<:Mesmer:752638205697851413> "
				if Class == "Rogue":
					icon = "<:Rogue:752638205928538252> "
				if Class == "High Rogue":
					icon = "<:Rogue:752638205928538252> "
				if Class == "Adept Mesmer":
					icon = "<:Mesmer:752638205697851413> "
				if Class == "Archer":
					icon = "<:Archer:752633441282949222> "
				if Class == "Ranger":
					icon = "<:Ranger:752638206285185116> "
				if Class == "Assassin":
					icon = "<:Assassin:639473417791209472> "
				if Class == "Night Assassin":
					icon = "<:Assassin:639473417791209472> "
				if Class == "Skilled Ranger":
					icon = "<:Ranger:752638206285185116> "
			except:
				pass

			
			try:
				Race = ""
				Race = userinfo["race"]
				if Race == "Elf":
					ricon = "<:Elf:639474564023189554> "
				if Race == "Human":
					ricon = "<:Human:639474561355874304> "
				if Race == "Orc":
					ricon = "<:Orc:639474558109483028> "
				if Race == "Demon":
					ricon = "<:Demon:639474562463170590> "
			except:
				pass

			em = discord.Embed(description="**Name:** {}\n{}**Race:** {}\n{}**Class:** {}\n:scroll: **Title:** {}\n<:Guild:560844076967002112> **Guild:** {}\n\n<:Magic:560844225839890459> **Level:** {}\n<:Experience:560809103346368522> **Exp:** {} / {}\n<:HealthHeart:560845406750375937> **Health:** {} / {}".format(userinfo["name"], ricon, userinfo["race"], icon, userinfo["class"], userinfo["title"], userguild.name, userinfo["lvl"], userinfo["exp"], maxexp, userinfo["health"], userinfo["MaxHealth"]), color=discord.Colour(0xffffff))
			em.add_field(name="Equipment", value=":crossed_swords: **Weapon:** {}\n:crossed_swords: **Weapon Damage:** {}-{}\n\n<:Shield:573576333863682064> **Armor:** {}\n<:Shield:573576333863682064> **Armor Defense:** {}-{}\n".format(weaponequipped, item, item2, armorequipped, item3, item4), inline=False)
			em.add_field(name="Tools", value="<:Axe:573574740220969007> **Axe level:** {}\n<:Pickaxe:573574740640530471> **Pickaxe level:** {}\n**Saw level:** {}\n**Chisel level:** {}\n**Hammer level:** {}".format(userinfo["axelvl"], userinfo["pickaxelvl"], userinfo["sawlvl"], userinfo["chisellvl"], userinfo["hammerlvl"]), inline=False)
			em.add_field(name="History", value="<:PvP:573580993055686657> **Kills:** {}\n:mouse_trap: **Trap Kills:** {}\n<:Skull:560844645991710740> **Deaths:** {}".format(userinfo["enemieskilled"], userinfo["TrapKills"], userinfo["deaths"]), inline=False)
			em.set_author(name="{}'s Statistics".format(userinfo["name"]), icon_url=user.avatar_url)
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return



		else:
			
			maxexp = 100 + ((userinfo["lvl"] + 1) * 3.5)
			if not userinfo["guild"] == "None":
				try:
					guildid = userinfo["guild"]
					userguild = self.bot.get_guild(guildid)
				except:
					userguild = guild
			else:
				userguild = guild

			if not userinfo["equip"] == "None":
				weaponequipped = userinfo["equip"]["name"]
				item = userinfo["equip"]["stats_min"]
				item2 = userinfo["equip"]["stats_max"]
			else:
				weaponequipped = "None"
				item = ""
				item2 = ""

			if not userinfo["wearing"] == "None":
				armorequipped = userinfo["wearing"]["name"]
				item3 = userinfo["wearing"]["stats_min"]
				item4 = userinfo["wearing"]["stats_max"]
			else:
				armorequipped = "None"
				item3 = ""
				item4 = ""

			

			
			try:
				icon = ""
				Class = userinfo["class"]
				if Class == "Mage":
					icon = "<:Mage:752633441626882058> "
				if Class == "Elementalist":
					icon = "<:Elementalist:752638205584474164> "
				if Class == "Necromancer":
					icon = "<:Necromancer:752638205832069191> "
				if Class == "Developed Necromancer":
					icon = "<:Necromancer:752638205832069191> "
				if Class == "Adequate Elementalist":
					icon = "<:Elementalist:752638205584474164> "
				if Class == "Paladin":
					icon = "<:Paladin:752638205869949168> "
				if Class == "Samurai":
					icon = "<:Samurai:752638205920018603> "
				if Class == "Knight":
					icon = "<:Knight:752633441362903120> "
				if Class == "Master Samurai":
					icon = "<:Samurai:752638205920018603> "
				if Class == "Grand Paladin":
					icon = "<:Paladin:752638205869949168> "
				if Class == "Thief":
					icon = "<:Thief:752633441811693638> "
				if Class == "Mesmer":
					icon = "<:Mesmer:752638205697851413> "
				if Class == "Rogue":
					icon = "<:Rogue:752638205928538252> "
				if Class == "High Rogue":
					icon = "<:Rogue:752638205928538252> "
				if Class == "Adept Mesmer":
					icon = "<:Mesmer:752638205697851413> "
				if Class == "Archer":
					icon = "<:Archer:752633441282949222> "
				if Class == "Ranger":
					icon = "<:Ranger:752638206285185116> "
				if Class == "Assassin":
					icon = "<:Assassin:639473417791209472> "
				if Class == "Night Assassin":
					icon = "<:Assassin:639473417791209472> "
				if Class == "Skilled Ranger":
					icon = "<:Ranger:752638206285185116> "
			except:
				pass

			
			try:
				Race = ""
				Race = userinfo["race"]
				if Race == "Elf":
					ricon = "<:Elf:639474564023189554> "
				if Race == "Human":
					ricon = "<:Human:639474561355874304> "
				if Race == "Orc":
					ricon = "<:Orc:639474558109483028> "
				if Race == "Demon":
					ricon = "<:Demon:639474562463170590> "
			except:
				pass

			em = discord.Embed(description="**Name:** {}\n{}**Race:** {}\n{}**Class:** {}\n:scroll: **Title:** {}\n<:Guild:560844076967002112> **Guild:** {}\n\n<:Magic:560844225839890459> **Level:** {}\n<:Experience:560809103346368522> **Exp:** {} / {}\n<:HealthHeart:560845406750375937> **Health:** {} / {}".format(userinfo["name"], ricon, userinfo["race"], icon, userinfo["class"], userinfo["title"], userguild.name, userinfo["lvl"], userinfo["exp"], maxexp, userinfo["health"], userinfo["MaxHealth"]), color=discord.Colour(0xffffff))
			em.add_field(name="Equipment", value=":crossed_swords: **Weapon:** {}\n:crossed_swords: **Weapon Damage:** {}-{}\n\n<:Shield:573576333863682064> **Armor:** {}\n<:Shield:573576333863682064> **Armor Defense:** {}-{}\n".format(weaponequipped, item, item2, armorequipped, item3, item4), inline=False)
			em.add_field(name="Tools", value="<:Axe:573574740220969007> **Axe level:** {}\n<:Pickaxe:573574740640530471> **Pickaxe level:** {}\n**Saw level:** {}\n**Chisel level:** {}\n**Hammer level:** {}".format(userinfo["axelvl"], userinfo["pickaxelvl"], userinfo["sawlvl"], userinfo["chisellvl"], userinfo["hammerlvl"]), inline=False)
			em.add_field(name="History", value="<:PvP:573580993055686657> **Kills:** {}\n:mouse_trap: **Trap Kills:** {}\n<:Skull:560844645991710740> **Deaths:** {}".format(userinfo["enemieskilled"], userinfo["TrapKills"], userinfo["deaths"]), inline=False)
			em.set_author(name="{}'s Statistics".format(userinfo["name"]), icon_url=user.avatar_url)
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	@commands.command(pass_context=True, aliases=["monsterstats", "statsmonsters", "killstats", "stats2"], no_pm=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def mstats(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has Checked their status")

		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		
		em = discord.Embed(color=discord.Colour(0xffffff))
		em.add_field(name="**Golden Temple.**", value="**Rachi:** {}\n**Debin:** {}\n**Oofer:** {}\n**Wyvern:** {}\n**Fire Golem:** {}".format(userinfo["Rachikilled"], userinfo["Debinkilled"], userinfo["Ooferkilled"], userinfo["Wyvernkilled"], userinfo["FireGolemkilled"]), inline=False)
		em.add_field(name="**Saker Keep**", value="**Draugr:** {}\n**Stalker:** {}\n**Souleater:** {}\n**The Corrupted:** {}".format(userinfo["Draugrkilled"], userinfo["Stalkerkilled"], userinfo["Souleaterkilled"], userinfo["TheCorruptedkilled"]), inline=False)
		em.add_field(name="**The Forest**", value="**Wolf:** {}\n**Goblin:** {}\n**Zombie:** {}\n**Phantasm:** {}".format(userinfo["Wolfkilled"], userinfo["Goblinkilled"], userinfo["Zombiekilled"], userinfo["Phantasmkilled"]), inline=False)
		em.add_field(name="**Ebony Mountains**", value="**Elder Dragon:** {}\n**Hades:** {}\n**Ebony Guardian:** {}\n**The Accursed:** {}".format(userinfo["ElderDragonkilled"], userinfo["Hadeskilled"], userinfo["EbonyGuardiankilled"], userinfo["TheAccursedkilled"]), inline=False)
		em.add_field(name="**Town of Arkina**", value="**Ettin:** {}\n**Dormammu:** {}\n**Harpy:** {}\n**The Nameless King:** {}".format(userinfo["Ettinkilled"], userinfo["Dormammukilled"], userinfo["Harpykilled"], userinfo["TheNamelessKingkilled"]), inline=False)
		em.add_field(name="**Zulanthu**", value="**Saurian:** {}\n**Deathclaw:** {}\n**Largos:** {}\n**The Venemous:** {}".format(userinfo["Sauriankilled"], userinfo["Deathclawkilled"], userinfo["Largoskilled"], userinfo["TheVenomouskilled"]), inline=False)
		em.add_field(name="**Lost City**", value="**Skeleton:** {}\n**Lizardmen:** {}\n**Giant:** {}\n**Death Knight:** {}".format(userinfo["Skeletonkilled"], userinfo["Lizardmenkilled"], userinfo["Giantkilled"], userinfo["DeathKnightkilled"]), inline=False)
		em.add_field(name="**Drenheim**", value="**Ice Wolves:** {}\n**Frost Goblin:** {}\n**Frost Orc:** {}\n**Frost Dragon:** {}".format(userinfo["IceWolveskilled"], userinfo["FrostGoblinkilled"], userinfo["FrostOrckilled"], userinfo["FrostDragonkilled"]), inline=False)
		
		em.set_author(name="{}'s Monster Kill Statistics".format(userinfo["name"]), icon_url=user.avatar_url)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

def setup(bot):
	c = status(bot)
	bot.add_cog(c)