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



class travel(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		# - - - Location / Travel - - - #

	@commands.command (pass_context=True, no_pm=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def travel(self, ctx):


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has Traveled")

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.message.guild
		guildinfo = db.guilds.find_one({ "_id": guild.id })

		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		options = []
		options2 = []

		if userinfo["lvl"] >= 0: 
			options.append("(1) Golden Temple")
			options2.append("1")

		if userinfo["lvl"] >= 10:
			options.append("(2) Saker Keep")
			options2.append("2")
	
		if userinfo["lvl"] >= 20:
			options.append("(3) The Forest")
			options2.append("3")

		if userinfo["lvl"] >= 40:
			options.append("(4) Ebony Mountains")
			options2.append("4")

		if userinfo["lvl"] >= 60:
			options.append("(5) Township of Arkina")
			options2.append("5")

		if userinfo["lvl"] >= 90:
			options.append("(6) Zulanthu")
			options2.append("6")

		if userinfo["lvl"] >= 120:
			options.append("(7) Lost City")
			options2.append("7")

		if userinfo["lvl"] >= 150:
			options.append("(8) Drenheim ")
			options2.append("8")

		if userinfo["lvl"] >= 200:
			options.append("(9) Havelow [Coming soon]")
			options2.append("9")

		if userinfo["lvl"] >= 250:
			options.append("(10) Sacred Cave [Coming soon]")
			options2.append("10")

		if userinfo["lvl"] >= 300:
			options.append("(11) The Haunted Tomb [Coming soon]")
			options2.append("11")

		em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["title"]["translation"], description="{}".format("\n ".join(options)), color=discord.Colour(0xffffff))
		em.set_author(name=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["author"]["translation"], icon_url=user.avatar_url)
		em.set_footer(text=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["footer"]["translation"])
		try:
			await ctx.send(content="{}".format(user.mention), embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return
		
		answer1 = await self.check_answer(ctx, options2)

		if answer1 == "1":
			if userinfo["location"] == "Golden Temple":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "Golden Temple"
				userinfo["location"] = "Golden Temple"

		elif answer1 == "2":


			if userinfo["location"] == "Saker Keep":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "Saker Keep"
				userinfo["location"] = "Saker Keep"

		elif answer1 == "3":
			if userinfo["location"] == "The Forest":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "The Forest"
				userinfo["location"] = "The Forest"

		elif answer1 == "4":
			if userinfo["location"] == "Ebony Mountains":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "Ebony Mountains"
				userinfo["location"] = "Ebony Mountains"

		elif answer1 == "5":
			if userinfo["location"] == "Township of Arkina":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "Township of Arkina"
				userinfo["location"] = "Township of Arkina"

		elif answer1 == "6":
			if userinfo["location"] == "Zulanthu":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "Zulanthu"
				userinfo["location"] = "Zulanthu"

		elif answer1 == "7":
			if userinfo["location"] == "Lost City":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "Lost City"
				userinfo["location"] = "Lost City"

		elif answer1 == "8":
			if userinfo["location"] == "Drenheim":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "Drenheim"
				userinfo["location"] = "Drenheim"

		elif answer1 == "9":
			return
			if userinfo["location"] == "Havelow":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "Havelow"
				userinfo["location"] = "Havelow"


		elif answer1 == "10":
			return
			if userinfo["location"] == "Sacred Cave":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "Sacred Cave"
				userinfo["location"] = "Sacred Cave"

		elif answer1 == "11":
			return
			if userinfo["location"] == "The Haunted Tomb":
				em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["alreadyat"]["translation"].format(userinfo["location"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				return
			else:
				location_name = "The Haunted Tomb"
				userinfo["location"] = "The Haunted Tomb"

		else:
			return

		em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["traveling"]["translation"].format(location_name), description="{}".format(user.mention), color=discord.Colour(0xffffff))
		if location_name == "Golden Temple":
			em.set_image(url="https://i.imgur.com/6u83Sy9.jpg")
		elif location_name == "Saker Keep":
			em.set_image(url="https://i.imgur.com/xyrgOth.jpg")
		elif location_name == "The Forest":
			em.set_image(url="https://i.imgur.com/FAHXOLl.jpg")
		elif location_name == "Ebony Mountains":
			em.set_image(url="https://i.imgur.com/pPd5s9r.jpg")
		elif location_name == "Zulanthu":
			em.set_image(url="https://i.imgur.com/GEvABaS.jpg")
		elif location_name == "Township of Arkina":
			em.set_image(url="https://i.imgur.com/lypzFbu.jpg")
		elif location_name == "Lost City":
			em.set_image(url="https://i.imgur.com/cBo113x.jpg")
		elif location_name == "Drenheim":
			em.set_image(url="https://i.imgur.com/AVBSEfQ.jpg")
		elif location_name == "Havelow":
			em.set_image(url="https://i.imgur.com/lypzFbu.jpg")
		elif location_name == "The Haunted Tomb":
			em.set_image(url="https://i.imgur.com/duqlXae.jpg")
		elif location_name == "Sacred Cave":
			em.set_image(url="https://i.imgur.com/BwKaOW9.jpg")
		else:
			pass

		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return
		await asyncio.sleep(3)
		userinfo["location"] = location_name
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["travel"]["arrived"]["translation"].format(location_name), description="{}".format(user.mention), color=discord.Colour(0xffffff))
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return
		return

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
	n = travel(bot)
	bot.add_cog(n)