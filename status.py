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
			em.add_field(name="History", value="<:PvP:573580993055686657> **Kills:** {}\n<:Skull:560844645991710740> **Deaths:** {}".format(userinfo["enemieskilled"], userinfo["deaths"]), inline=False)
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
			em.add_field(name="History", value="<:PvP:573580993055686657> **Kills:** {}\n<:Skull:560844645991710740> **Deaths:** {}".format(userinfo["enemieskilled"], userinfo["deaths"]), inline=False)
			em.set_author(name="{}'s Statistics".format(userinfo["name"]), icon_url=user.avatar_url)
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