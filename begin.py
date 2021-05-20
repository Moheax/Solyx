import asyncio
import datetime
import random
from random import choice as randchoice

import discord
from discord.ext import commands

from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import userdata

# - - - Begin / Start - - - WORKS

class begin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True, aliases=["start"])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def begin(self, ctx):
		languageinfo = db.servers.find_one({"_id": ctx.message.guild.id})
		language = languageinfo["language"]

		user = ctx.message.author
		
		userinfo = db.users.find_one({"_id": user.id})

		if not userinfo["class"] == "None" and not userinfo["race"] == "None":
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["rpg"]["restart"]["translation"].format(user.mention))
			answer1 = await self.check_answer(ctx, ["No", "no", "N", "n", "Yes", "yes", "Y", "y", "Nee", "Ja", "J", "-begin"])

			if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes" or answer1 == "ja" or answer1 == "Ja" or answer1 == "j":
				userinfo = userdata(user)
				db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
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

		db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

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


		answer2 = await self.check_answer(ctx, ["archer", "knight", "mage", "thief", "-archer", "-knight", "-mage", "-thief"])

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

		db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

		embed = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["setupdone"]["title"]["translation"], colour=0xffffff)
		embed.add_field(name="Quests", value=":notebook_with_decorative_cover: **You new Quest is *Basic A***\n Take a look at your stats\nType `{}stats`!".format(ctx.prefix), inline=False)
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

		try:
			creationchannel = self.bot.get_channel(818858244625793107)

			humans = db.users.count({"race": "Human"})
			demons = db.users.count({"race": "Demon"})
			elfs = db.users.count({"race": "Elf"})
			orcs = db.users.count({"race": "Orc"})

			total = humans + demons + elfs + orcs

			color = 0xffffff
			embed = discord.Embed(title="New user created.", colour=color)
			embed.add_field(name="Name:", value="{}\n{}".format(user.mention, userinfo["name"]), inline=False)
			embed.add_field(name="Class", value=userinfo["class"], inline=False)
			embed.add_field(name="Race", value=userinfo["race"], inline=False)
			embed.add_field(name="Account number", value=total, inline=False)
			try:
				
				await creationchannel.send(embed=embed)
			except Exception as e:
				print(e)
		
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except Exception as e:
					print(e)
					return
		except:
			pass
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator, "Has created a new charater")
        
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
	n = begin(bot)
	bot.add_cog(n)