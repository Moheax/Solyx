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




class fight(commands.Cog):
	def __init__(self, bot):
		self.bot = bot




# - - - Begin / Start - - - WORKS

	@commands.command(pass_context=True, no_pm=True, aliases=["start"])
	@commands.cooldown(1, 30, commands.BucketType.user)
	async def begin(self, ctx):
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		channel = ctx.message.channel
		user  = ctx.message.author
		
		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.message.guild
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if not userinfo["class"] == "None" and not userinfo["race"] == "None":
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["restart"]["translation"].format(user.mention))
			answer1 = await self.check_answer(ctx, ["No", "no", "N", "n", "Yes", "yes", "Y", "y", "Nee", "Ja", "J", "-begin"])

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "ja" or answer1 == "Ja" or answer1 == "j":
				userinfo = userdata(user)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["yesrestart"]["translation"].format(ctx.prefix))
				return
			elif answer1 == "n" or answer1 == "N" or answer1 == "no" or answer1 == "No" or answer1 == "nee" or answer1 == "Nee":
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["norestart"]["translation"])
				return
			else:
				return

		await asyncio.sleep(1)
		color = 0xffffff
		embed = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["raceselection"]["title"]["translation"], description=fileIO(f"data/languages/EN.json", "load")["rpg"]["raceselection"]["description"]["translation"], colour=color)
		embed.add_field(name="<:Demon:639474562463170590> Demon", value=fileIO(f"data/languages/EN.json", "load")["rpg"]["raceselection"]["demon"]["translation"], inline=False)
		embed.add_field(name="<:Elf:639474564023189554> Elf", value=fileIO(f"data/languages/EN.json", "load")["rpg"]["raceselection"]["elf"]["translation"], inline=False)
		embed.add_field(name="<:Human:639474561355874304> Human", value=fileIO(f"data/languages/EN.json", "load")["rpg"]["raceselection"]["human"]["translation"], inline=False)
		embed.add_field(name="<:Orc:639474558109483028> Orc", value=fileIO(f"data/languages/EN.json", "load")["rpg"]["raceselection"]["orc"]["translation"], inline=False)
		try:
			await ctx.send(embed=embed)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except Exception as e:
				print(e)
				return

		answer1 = await self.check_answer(ctx, ["orc", "human", "elf", "demon", "-orc", "-human", "-elf", "-demon"])

		if not answer1:
			return
		elif answer1.lower() in ["orc", "-orc"]:
			userinfo["race"] = "Orc"
		elif answer1.lower() in ["human", "-human"]:
			userinfo["race"] = "Human"
		elif answer1.lower() in ["elf", "-elf"]:
			userinfo["race"] = "Elf"
		elif answer1.lower() in ["demon", "-demon"]:
			userinfo["race"] = "Demon"
		else:
			return

		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		color = 0xffffff
		embed = discord.Embed(title="What class are you?", colour=color)
		embed.add_field(name="<:Archer:639473419703812122> Archer", value=fileIO(f"data/languages/EN.json", "load")["rpg"]["classselection"]["archer"]["translation"], inline=False)
		embed.add_field(name="<:Knight:639473415492861972> Knight", value=fileIO(f"data/languages/EN.json", "load")["rpg"]["classselection"]["knight"]["translation"], inline=False)
		embed.add_field(name="<:Mage:639473422040301574> Mage", value=fileIO(f"data/languages/EN.json", "load")["rpg"]["classselection"]["mage"]["translation"], inline=False)
		embed.add_field(name="<:Thief:639473408563740681> Thief", value=fileIO(f"data/languages/EN.json", "load")["rpg"]["classselection"]["thief"]["translation"], inline=False)
		try:
			await ctx.send(embed=embed)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except Exception as e:
				print(e)
				return


		answer2= await self.check_answer(ctx, ["archer", "knight", "mage", "thief", "-archer", "-knight", "-mage", "-thief"])

		if not answer2:
			return
		if answer2.lower() in ["archer", "-archer"]:
			userinfo["class"] = "Archer"
			userinfo["skills_learned"].append("Shoot")
			userinfo["equip"] = {"name": "Starter Bow", "type": "bow", "rarity": "Basic", "stats_min": 5, "stats_max": 12, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/JSHWiSK.png"}
		elif answer2.lower() in ["knight", "-knight"]:
			userinfo["class"] = "Knight"
			userinfo["skills_learned"].append("Swing")
			userinfo["equip"] = {"name": "Starter Sword", "type": "sword", "rarity": "Basic", "stats_min": 5, "stats_max": 12, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/oW8roUp.png"}
		elif answer2.lower() in ["mage", "-mage"]:
			userinfo["class"] = "Mage"
			userinfo["skills_learned"].append("Cast")
			userinfo["equip"] = {"name": "Starter Staff", "type": "staff", "rarity": "Basic", "stats_min": 5, "stats_max": 12, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/S7eGyqy.png"}
		elif answer2.lower() in ["thief", "-thief"]:
			userinfo["class"] = "Thief"
			userinfo["skills_learned"].append("Stab")
			userinfo["equip"] = {"name": "Starter Dagger", "type": "dagger", "rarity": "Basic", "stats_min": 5, "stats_max": 12, "refinement": "Normal", "description": "?!",  "image": "https://i.imgur.com/WGaqfei.png"}
		else:
			return

		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		embed = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["setupdone"]["title"]["translation"], colour=0xffffff)
		embed.set_footer(text=fileIO(f"data/languages/EN.json", "load")["rpg"]["setupdone"]["footer"]["translation"].format(ctx.prefix))
		try:
			await ctx.send(embed=embed)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["setupdone"]["footer"]["translation"].format(ctx.prefix))
				return
			except Exception as e:
				print(e)
				return


		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has created a new charater")


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


	async def _level_up_check_user(self, ctx, user):
		userinfo = db.users.find_one({ "_id": user.id })
		titlesinfo = db.titles.find_one({ "_id": user.id })
		if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
			userinfo["lvl"] = userinfo["lvl"] + 1
			userinfo["health"] = 100
			userinfo["exp"] = 0
			em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		if userinfo["lvl"] >= 10 and not "Beginner" in titlesinfo["titles_list"]:
			newtitle = "Beginner"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 20 and not "Amateur" in titlesinfo["titles_list"]:
			newtitle = "Amateur"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 30 and not "Novice" in titlesinfo["titles_list"]:
			newtitle = "Novice"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 40 and not "Apprentice" in titlesinfo["titles_list"]:
			newtitle = "Apprentice"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["lvl"] >= 50 and not "Respected" in titlesinfo["titles_list"]:
			newtitle = "Respected"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["lvl"] >= 75 and not "Renowned" in titlesinfo["titles_list"]:
			newtitle = "Renowned"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["lvl"] >= 100 and not "Professional" in titlesinfo["titles_list"]:
			newtitle = "Professional"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["lvl"] >= 125 and not "Master" in titlesinfo["titles_list"]:
			newtitle = "Master"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
		
		if userinfo["lvl"] >= 150 and not "Grand-Master" in titlesinfo["titles_list"]:
			newtitle = "Grand-Master"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
		
		if userinfo["lvl"] >= 200 and not "Enlightened" in titlesinfo["titles_list"]:
			newtitle = "Enlightened"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 250 and not "Mighty" in titlesinfo["titles_list"]:
			newtitle = "Mighty"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 300 and not "Empowered" in titlesinfo["titles_list"]:
			newtitle = "Empowered"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 350 and not "Golden" in titlesinfo["titles_list"]:
			newtitle = "Golden"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 400 and not "Radiant" in titlesinfo["titles_list"]:
			newtitle = "Radiant"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 450 and not "Arcane" in titlesinfo["titles_list"]:
			newtitle = "Arcane"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 500 and not "Iridescent" in titlesinfo["titles_list"]:
			newtitle = "Iridescent"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 600 and not "Luminescent" in titlesinfo["titles_list"]:
			newtitle = "Luminescent"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 700 and not "Celestial" in titlesinfo["titles_list"]:
			newtitle = "Celestial"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 800 and not "unbelievable" in titlesinfo["titles_list"]:
			newtitle = "unbelievable"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["lvl"] >= 900 and not "Unreal" in titlesinfo["titles_list"]:
			newtitle = "Unreal"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 1000 and not "Godlike" in titlesinfo["titles_list"]:
			newtitle = "Godlike"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
			
		if userinfo["Rachikilled"] >= 100  and not "Rachi Killer" in titlesinfo["titles_list"]:
			newtitle = "Rachi Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["Draugrkilled"] >= 100  and not "Draugr Killer" in titlesinfo["titles_list"]:
			newtitle = "Draugr Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["Debinkilled"] >= 100  and not "Debin Killer" in titlesinfo["titles_list"]:
			newtitle = "Debin Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["Stalkerkilled"] >= 100  and not "Stalker Killer" in titlesinfo["titles_list"]:
			newtitle = "Stalker Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["FireGolemkilled"] >= 100  and not "Fire Golem Killer" in titlesinfo["titles_list"]:
			newtitle = "Fire Golem Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["Wyvernkilled"] >= 100  and not "Wyvern Killer" in titlesinfo["titles_list"]:
			newtitle = "Wyvern Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["Ooferkilled"] >= 100  and not "Oofer Killer" in titlesinfo["titles_list"]:
			newtitle = "Oofer Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["Souleaterkilled"] >= 100  and not "Souleater Killer" in titlesinfo["titles_list"]:
			newtitle = "Souleater Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["Wolfkilled"] >= 100  and not "Wolf Killer" in titlesinfo["titles_list"]:
			newtitle = "Wolf Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["Goblinkilled"] >= 100  and not "Goblin Killer" in titlesinfo["titles_list"]:
			newtitle = "Goblin Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["Zombiekilled"] >= 100  and not "Zombie Killer" in titlesinfo["titles_list"]:
			newtitle = "Zombie Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["Phantasmkilled"] >= 100  and not "Phantasm Killer" in titlesinfo["titles_list"]:
			newtitle = "Phantasm Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["TheCorruptedkilled"] >= 100  and not "The Corrupted Killer" in titlesinfo["titles_list"]:
			newtitle = "The Corrupted Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["TheAccursedkilled"] >= 100  and not "The Accursed Killer" in titlesinfo["titles_list"]:
			newtitle = "The Accursed Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["ElderDragonkilled"] >= 100  and not "Elder Dragon Killer" in titlesinfo["titles_list"]:
			newtitle = "Elder Dragon Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
								
		if userinfo["Hadeskilled"] >= 100  and not "Hades Killer" in titlesinfo["titles_list"]:
			newtitle = "Hades Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)			
		if userinfo["EbonyGuardiankilled"] >= 100  and not "Ebony Killer" in titlesinfo["titles_list"]:
			newtitle = "Ebony Guardian Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)			
		if userinfo["Harpykilled"] >= 100  and not "Harpy Killer" in titlesinfo["titles_list"]:
			newtitle = "Harpy Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)			
		if userinfo["Dormammukilled"] >= 100  and not "Dormammu Killer" in titlesinfo["titles_list"]:
			newtitle = "Dormammu Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)			
		if userinfo["Ettinkilled"] >= 100  and not "Ettin Killer" in titlesinfo["titles_list"]:
			newtitle = "Ettin Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)			
		if userinfo["TheNamelessKingkilled"] >= 100  and not "The Nameless King Killer" in titlesinfo["titles_list"]:
			newtitle = "The Nameless King Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)			
		if userinfo["Largoskilled"] >= 100  and not "Largos Killer" in titlesinfo["titles_list"]:
			newtitle = "Largos Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)			
			
		if userinfo["Deathclawkilled"] >= 100  and not "Deathclaw Killer" in titlesinfo["titles_list"]:
			newtitle = "Deathclaw Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["Sauriankilled"] >= 100  and not "Saurian Killer" in titlesinfo["titles_list"]:
			newtitle = "Saurian Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
					
		if userinfo["TheVenomouskilled"] >= 100  and not "The Venomous Killer" in titlesinfo["titles_list"]:
			newtitle = "The Venomous Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["Skeletonkilled"] >= 100  and not "Skeleton Killer" in titlesinfo["titles_list"]:
			newtitle = "Skeleton Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["Lizardmenkilled"] >= 100  and not "Lizardmen Killer" in titlesinfo["titles_list"]:
			newtitle = "Lizardmen Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["Giantkilled"] >= 100  and not "Giant Killer" in titlesinfo["titles_list"]:
			newtitle = "Giant Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["DeathKnightkilled"] >= 100  and not "Death Knight Killer" in titlesinfo["titles_list"]:
			newtitle = "Death Knight Killer"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["deaths"] >= 15  and not "Uncoordinated" in titlesinfo["titles_list"]:
			newtitle = "Uncoordinated"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)	
					
		if userinfo["deaths"] >= 30  and not "Unhandy" in titlesinfo["titles_list"]:
			newtitle = "Unhandy"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
							
		if userinfo["deaths"] >= 60  and not "Clumsy" in titlesinfo["titles_list"]:
			newtitle = "Clumsy"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
							
		if userinfo["deaths"] >= 90  and not "Unskillful" in titlesinfo["titles_list"]:
			newtitle = "Unskillful"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
							
		if userinfo["deaths"] >= 120  and not "Inexpert" in titlesinfo["titles_list"]:
			newtitle = "Inexpert"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["deaths"] >= 999  and not "I'm playing the game wrong..." in titlesinfo["titles_list"]:
			newtitle = "I'm playing the game wrong..."
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)



		if userinfo["gold"] == 0 and not "Broke" in titlesinfo["titles_list"]:
			newtitle = "Broke"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["gold"] >= 500 and not "Poor" in titlesinfo["titles_list"]:
			newtitle = "Poor"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["gold"] >= 10000 and not "Rich" in titlesinfo["titles_list"]:
			newtitle = "Rich"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["gold"] >= 100000 and not "Wealthy" in titlesinfo["titles_list"]:
			newtitle = "Wealthy"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["gold"] >= 1000000 and not "Millionaire" in titlesinfo["titles_list"]:
			newtitle = "Millionaire"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)

		if userinfo["lvl"] >= 30:
			if userinfo["class"] == "Thief":
				options = ["Rogue", "rogue", "Mesmer", "mesmer"]
				em = discord.Embed(title=":military_medal: Specialization!", description="Please choose a specialization:", color=discord.Colour(0xffffff))
				em.add_field(name="<:Mesmer:639473407401918485> Mesmer", value="Master of confusion and movement", inline=False)
				em.add_field(name="<:Rogue:639473412221304842> Rogue", value="Quick and brutal attacks", inline=False)
				await ctx.send(embed=em)
				answer = await self.check_answer(ctx, options)
				if answer == "Rogue" or answer == "rogue":
					spechoice = "Rogue"
					userinfo["class"] = spechoice
					userinfo["skills_learned"].append("Parry")
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))
				elif answer == "Mesmer" or answer == "mesmer":
					spechoice = "Mesmer"
					userinfo["class"] = spechoice
					userinfo["skills_learned"].append("Distort")
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))
			elif userinfo["class"] == "Mage":
				options = ["Necromancer", "necromancer", "Elementalist", "elementalist"]
				em = discord.Embed(title=":military_medal: Specialization!", description="Please choose a specialization:", color=discord.Colour(0xffffff))
				em.add_field(name="<:Elementalist:639473417376235551> Elementalist", value="Controll all the elements", inline=False)
				em.add_field(name="<:Necromancer:639473415295860767> Necromancer", value="Wield the power of the dead", inline=False)
				await ctx.send(embed=em)
				answer = await self.check_answer(ctx, options)
				if answer == "Necromancer" or answer == "necromancer":
					spechoice = "Necromancer"
					userinfo["class"] = spechoice
					userinfo["skills_learned"].append("Reap")
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))
				elif answer == "Elementalist" or answer == "elementalist":
					spechoice = "Elementalist"
					userinfo["class"] = spechoice
					userinfo["skills_learned"].append("Overload")
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))
			elif userinfo["class"] == "Knight":
				options = ["Samurai", "samurai", "Paladin", "paladin"]
				em = discord.Embed(title=":military_medal: Specialization!", description="Please choose a specialization:", color=discord.Colour(0xffffff))
				em.add_field(name="<:Paladin:639473415257980938> Paladin", value="Brutal attacks", inline=False)
				em.add_field(name="<:Samurai:639473412028497940> Samurai", value="Defensive playstile", inline=False)
				await ctx.send(embed=em)
				answer = await self.check_answer(ctx, options)
				if answer == "Paladin" or answer == "paladin":
					spechoice = "Paladin"
					userinfo["class"] = spechoice
					userinfo["skills_learned"].append("Fusillade")
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))
				elif answer == "Samurai" or answer == "samurai":
					spechoice = "Samurai"
					userinfo["class"] = spechoice
					userinfo["skills_learned"].append("Protrude")
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))
			elif userinfo["class"] == "Archer":
				options = ["Assassin", "assassin", "Ranger", "ranger"]
				em = discord.Embed(title=":military_medal: Specialization!", description="Please choose a specialization:", color=discord.Colour(0xffffff))
				em.add_field(name="<:Assassin:639473417791209472> Assassin", value="High damage but low health", inline=False)
				em.add_field(name="<:Ranger:639473419930304513> Ranger", value="Always sure to hit for a decent amount of damage", inline=False)
				await ctx.send(embed=em)
				answer = await self.check_answer(ctx, options)
				if answer == "Ranger" or answer == "ranger":
					spechoice = "Ranger"
					userinfo["class"] = spechoice
					userinfo["skills_learned"].append("Strike")
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))
				elif answer == "Assassin" or answer == "assassin":
					spechoice = "Assassin"
					userinfo["class"] = spechoice
					userinfo["skills_learned"].append("Corrupt")
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))

		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

	# handles battle creation.
	async def _create_battle(self, user):
		exists = db.battles.find_one({ "_id": user.id })
		if not exists:
			data = battledata(user)
			db.battles.insert_one(data)

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def fight(self, ctx):
		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]

		user = ctx.author
		userinfo = db.users.find_one({ "_id": user.id })
		titlesinfo = db.titles.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo["health"] <= 0:
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["fight"]["nohp"]["translation"])
			return
		guild = ctx.guild
		guildinfo = db.servers.find_one({ "_id": guild.id })

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Started a fight")
				
		now = datetime.datetime.now()


		#IF PLAYER ISNT FIGHTING AN ENEMY, CHOOSE ONE BASED ON LOCATION
		if userinfo["selected_enemy"] == "None":
			if userinfo["location"] == "Golden Temple":
				debi = randchoice(["Rachi", "Debin", "Oofer", "Fire Golem", "Wyvern"])
			elif userinfo["location"] == "The Forest":
				debi = randchoice(["Wolf", "Goblin", "Zombie", "Phantasm"])
			elif userinfo["location"] == "Saker Keep":
				debi = randchoice(["Draugr", "Stalker", "Souleater", "The Corrupted"])
			elif userinfo["location"] == "Ebony Mountains":
				debi = randchoice(["The Accursed", "Elder Dragon", "Hades", "Ebony Guardian"])
			elif userinfo["location"] == "Township of Arkina":
				debi = randchoice(["The Nameless King", "Harpy", "Dormammu", "Ettin"])
			elif userinfo["location"] == "Zulanthu":
				debi = randchoice(["Largos", "Deathclaw", "Saurian", "The Venomous"])
			elif userinfo["location"] == "Lost City":
				debi = randchoice(["Skeleton", "Lizardmen", "Giant", "Death Knight"])
			enemyname = debi
			if debi == "Fire Golem" or debi == "Phantasm" or debi == "The Corrupted" or debi == "The Accursed" or debi == "The Nameless King" or debi == "The Venomous" or debi == "Death Knight":
				enemyname = ":trident: " + debi
			em = discord.Embed(title=fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["title"]["translation"].format(userinfo["location"], enemyname), description=fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["description"]["translation"], color=discord.Colour(0xffffff))
			if debi == "Phantasm":
				em.set_image(url="https://i.imgur.com/BbBmEOF.jpg")
			elif debi == "Fire Golem":
				em.set_image(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/c7f23f41-5bd8-4b82-a00c-d61b0cfb0160/d9p8w3t-e2e0278a-7b05-4d6b-9a69-c50f3f005126.png/v1/fill/w_700,h_331,q_70,strp/fire_golem_by_sourshade_d9p8w3t-350t.jpg")
			elif debi == "The Corrupted":
				em.set_image(url="https://i.imgur.com/oTi3K3q.jpg")
			elif debi == "Death Knight":
				em.set_image(url="https://i.imgur.com/ELd7Ll5.jpg")
			em.set_footer(text="yes / no")
			await ctx.send(embed=em)
			options = ["y", "Y", "yes", "Yes", "n", "N", "No", "no", "-fight"]
			answer1 = await self.check_answer(ctx, options)

			if answer1 == "y" or answer1 == "Y" or answer1 == "Yes" or answer1 == "yes":
				userinfo["selected_enemy"] = debi
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				if userinfo["selected_enemy"] in ["Rachi", "Draugr"]:
					userinfo["enemyhp"] = random.randint(10, 30)
				elif userinfo["selected_enemy"] in ["Debin", "Stalker"]:
					userinfo["enemyhp"] = random.randint(20, 40)
				elif userinfo["selected_enemy"] in ["Fire Golem", "Wyvern"]:
					userinfo["enemyhp"] = random.randint(30, 50)
				elif userinfo["selected_enemy"] in ["Oofer", "Souleater"]:
					userinfo["enemyhp"] = random.randint(40, 60)
				elif userinfo["selected_enemy"] in ["Wolf", "Goblin"]:
					userinfo["enemyhp"] = random.randint(50, 70)
				elif userinfo["selected_enemy"] in ["Zombie", "Phantasm"]:
					userinfo["enemyhp"] = random.randint(60, 80)
				elif userinfo["selected_enemy"] in ["The Corrupted", "The Accursed", "Elder Dragon"]:
					userinfo["enemyhp"] = random.randint(70, 90)
				elif userinfo["selected_enemy"] in ["Hades", "Ebony Guardian", "Harpy"]:
					userinfo["enemyhp"] = random.randint(80, 100)
				elif userinfo["selected_enemy"] in ["Dormammu", "Ettin", "Skeleton"]: 
					userinfo["enemyhp"] = random.randint(90, 110)
				elif userinfo["selected_enemy"] in ["The Nameless King", "Largos", "Deathclaw", "Lizardmen"]: 
					userinfo["enemyhp"] = random.randint(100, 120)
				elif userinfo["selected_enemy"] in ["Saurian", "The Venomous","Giant", "Death Knight"]: 
					userinfo["enemyhp"] = random.randint(110, 130)

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			elif answer1 == "n" or answer1 == "N" or answer1 == "no" or answer1 == "No":
				funanswer = randchoice([fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["run"]["run1"]["translation"], fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["run"]["run2"]["translation"], fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["run"]["run3"]["translation"], fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["run"]["run4"]["translation"], fileIO(f"data/languages/{language}.json", "load")["fight"]["wander"]["run"]["run5"]["translation"]])
				await ctx.send(funanswer)
				return

			else:
				return
		#YOUR DAMAGE BASED ON THE WEAPON YOURE HOLDING
# - - Starting weapons - -
		mindmg = userinfo["equip"]["stats_min"]
		maxdmg = userinfo["equip"]["stats_max"]
		youdmg = random.randint(mindmg, maxdmg)



		#YOUR PROTECTION IS BASED ON THE ARMOR YOURE HOLDING
		youdef = 0

		if userinfo["class"] == "Paladin":
			youdef += random.randint(5, 10)
		elif userinfo["class"] == "Knight":
			youdef += random.randint(8, 15)

# - - Common Armor - -
		if userinfo["wearing"] == "Chainmail Armor":
			youdef += random.randint(2, 12)
		elif userinfo["wearing"] == "Barbaric Armor":
			youdef += random.randint(5, 7)
		elif userinfo["wearing"] == "Pit fighter Armor":
			youdef += random.randint(4, 9)
		elif userinfo["wearing"] == "Banded Armor":
			youdef += random.randint(1, 10)
		elif userinfo["wearing"] == "Leather Armor":
			youdef += random.randint(3, 8)
# - - Rare Armor - -
		elif userinfo["wearing"] == "Iron Armor":
			youdef += random.randint(14, 16)
		elif userinfo["wearing"] == "Branded Metal Armor":
			youdef += random.randint(13, 17)
		elif userinfo["wearing"] == "Wolf Fur":
			youdef += random.randint(1, 24)
		elif userinfo["wearing"] == "Enchanted Steel Armor":
			youdef += random.randint(12, 17)
# - - Legendary Armor - -
		elif userinfo["wearing"] == "Bane Of The Goblin Lord":
			youdef += random.randint(20, 25)
		elif userinfo["wearing"] == "Nightstalker Mantle":
			youdef += random.randint(15, 28)
		elif userinfo["wearing"] == "Hephaestus Armor":
			youdef += random.randint(16, 27)

		#ENEMY DAMAGE BASED ON ENEMY GROUPS
		enemydmg = 0
		enemygold = random.randint(30, 60)
		xpgain = random.randint(10, 15)

		#GUILD BOOST


		#try:
		#	guild = ctx.guild
		#	guildinfo = db.servers.find_one({ "_id": guild.id })
		#	guildbonus = guildinfo["bonus"]

		#	if guildbonus >= 200:
		#		effectiveguildbonus == 200
		#	else:
		#		effectiveguildbonus == guildbonus
		#except:
		#	effectiveguildbonus = 0


		guild = ctx.guild
		guildinfo = db.servers.find_one({ "_id": guild.id })
		effectiveguildbonus = guildinfo["bonus"]

		if effectiveguildbonus >= 200:
			effectiveguildbonus == 200

		if userinfo["selected_enemy"] == "Rachi":
			enemydmg += random.randint(2, 10)
			enemygold = random.randint(10, 15) + (effectiveguildbonus)
			goldlost = random.randint(20, 60)
			xpgain = random.randint(5, 10)
		if userinfo["selected_enemy"] == "Draugr":
			enemydmg += random.randint(2, 10)
			enemygold = random.randint(10, 15) + (effectiveguildbonus)
			goldlost = random.randint(20, 60)
			xpgain = random.randint(5, 10)
		elif userinfo["selected_enemy"] == "Debin" or userinfo["selected_enemy"] == "Stalker":
			enemydmg += random.randint(5, 10)
			enemygold = random.randint(12, 17) + (effectiveguildbonus)
			goldlost = random.randint(30, 70)
			xpgain = random.randint(5, 20)
		elif userinfo["selected_enemy"] == "Oofer" or userinfo["selected_enemy"] == "Souleater" or userinfo["selected_enemy"] == "Wyvern":
			enemydmg += random.randint(5, 15)
			enemygold = random.randint(14, 19) + (effectiveguildbonus)
			goldlost = random.randint(40, 80)
			xpgain = random.randint(10, 25)
		elif userinfo["selected_enemy"] == "Wolf" or userinfo["selected_enemy"] == "Phantasm":
			enemydmg += random.randint(10, 15)
			enemygold = random.randint(16, 21) + (effectiveguildbonus)
			goldlost = random.randint(90, 160)
			xpgain = random.randint(10, 30)
		elif userinfo["selected_enemy"] == "Goblin" or userinfo["selected_enemy"] == "Fire Golem":
			enemydmg += random.randint(10, 20)
			enemygold = random.randint(18, 21) + (effectiveguildbonus)
			goldlost = random.randint(90, 160)
			xpgain = random.randint(10, 30)
		elif userinfo["selected_enemy"] == "Zombie":
			enemydmg += random.randint(15, 20)
			enemygold = random.randint(20, 23) + (effectiveguildbonus)
			goldlost = random.randint(90, 160)
			xpgain = random.randint(10, 30)
		elif userinfo["selected_enemy"] == "The Corrupted":
			enemydmg += random.randint(15, 30)
			enemygold = random.randint(22, 25) + (effectiveguildbonus)
			goldlost = random.randint(100, 180)
			xpgain = random.randint(10, 35)
		elif userinfo["selected_enemy"] == "Ebony Guardian" or userinfo["selected_enemy"] == "Elder Dragon" or userinfo["selected_enemy"] == "Hades" or userinfo["selected_enemy"] == "Skeleton":
			enemydmg += random.randint(20, 30)
			enemygold = random.randint(24, 27) + (effectiveguildbonus)
			goldlost = random.randint(100, 190)
			xpgain = random.randint(15, 35)
		elif userinfo["selected_enemy"] == "The Accursed" or userinfo["selected_enemy"] == "Harpy" or userinfo["selected_enemy"] == "Ettin" or userinfo["selected_enemy"] == "Dormammu":
			enemydmg += random.randint(20, 40)
			enemygold = random.randint(26, 29) + (effectiveguildbonus)
			goldlost = random.randint(150, 200)
			xpgain = random.randint(15, 35)
		elif userinfo["selected_enemy"] == "The Nameless King" or userinfo["selected_enemy"] == "Deathclaw" or userinfo["selected_enemy"] == "Saurian" or userinfo["selected_enemy"] == "Lizardmen":
			enemydmg += random.randint(25, 40)
			enemygold = random.randint(28, 31) + (effectiveguildbonus)
			goldlost = random.randint(160, 220)
			xpgain = random.randint(20, 40)
		elif userinfo["selected_enemy"] == "Largos" or userinfo["selected_enemy"] == "The Venomous"  or userinfo["selected_enemy"] == "Giant":
			enemydmg += random.randint(25, 50)
			enemygold = random.randint(30, 33) + (effectiveguildbonus)
			goldlost = random.randint(170, 240)
			xpgain = random.randint(25, 45)
		elif userinfo["selected_enemy"] == "Death Knight":
			enemydmg += random.randint(30, 55)
			enemygold = random.randint(35, 37) + (effectiveguildbonus)
			goldlost = random.randint(200, 260)
			xpgain = random.randint(30, 45)
		elif userinfo["selected_enemy"] == "None":
			return 

		
			#YOUR SKILL OPTIONS LIST
		skill_list = [i for i in userinfo["skills_learned"]]
		show_list = []
		options = []

		all_skills = [
			"Swing", "Stab", "Shoot",
			"Cast", "Parry", "Distort",
			"Reap", "Overload", "Fusillade",
			"Protrude", "Strike", "Corrupt",
		]

		for skill in all_skills:
			if skill in skill_list:
				options.append(skill)
				options.append(skill.lower())
				show_list.append(skill)

		options.append("Heal")
		options.append("heal")
		show_list.append("Heal")

		#IF FOR WHATEVER REASON THE USER DOES -fight AGAIN, RETURN
		em = discord.Embed(title=fileIO(f"data/languages/{language}.json", "load")["fight"]["skill"]["title"]["translation"], description="\n".join(show_list), color=discord.Colour(0xffffff))
		em.set_author(name=fileIO(f"data/languages/{language}.json", "load")["fight"]["skill"]["author"]["translation"], icon_url=ctx.message.author.avatar_url)
		skillmsg = await ctx.send(embed=em)
		answer2 = await self.check_answer(ctx, options)

		#DEFINE WHAT SKILL WE SELECTED
#Done
		if answer2 == "cast" or answer2 == "Cast":
			move = "Cast"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0	
			userhealth = userhealth - enemydmg
			enemyhp = userinfo["enemyhp"] - youdmg
			lootbag = random.randint(1, 15)
			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			"""
			em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em1.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em1)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em2.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em2)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
			await asyncio.sleep(0.4)
			"""

			em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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

#Done
		elif answer2 == "shoot" or answer2 == "Shoot":
			move = "Shoot"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0	
			userhealth = userhealth - enemydmg
			enemyhp = userinfo["enemyhp"] - youdmg
			lootbag = random.randint(1, 15)
			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100
			
			"""
			em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em1.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em1)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em2.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em2)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
			await asyncio.sleep(0.4)
			"""

			em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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

#Done
		elif answer2 == "swing" or answer2 == "Swing":
			move = "Swing"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0
			userhealth = userhealth - enemydmg
			enemyhp = userinfo["enemyhp"] - youdmg
			lootbag = random.randint(1, 15)
			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			"""
			em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em1.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em1)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em2.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em2)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
			await asyncio.sleep(0.4)
			"""

			em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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

#Done
		elif answer2 == "stab" or answer2 == "Stab":
			move = "Stab"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0	
			userhealth = userhealth - enemydmg
			enemyhp = userinfo["enemyhp"] - youdmg
			lootbag = random.randint(1, 15)
			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			"""
			em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em1.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em1)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em2.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em2)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
			await asyncio.sleep(0.4)
			"""

			em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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

#Done
		elif answer2 == "parry" or answer2 == "Parry":
			move = "Parry"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0	
			enemyhp = userinfo["enemyhp"] - youdmg
			lootbag = random.randint(1, 15)
			
			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			parrychance = random.randint(1, 100)
			
			if parrychance >= 70:
				hpgain = int((youdmg / 100) * 25)
				userhealth += hpgain
				youdmg -= int((youdmg / 100) * 20)
				enemyhp = userinfo["enemyhp"] - youdmg
				userhealth = userhealth - enemydmg

				if userhealth < 0:
					userhealth = 0
				if enemyhp < 0:
					enemyhp = 0	

				"""
				em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em1.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em1)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em2.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em2)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage and regains {} HP**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, hpgain), color=discord.Colour(0xffffff))
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
				await asyncio.sleep(0.4)
				"""

				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage and regains {} HP**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, hpgain, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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
				enemydmg = int((enemydmg / 100) * 150)
				youdmg -= int((youdmg / 100) * 20)
				enemyhp = userinfo["enemyhp"] - youdmg
				userhealth = userhealth - enemydmg


				if userhealth < 0:
					userhealth = 0
				if enemyhp < 0:
					enemyhp = 0
	
				"""
				em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em1.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em1)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				
				em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em2.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em2)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
				await asyncio.sleep(0.4)
				"""

				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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

#Done
		elif answer2 == "distort" or answer2 == "Distort":
			move = "Distort"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0
			enemyhp = userinfo["enemyhp"] - youdmg
			lootbag = random.randint(1, 15)
			distortchance = random.randint(1, 100)
			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			if distortchance >= 80:
				userhealth = userhealth
				enemyhp = userinfo["enemyhp"] - youdmg
			
				if userhealth < 0:
					userhealth = 0
				if enemyhp < 0:
					enemyhp = 0
				"""
				em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em1.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em1)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and nulls {}'s attack**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em2.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em2)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and nulls {}'s attack**\n**{} hits {} for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], userinfo["name"], userinfo["selected_enemy"], youdmg), color=discord.Colour(0xffffff))
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
				await asyncio.sleep(0.4)
				"""

				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses {} and nulls {}'s attack**\n**{} hits {} for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], move, userinfo["selected_enemy"], userinfo["name"], userinfo["selected_enemy"], youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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
				enemydmg += int((enemydmg / 100) * 35)
				userhealth = userhealth - enemydmg
				enemyhp = userinfo["enemyhp"] - youdmg

				if userhealth < 0:
					userhealth = 0
				if enemyhp < 0:
					enemyhp = 0
				"""
				em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em1.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em1)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em2.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em2)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
				await asyncio.sleep(0.4)
				"""

				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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


#Done
		elif answer2 == "reap" or answer2 == "Reap":
			move = "Reap"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			enemyhp = userinfo["enemyhp"]
			if enemydmg < 0:
				enemydmg = 0
			lootbag = random.randint(1, 15)
			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			reapchance = random.randint(1, 100)

			if reapchance >= 85:
				absorb = enemydmg
				userhealth += absorb
				if userhealth >= 100:
					userhealth = 100
				enemydmg = 0
				enemyhp = userinfo["enemyhp"]
				if userhealth < 0:
					userhealth = 0
				if enemyhp < 0:
					enemyhp = 0

				"""
				em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em1.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em1)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses reap and absorbs {}'s damage.**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em2.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em2)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)
				"""

				em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} uses reap and absorbs {}'s damage \n{} Hp healed!**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["name"], userinfo["selected_enemy"], absorb, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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
				userhealth = userhealth - enemydmg
				youdmg -= int((youdmg / 100) * 20)
				enemyhp = userinfo["enemyhp"] - youdmg
				if userhealth < 0:
					userhealth = 0
				if enemyhp < 0:
					enemyhp = 0
				"""

				em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em1.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em1)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em2.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em2)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return
				await asyncio.sleep(0.4)

				em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
				await asyncio.sleep(0.4)
				"""

				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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

#Done
		elif answer2 == "overload" or answer2 == "Overload":
			move = "Overload"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0
			
			
			lootbag = random.randint(1, 15)
			overloaddmg = random.randint(15, 25)
			overloadselfdmg = random.randint(5, 10)
			youdmg += overloaddmg
			enemydmg += overloadselfdmg
			userhealth = userhealth - enemydmg - overloadselfdmg 
			enemyhp = userinfo["enemyhp"] - youdmg

			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			"""
			em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em1.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em1)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em2.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em2)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} overloads {} for {} damage but also deals {} self damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, overloadselfdmg), color=discord.Colour(0xffffff))
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
			await asyncio.sleep(0.4)
			"""


			em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} overloads {} for {} damage but also deals {} self damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], userinfo["selected_enemy"], youdmg, overloadselfdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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

#done
		elif answer2 == "fusillade" or answer2 == "Fusillade":
			move = "Fusillade"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0
			lootbag = random.randint(1, 15)
			critchance = random.randint(1, 100)
			if critchance <= 75:
				youdmg += int((youdmg / 100) * 30)
			else:
				enemydmg += int((enemydmg / 100) * 25)
			userhealth = userhealth - enemydmg
			enemyhp = userinfo["enemyhp"] - youdmg
			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			"""
			em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em1.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em1)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em2.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em2)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
			await asyncio.sleep(0.4)
			"""
			if critchance <= 75:
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and has a Critical hit! for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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
				em5 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em5.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em5)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

#done
		elif answer2 == "protrude" or answer2 == "Protrude":
			move = "Protrude"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0
			lootbag = random.randint(1, 15)
			youdmg -= int((youdmg / 100) * 75)
			misschance = random.randint(1, 10)
			if misschance >= 5:
				enemydmg = 0
			userhealth = userhealth - enemydmg
			enemyhp = userinfo["enemyhp"] - youdmg
			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			"""
			em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em1.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em1)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em2.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em2)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
			await asyncio.sleep(0.4)
			"""
			if misschance >= 5:
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} Misses and hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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
				em5 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em5.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em5)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

#done
		elif answer2 == "strike" or answer2 == "Strike":
			move = "Strike"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0
			lootbag = random.randint(1, 15)
			extradmgchance = random.randint(1, 100)
			randomdamage = random.randint(5, 15)
			if extradmgchance >= 50:
				youdmg += randomdamage
			else:
				youdmg -= randomdamage
			userhealth = userhealth - enemydmg
			enemyhp = userinfo["enemyhp"] - youdmg
			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			"""
			em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em1.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em1)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em2.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em2)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
			await asyncio.sleep(0.4)
			"""

			em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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

#Not done yet
		elif answer2 == "corrupt" or answer2 == "Corrupt":
			move = "Corrupt"
			userhealth = userinfo["health"]
			enemydmg -= youdef
			if enemydmg < 0:
				enemydmg = 0
			lootbag = random.randint(1, 15)
			corruptchance = random.randint(1, 100)
			if corruptchance >= 70:
				corruptdmg =  int((100 - userhealth) / 3)
			userhealth = userhealth - enemydmg
			enemyhp = userinfo["enemyhp"] - youdmg - corruptdmg

			if enemydmg < 0:
				enemydmg = 0
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100

			"""
			em1 = discord.Embed(description="{} has {} HP\n{} has {} HP".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"]), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em1.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em1)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em2 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg), color=discord.Colour(0xffffff))
			if not userinfo["equip"]["image"] == "None":
				em2.set_thumbnail(url=userinfo["equip"]["image"])
			try:
				await skillmsg.edit(embed=em2)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
					return
				except:
					return
			await asyncio.sleep(0.4)

			em3 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg), color=discord.Colour(0xffffff))
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
			await asyncio.sleep(0.4)

			"""
			if corruptchance >= 70:
				em4 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage\nDeals a extra {} corrupt damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, corruptdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
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
				em5 = discord.Embed(description="{} has {} HP\n{} has {} HP\n\n**{} hits {} for {} damage**\n**{} uses {} and hits for {} damage**\n\n{} has {} HP left\n{} has {} HP left".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Colour(0xffffff))
				if not userinfo["equip"]["image"] == "None":
					em5.set_thumbnail(url=userinfo["equip"]["image"])
				try:
					await skillmsg.edit(embed=em5)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
						return
					except:
						return

		elif answer2 == "heal" or answer2 == "Heal":
			battleinfo = db.battles.find_one({ "_id": user.id })
			if battleinfo["battle_active"] == "True":
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["heal"]["inbattle"]["translation"])
				return
			else:
				await self._heal_reaction(ctx, user, skillmsg)
				return

		else:
			return

		await asyncio.sleep(0.4)

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
			userinfo["health"] = 0
			userinfo["selected_enemy"] = "None"
			userinfo["enemieskilled"] = userinfo["enemieskilled"] + 1
			userinfo["deaths"] = userinfo["deaths"] + 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		elif userhealth <= 0:
			em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["playerdied"]["translation"].format(userinfo["selected_enemy"], userinfo["name"], userinfo["name"], goldlost), color=discord.Colour(0xff0000))
			await ctx.send(embed=em)
			userinfo["gold"] = userinfo["gold"] - goldlost
			if userinfo["gold"] < 0:
				userinfo["gold"] = 0
			if userinfo["health"] < 0:
				userinfo["health"] = 0
			userinfo["selected_enemy"] = "None"
			userinfo["deaths"] = userinfo["deaths"] + 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		elif enemyhp <= 0:
			em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["enemydied"]["translation"].format(userinfo["name"], userinfo["selected_enemy"], userinfo["name"], int(enemygold), userinfo["name"], xpgain), color=discord.Colour(0x00ff00))
			await ctx.send(embed=em)

			if userinfo["selected_enemy"] == "Oofer":
				try:
					mission = "Kill 400 Oofers"
					await self._guild_mission_check(user, guild, mission, 1)
				except:
					
					pass
			if userinfo["selected_enemy"] == "Goblin":
				try:
					mission = "Kill 100 Goblins"
					await self._guild_mission_check(user, guild, mission, 1)
				except:
					print("Error while trying to check '" + mission + "' mission for " + user.name + " (" + user.id + ")")
					pass


			if userinfo["selected_enemy"] == "Rachi":
				try:
					userinfo["Rachikilled"] = userinfo["Rachikilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass
					
			if userinfo["selected_enemy"] == "Draugr":
				try:
					userinfo["Draugrkilled"] = userinfo["Draugrkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass
			if userinfo["selected_enemy"] == "Debin":
				try:
					userinfo["Debinkilled"] = userinfo["Debinkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Stalker":
				try:
					userinfo["Stalkerkilled"] = userinfo["Stalkerkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Fire Golem":
				try:
					userinfo["FireGolemkilled"] = userinfo["FireGolemkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Wyvern":
				try:
					userinfo["Wyvernkilled"] = userinfo["Wyvernkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Oofer":
				try:
					userinfo["Ooferkilled"] = userinfo["Ooferkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Souleater":
				try:
					userinfo["Souleaterkilled"] = userinfo["Souleaterkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Wolf":
				try:
					userinfo["Wolfkilled"] = userinfo["Wolfkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Goblin":
				try:
					userinfo["Goblinkilled"] = userinfo["Goblinkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Zombie":
				try:
					userinfo["Zombiekilled"] = userinfo["Zombiekilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Phantasm":
				try:
					userinfo["Phantasmkilled"] = userinfo["Phantasmkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "The Corrupted":
				try:
					userinfo["TheCorruptedkilled"] = userinfo["TheCorruptedkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "The Accursed":
				try:
					userinfo["TheAccursedkilled"] = userinfo["TheAccursedkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Elder Dragon":
				try:
					userinfo["ElderDragonkilled"] = userinfo["ElderDragonkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Hades":
				try:
					userinfo["Hadeskilled"] = userinfo["Hadeskilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Ebony Guardian":
				try:
					userinfo["EbonyGuardiankilled"] = userinfo["EbonyGuardiankilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Harpy":
				try:
					userinfo["Harpykilled"] = userinfo["Harpykilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Dormammu":
				try:
					userinfo["Dormammukilled"] = userinfo["Dormammukilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Ettin":
				try:
					userinfo["Ettinkilled"] = userinfo["Ettinkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "The Nameless King":
				try:
					userinfo["TheNamelessKingkilled"] = userinfo["TheNamelessKingkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Largos":
				try:
					userinfo["Largoskilled"] = userinfo["Largoskilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Death Claw":
				try:
					userinfo["Deathclawilled"] = userinfo["Deathclawilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Saurian":
				try:
					userinfo["Sauriankilled"] = userinfo["Sauriankilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "The venemous":
				try:
					userinfo["TheVenomouskilled"] = userinfo["TheVenomouskilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Skeleton":
				try:
					userinfo["Skeletonkilled"] = userinfo["Skeletonkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Lizardmen":
				try:
					userinfo["Lizardmenkilled"] = userinfo["Lizardmenkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Giant":
				try:
					userinfo["Giantkilled"] = userinfo["Giantkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass

			if userinfo["selected_enemy"] == "Death Knight":
				try:
					userinfo["DeathKnightkilled"] = userinfo["DeathKnightkilled"] + 1
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				except:
					pass


			userinfo["selected_enemy"] = "None"
			userinfo["gold"] = userinfo["gold"] + int(enemygold)
			userinfo["exp"] = userinfo["exp"] + xpgain
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

			if lootbag == 2:
				userinfo = db.users.find_one({ "_id": user.id })
				em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["crate"]["translation"].format(userinfo["name"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				userinfo["lootbag"] = userinfo["lootbag"] + 1
			if lootbag == 1:
				userinfo = db.users.find_one({ "_id": user.id })
				em = discord.Embed(description=fileIO(f"data/languages/{language}.json", "load")["fight"]["key"]["translation"].format(userinfo["name"]), color=discord.Colour(0xffffff))
				await ctx.send(embed=em)
				userinfo["keys"] = userinfo["keys"] + 1

			userinfo["enemieskilled"] = userinfo["enemieskilled"] + 1
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		await self._level_up_check_user(ctx, user)

	@commands.group()
	@commands.guild_only()
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def battle(self, ctx):
		server = ctx.guild
		channel = ctx.channel
		servercolor = ctx.author.color

		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=servercolor)
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
		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]

		author = ctx.author

		# INVITER
		authorinfo = db.users.find_one({ "_id": author.id })

		# USER
		userinfo = db.users.find_one({ "_id": user.id })

		# CHECK IF USERS EXIST
		if authorinfo["race"] == "None" or authorinfo["class"] == "None":
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		# CHECK IF USERS HAVE ENOUGH HP
		if authorinfo["health"] <= 0:
			await ctx.send("<:Solyx:560809141766193152> **| You cannot fight with 0 HP!**")
			return

		if userinfo["health"] <= 0:
			await ctx.send("<:Solyx:560809141766193152> **| {} does not have enough HP.**".format(user.name))
			return

		# CHECK IF USERS HAVE BATTLE INFO
		await self._create_battle(author)
		await self._create_battle(user)
		authorbattleinfo = db.battles.find_one({ "_id": author.id })
		userbattleinfo = db.battles.find_one({ "_id": user.id })

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
		#em.set_thumbnail(url=RankSwordsPLZ)
		await ctx.send(embed=em)
		answer1 = await self.check_answer_other_user(ctx, user, ["yes", "no", "n", "y", "Y", "Yes", "N", "No"])
		if answer1 in ["y", "yes", "Y", "Yes"]:
			userbattleinfo["battle_enemy"] = author.id
			userbattleinfo["battle_turn"] = "True"
			userbattleinfo["battle_active"] = "True"
			userbattleinfo["lastmove"] = round(time())
			db.battles.replace_one({ "_id": user.id }, userbattleinfo, upsert=True)

			authorbattleinfo["battle_enemy"] = user.id
			authorbattleinfo["battle_turn"] = "False"
			authorbattleinfo["battle_active"] = "True"
			authorbattleinfo["lastmove"] = round(time())
			db.battles.replace_one({ "_id": author.id }, authorbattleinfo, upsert=True)

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
		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]

		user = ctx.author
		userinfo = db.users.find_one({ "_id": user.id })
		battleinfo = db.battles.find_one({ "_id": user.id })
		enemyid = battleinfo["battle_enemy"]
		enemyinfo = db.users.find_one({ "_id": enemyid })
		enemybattleinfo = db.battles.find_one({ "_id": enemyid })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
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
				db.battles.replace_one({ "_id": user.id }, battleinfo)

				enemybattleinfo["battle_active"] = "False"
				enemybattleinfo["battle_enemy"] = "None"
				enemybattleinfo["battle_turn"] = "False"
				db.battles.replace_one({ "_id": enemyid }, enemybattleinfo)
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

		#YOUR PROTECTION IS BASED ON THE ARMOR YOURE HOLDING
		youdef = 0

		if userinfo["class"] == "Paladin":
			youdef += random.randint(5, 10)
		elif userinfo["class"] == "Knight":
			youdef += random.randint(8, 15)

# - - Common Armor - -
		if userinfo["wearing"] == "Chainmail Armor":
			youdef += random.randint(2, 12)
		elif userinfo["wearing"] == "Barbaric Armor":
			youdef += random.randint(5, 7)
		elif userinfo["wearing"] == "Pit fighter Armor":
			youdef += random.randint(4, 9)
		elif userinfo["wearing"] == "Banded Armor":
			youdef += random.randint(1, 10)
		elif userinfo["wearing"] == "Leather Armor":
			youdef += random.randint(3, 8)
# - - Rare Armor - -
		elif userinfo["wearing"] == "Iron Armor":
			youdef += random.randint(14, 16)
		elif userinfo["wearing"] == "Branded Metal Armor":
			youdef += random.randint(13, 17)
		elif userinfo["wearing"] == "Wolf Fur":
			youdef += random.randint(1, 24)
		elif userinfo["wearing"] == "Enchanted Steel Armor":
			youdef += random.randint(12, 17)
# - - Legendary Armor - -
		elif userinfo["wearing"] == "Bane Of The Goblin Lord":
			youdef += random.randint(20, 25)
		elif userinfo["wearing"] == "Nightstalker Mantle":
			youdef += random.randint(15, 28)
		elif userinfo["wearing"] == "Hephaestus Armor":
			youdef += random.randint(19, 26)

# - - - - - - - - - - - - - - - ENEMY STATS CHECKS - - - - - - - - - - - - - - -
		mindmg = enemyinfo["equip"]["stats_min"]
		maxdmg = enemyinfo["equip"]["stats_max"]
		enemydmg = random.randint(mindmg, maxdmg)

		#YOUR PROTECTION IS BASED ON THE ARMOR YOURE HOLDING
		enemydef = 0

		if enemyinfo["class"] == "Paladin":
			enemydef += random.randint(5, 10)
		elif enemyinfo["class"] == "Knight":
			enemydef += random.randint(8, 15)

# - - Common Armor - -
		if enemyinfo["wearing"] == "Chainmail Armor":
			enemydef += random.randint(2, 12)
		elif enemyinfo["wearing"] == "Barbaric Armor":
			enemydef += random.randint(5, 7)
		elif enemyinfo["wearing"] == "Pit fighter Armor":
			enemydef += random.randint(4, 9)
		elif enemyinfo["wearing"] == "Banded Armor":
			enemydef += random.randint(1, 10)
		elif enemyinfo["wearing"] == "Leather Armor":
			enemydef += random.randint(3, 8)
# - - Rare Armor - -
		elif enemyinfo["wearing"] == "Iron Armor":
			enemydef += random.randint(14, 16)
		elif enemyinfo["wearing"] == "Branded Metal Armor":
			enemydef += random.randint(13, 17)
		elif enemyinfo["wearing"] == "Wolf Fur":
			enemydef += random.randint(1, 24)
		elif enemyinfo["wearing"] == "Enchanted Steel Armor":
			enemydef += random.randint(12, 17)
# - - Legendary Armor - -
		elif enemyinfo["wearing"] == "Bane Of The Goblin Lord":
			enemydef += random.randint(20, 25)
		elif enemyinfo["wearing"] == "Nightstalker Mantle":
			enemydef += random.randint(15, 28)
		elif enemyinfo["wearing"] == "Hephaestus Armor":
			enemydef += random.randint(16, 27)

		enemygold = random.randint(30, 60) # CHECK THIS - unused
		xpgain = random.randint(10, 15) # CHECK THIS - unused

		#GUILD BOOST
		try:
			guild = ctx.guild
			guildinfo = db.servers.find_one({ "_id": guild.id })
			guildbonus = guildinfo["bonus"] # CHECK THIS - unused
		except:
			guildbonus = 0

			#YOUR SKILL OPTIONS LIST
		skill_list = [i for i in userinfo["skills_learned"]]
		show_list = []
		options = []

		all_skills = [
			"Swing", "Stab", "Shoot",
			"Cast", "Parry", "Distort",
			"Reap", "Overload", "Fusillade",
			"Protrude", "Strike", "Corrupt",
		]

		for skill in all_skills:
			if skill in skill_list:
				options.append(skill)
				options.append(skill.lower())
				show_list.append(skill)

		#IF FOR WHATEVER REASON THE USER DOES -fight AGAIN, RETURN
		em = discord.Embed(title=fileIO(f"data/languages/{language}.json", "load")["fight"]["skill"]["title"]["translation"], description="\n".join(show_list), color=discord.Colour(0xffffff))
		em.set_author(name=fileIO(f"data/languages/{language}.json", "load")["fight"]["skill"]["author"]["translation"], icon_url=ctx.message.author.avatar_url)
		skillmsg = await ctx.send(embed=em)
		answer2 = await self.check_answer(ctx, options)

		#DEFINE WHAT SKILL WE SELECTED
		if answer2 == "cast" or answer2 == "Cast":
			move = "Cast"
		elif answer2 == "shoot" or answer2 == "Shoot":
			move = "Shoot"
		elif answer2 == "swing" or answer2 == "Swing":
			move = "Swing"
		elif answer2 == "stab" or answer2 == "Stab":
			move = "Stab"
		elif answer2 == "parry" or answer2 == "Parry":
			move = "Parry"
		elif answer2 == "distort" or answer2 == "Distort":
			move = "Distort"
		elif answer2 == "reap" or answer2 == "Reap":
			move = "Reap"
		elif answer2 == "overload" or answer2 == "Overload":
			move = "Overload"
		elif answer2 == "fusillade" or answer2 == "Fusillade":
			move = "Fusillade"
		elif answer2 == "protrude" or answer2 == "Protrude":
			move = "Protrude"
		elif answer2 == "strike" or answer2 == "Strike":
			move = "Strike"
		elif answer2 == "corrupt" or answer2 == "Corrupt":
			move = "Corrupt"
		else:
			return

		#LETS DEFINE OUR VAR'S
		userhealth = userinfo["health"]
		enemydmg -= youdef
		if enemydmg < 0:
			enemydmg = 1
		userhealth -= enemydmg

		#LETS DEFINE THE ENEMY'S VAR'S
		enemyhp = enemyinfo["health"]
		youdmg -= enemydef
		if youdmg < 0:
			youdmg = 1
		enemyhp -= youdmg

		#IF SELECTED A SKILL, FIGHT
		if answer2:
			if userhealth < 0:
				userhealth = 0
			if enemyhp < 0:
				enemyhp = 0
			if userhealth >= 100:
				userhealth = 100
			em = discord.Embed(description="<@{}> has {} HP\n{} has {} HP\n\n<@{}> hits {} for {} damage\n{} uses {} and hits for {} damage\n\n<@{}> has {} HP left\n{} has {} Hp left".format(battleinfo["battle_enemy"], enemyinfo["health"], user.mention, userinfo["health"], battleinfo["battle_enemy"], user.mention, enemydmg, user.mention, move, youdmg, battleinfo["battle_enemy"], enemyhp, user.mention, userhealth), color=discord.Colour(0xffffff))
			await skillmsg.edit(embed=em)
			userinfo["health"] = userhealth
			enemyinfo["health"] = enemyhp

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

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				db.battles.replace_one({ "_id": user.id }, battleinfo, upsert=True)
				db.users.replace_one({ "_id": enemyid }, enemyinfo, upsert=True)
				db.battles.replace_one({ "_id": enemyid }, enemybattleinfo, upsert=True)

			elif userhealth <= 0:
				em = discord.Embed(description=":crown: <@{}> **won!** :crown:\n:sparkles: +{} Exp".format(battleinfo["battle_enemy"], xpgain), color=discord.Colour(0xffdf00))
				await ctx.send(embed=em)

				battleinfo["battle_active"] = "False"
				battleinfo["battle_enemy"] = "None"
				battleinfo["battle_streak"] = 0
				battleinfo["battle_losses"] = battleinfo["battle_losses"] + 1

				enemybattleinfo["battle_active"] = "False"
				enemybattleinfo["battle_enemy"] = "None"
				enemybattleinfo["battle_streak"] = enemybattleinfo["battle_streak"] + 1
				enemybattleinfo["battle_wins"] = enemybattleinfo["battle_wins"] + 1
				enemybattleinfo["exp"] = userinfo["exp"] + xpgain

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				db.battles.replace_one({ "_id": user.id }, battleinfo, upsert=True)
				db.users.replace_one({ "_id": enemyid }, enemyinfo, upsert=True)
				db.battles.replace_one({ "_id": enemyid }, enemybattleinfo, upsert=True)

			elif enemyhp <= 0:
				em = discord.Embed(description=":crown: {} **won!** :crown:\n:sparkles: +{} Exp".format(user.mention, xpgain), color=discord.Colour(0xffdf00))
				await asyncio.sleep(1)
				await ctx.send(embed=em)

				battleinfo["battle_active"] = "False"
				battleinfo["battle_enemy"] = "None"
				battleinfo["battle_streak"] = battleinfo["battle_streak"] + 1
				battleinfo["battle_wins"] = battleinfo["battle_wins"] + 1
				battleinfo["exp"] = userinfo["exp"] + xpgain

				enemybattleinfo["battle_active"] = "False"
				enemybattleinfo["battle_enemy"] = "None"
				enemybattleinfo["battle_streak"] = 0
				enemybattleinfo["battle_losses"] = enemybattleinfo["battle_losses"] + 1

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				db.battles.replace_one({ "_id": user.id }, battleinfo, upsert=True)
				db.users.replace_one({ "_id": enemyid }, enemyinfo, upsert=True)
				db.battles.replace_one({ "_id": enemyid }, enemybattleinfo, upsert=True)

			else:
				try:
					await ctx.send(content="<:Solyx:560809141766193152> | It's your turn to fight, <@{}>!".format(enemyid))
				except:
					pass

			timestamp = round(time())
			enemybattleinfo["battle_turn"] = "True"
			enemybattleinfo["lastmove"] = timestamp
			battleinfo["battle_turn"] = "False"
			battleinfo["lastmove"] = timestamp

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			db.users.replace_one({ "_id": enemyid }, enemyinfo, upsert=True)
			db.battles.replace_one({ "_id": user.id }, battleinfo, upsert=True)
			db.battles.replace_one({ "_id": enemyid }, enemybattleinfo, upsert=True)

			await self._level_up_check_user(ctx, user)

		else:
			return

	async def _heal_reaction(self, ctx, user, msg):
		userinfo = db.users.find_one({ "_id": user.id })
		if userinfo["health"] == 100:
			em = discord.Embed(description="<:HealingPotion:573577125064605706> You already have 100 HP!", color=discord.Colour(0xffffff))
			await msg.edit(embed=em)
			return
		if userinfo["hp_potions"] > 0:
			gain = random.randint(25, 55)
			userinfo["health"] = userinfo["health"] + gain
			if userinfo["health"] > 100:
				userinfo["health"] = 100
			userinfo["hp_potions"] = userinfo["hp_potions"] - 1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
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

	async def _guild_mission_check(self, user, guild, mission, add):
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })

		if guild == "None":
			return

		if mission == "Kill 400 Oofers":
			if not guildinfo["mission"] == "Kill 400 Oofers":
				return
			try:
				guildinfo["missionprogress"] = guildinfo["missionprogress"] + add
				db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
				return
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				return

		elif mission == "Kill 100 Goblins":
			if not guildinfo["mission"] == "Kill 100 Goblins":
				return
			try:
				guildinfo["missionprogress"] = guildinfo["missionprogress"] + add
				db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
				return
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				return

		else:
			print(user.name + " (" + user.id + ") from guild with leader id " + guild.id + "managed to check a non-existing mission!")
			return



# - - - Commands menu - - - NEEDS REWRITE

	async def commands_menu(self, ctx, user):
		embed = discord.Embed(description="Click [here](http://solyx.xyz) for a detailed documentation.", color=discord.Colour(0xffffff))
		embed.set_author(name="Solyx Commands:", icon_url=ctx.message.author.avatar_url)
		embed.add_field(name="🇦 Getting Started", value="The basics", inline=False)
		embed.add_field(name="🇧 Fighting", value="All basic fighting related commands", inline=False)
		embed.add_field(name="🇨 Inventory & Items", value="Items, weapons, equip, ...", inline=False)
		embed.add_field(name="🇩 Economy", value="Buying, selling, gold, ...", inline=False)
		embed.add_field(name="🇪 guilds", value="guild related commands", inline=False)
		embed.add_field(name="🇫 Battles", value="1v1 battles commands", inline=False)
		embed.add_field(name="🇬 Raids", value="Coming soon", inline=False)
		embed.add_field(name="🇭 Admin Commands", value="guild administration commands", inline=False)
		embed.add_field(name="🇮 Miscellaneous Commands", value="Miscellaneous commands", inline=False)
		embed.set_footer(text="Click the reactions to navigate through the commands menu!")
		try:
			msg = await ctx.send(ctx.message.author, embed=embed)
		except:
			try:
				msg = await ctx.send(ctx.message.channel, embed=embed)
			except discord.HTTPException:
				await ctx.send(ctx.message.channel, "I cound't send the message.")
				return
		try:
			await self.bot.add_reaction(msg, "🇦")
			await self.bot.add_reaction(msg, "🇧")
			await self.bot.add_reaction(msg, "🇨")
			await self.bot.add_reaction(msg, "🇩")
			await self.bot.add_reaction(msg, "🇪")
			await self.bot.add_reaction(msg, "🇫")
			await self.bot.add_reaction(msg, "🇬")
			await self.bot.add_reaction(msg, "🇭")
			await self.bot.add_reaction(msg, "🇮")
			await self.bot.add_reaction(msg, "⬅")
			await self.bot.add_reaction(msg, "❌")
		except:
			pass
		await self.commands_menu_check(ctx, msg, user)
		return

	async def commands_menu_check(self, ctx, msg, user):
		while True:
			
			response = await self.bot.wait_for_reaction(emoji=["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "⬅", "❌"], user=user, message=msg, timeout=20)
			await asyncio.sleep(0.1)

			if not response:
				try:
					await self.bot.clear_reactions(msg)
				except:
					pass
				return

			if response.reaction.emoji == '❌':
				try:
					await self.bot.delete_message(msg)
					return
				except:
					return

			elif response.reaction.emoji == '⬅':
				try:
					await self.bot.remove_reaction(msg, "⬅", user)
				except:
					pass
				embed = discord.Embed(description="Click [here](http://solyx.xyz) for a detailed documentation.", color=discord.Colour(0xffffff))
				embed.set_author(name="Solyx Commands:", icon_url=ctx.message.author.avatar_url)
				embed.add_field(name="🇦 Getting Started", value="The basics", inline=False)
				embed.add_field(name="🇧 Fighting", value="All basic fighting related commands", inline=False)
				embed.add_field(name="🇨 Inventory & Items", value="Items, weapons, equip, ...", inline=False)
				embed.add_field(name="🇩 Economy", value="Buying, selling, gold, ...", inline=False)
				embed.add_field(name="🇪 guilds", value="guild related commands", inline=False)
				embed.add_field(name="🇫 Battles", value="1v1 battles commands", inline=False)
				embed.add_field(name="🇬 Raids", value="Coming soon", inline=False)
				embed.add_field(name="🇭 Admin Commands", value="guild administration commands", inline=False)
				embed.add_field(name="🇮 Miscellaneous Commands", value="Miscellaneous commands", inline=False)
				embed.set_footer(text="Click the reactions to navigate through the commands menu!")
				msg = await self.bot.edit_message(msg, embed=embed)
				await self.commands_menu_check(ctx, msg, user)
				return

			elif response.reaction.emoji == "🇦":
				try:
					await self.bot.remove_reaction(msg, "🇦", user)
				except:
					pass
				e = discord.Embed(color=discord.Colour(0xffffff))
				e.set_author(name="Getting Started", icon_url=ctx.message.author.avatar_url)
				e.add_field(name="{}tutorial".format(ctx.prefix), value="Learn how to use the bot", inline=True)
				e.add_field(name="{}begin".format(ctx.prefix), value="Create a character to start your adventure!", inline=True)
				msg = await self.bot.edit_message(msg, embed=e)
				await self.commands_menu_check(ctx, msg, user)
				return

			elif response.reaction.emoji == "🇧":
				try:
					await self.bot.remove_reaction(msg, "🇧", user)
				except:
					pass
				e = discord.Embed(color=discord.Colour(0xffffff))
				e.set_author(name="Fighting", icon_url=ctx.message.author.avatar_url)
				e.add_field(name="{}fight".format(ctx.prefix), value="Fight a monster", inline=True)
				e.add_field(name="{}hp".format(ctx.prefix), value="Check your health", inline=True)
				e.add_field(name="{}heal".format(ctx.prefix), value="Use a healing potion to gain HP", inline=False)
				e.add_field(name="{}travel".format(ctx.prefix), value="Go to a new location to fight different monsters", inline=False)
				msg = await self.bot.edit_message(msg, embed=e)
				await self.commands_menu_check(ctx, msg, user)
				return

			elif response.reaction.emoji == "🇨":
				try:
					await self.bot.remove_reaction(msg, "🇨", user)
				except:
					pass
				e = discord.Embed(color=discord.Colour(0xffffff))
				e.set_author(name="Inventory & Items", icon_url=ctx.message.author.avatar_url)
				e.add_field(name="{}inv".format(ctx.prefix), value="Check your inventory", inline=True)
				e.add_field(name="{}stats".format(ctx.prefix), value="See your statistics", inline=True)
				e.add_field(name="{}profile".format(ctx.prefix), value="Show your profile card", inline=False)
				e.add_field(name="{}rank".format(ctx.prefix), value="Show your rank card", inline=False)
				e.add_field(name="{}market".format(ctx.prefix), value="Sell abd buy items on the market", inline=False)
				e.add_field(name="{}equip".format(ctx.prefix), value="Equip a weapon or a piece of armor", inline=False)
				e.add_field(name="{}sell".format(ctx.prefix), value="Sell an item", inline=False)
				e.add_field(name="{}crate".format(ctx.prefix), value="Open a crate", inline=False)
				e.add_field(name="{}mine".format(ctx.prefix), value="Mine for stone and metal", inline=False)
				e.add_field(name="{}chop".format(ctx.prefix), value="Chop for wood", inline=False)
				e.add_field(name="{}fish".format(ctx.prefix), value="Fishing command", inline=False)
				msg = await self.bot.edit_message(msg, embed=e)
				await self.commands_menu_check(ctx, msg, user)
				return

			elif response.reaction.emoji == "🇩":
				try:
					await self.bot.remove_reaction(msg, "🇩", user)
				except:
					pass
				e = discord.Embed(color=discord.Colour(0xffffff))
				e.set_author(name="Economy", icon_url=ctx.message.author.avatar_url)
				e.add_field(name="{}inv".format(ctx.prefix), value="Check your inventory", inline=True)
				e.add_field(name="{}sell".format(ctx.prefix), value="Sell an item", inline=True)
				e.add_field(name="{}market".format(ctx.prefix), value="Check the market or buy/sell items", inline=False)
				e.add_field(name="{}hp buy".format(ctx.prefix), value="Buy a healing potion", inline=False)
				e.add_field(name="{}daily".format(ctx.prefix), value="Earn daily credits", inline=False)
				e.add_field(name="{}vote".format(ctx.prefix), value="Vote for the bot and get a big reward", inline=False)
				msg = await self.bot.edit_message(msg, embed=e)
				await self.commands_menu_check(ctx, msg, user)
				return

			elif response.reaction.emoji == "🇪":
				try:
					await self.bot.remove_reaction(msg, "🇪", user)
				except:
					pass
				e = discord.Embed(color=discord.Colour(0xffffff))
				e.set_author(name="guilds", icon_url=ctx.message.author.avatar_url)
				e.add_field(name="{}guild".format(ctx.prefix), value="Check all guild commands", inline=True)
				e.add_field(name="{}leaderboard".format(ctx.prefix), value="Open the players/guilds leaderboard", inline=True)
				msg = await self.bot.edit_message(msg, embed=e)
				await self.commands_menu_check(ctx, msg, user)
				return

			elif response.reaction.emoji == "🇫":
				try:
					await self.bot.remove_reaction(msg, "🇫", user)
				except:
					pass
				e = discord.Embed(color=discord.Colour(0xffffff))
				e.set_author(name="Battles", icon_url=ctx.message.author.avatar_url)
				e.add_field(name="{}battle".format(ctx.prefix), value="Check all battle commands", inline=True)
				e.add_field(name="{}heal".format(ctx.prefix), value="Gain HP by consuming a health potion", inline=True)
				e.add_field(name="{}equip".format(ctx.prefix), value="Equip a weapon or a piece of armor", inline=False)
				msg = await self.bot.edit_message(msg, embed=e)
				await self.commands_menu_check(ctx, msg, user)
				return

			elif response.reaction.emoji == "🇬":
				try:
					await self.bot.remove_reaction(msg, "🇬", user)
				except:
					pass
				e = discord.Embed(color=discord.Colour(0xffffff))
				e.set_author(name="Raids", icon_url=ctx.message.author.avatar_url)
				e.add_field(name="Soon...", value="This is still in development", inline=True)
				msg = await self.bot.edit_message(msg, embed=e)
				await self.commands_menu_check(ctx, msg, user)
				return

			elif response.reaction.emoji == "🇭":
				try:
					await self.bot.remove_reaction(msg, "🇭", user)
				except:
					pass
				e = discord.Embed(color=discord.Colour(0xffffff))
				e.set_author(name="Admin Commands", icon_url=ctx.message.author.avatar_url)
				e.add_field(name="{}help".format(ctx.prefix), value="Shows a menu with useful links or get more information about a command", inline=True)
				e.add_field(name="{}commands".format(ctx.prefix), value="Shows this menu", inline=True)
				e.add_field(name="{}prefix".format(ctx.prefix), value="Set a new prefix for Solyx", inline=False)
				e.add_field(name="{}ignore".format(ctx.prefix), value="Set channels the bot has to ignore", inline=False)
				msg = await self.bot.edit_message(msg, embed=e)
				await self.commands_menu_check(ctx, msg, user)
				return

			elif response.reaction.emoji == "🇮":
				try:
					await self.bot.remove_reaction(msg, "🇮", user)
				except:
					pass
				e = discord.Embed(color=discord.Colour(0xffffff))
				e.set_author(name="Miscellaneous Commands", icon_url=ctx.message.author.avatar_url)
				e.add_field(name="{}vote".format(ctx.prefix), value="Vote for the bot and get a sweet reward", inline=True)
				e.add_field(name="{}help".format(ctx.prefix), value="Shows this menu", inline=False)
				e.add_field(name="{}commands".format(ctx.prefix), value="Shows this menu", inline=True)
				e.add_field(name="{}invite".format(ctx.prefix), value="Invite Solyx to your guild", inline=True)
				e.add_field(name="{}info".format(ctx.prefix), value="See some information about Solyx, and it's status", inline=True)
				e.add_field(name="{}guild".format(ctx.prefix), value="Get an invite to the Solyx guild", inline=True)
				e.add_field(name="{}support".format(ctx.prefix), value="A list of all ways to get help with Solyx", inline=True)
				e.add_field(name="{}botstatus".format(ctx.prefix), value="Get a link to the Solyx status page", inline=True)
				e.add_field(name="{}website".format(ctx.prefix), value="Get a link to the Solyx website", inline=True)
				msg = await self.bot.edit_message(msg, embed=e)
				await self.commands_menu_check(ctx, msg, user)
				return


def setup(bot):
	n = fight(bot)
	bot.add_cog(n)