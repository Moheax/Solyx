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



class friends(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.group(name="pets", aliases=["pet", "companion"], pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _pets(self, ctx):
		"""Pets!"""
		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
			
		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=guildcolor)
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			
			try:
				await ctx.send(embed=embed)
			except:
				return
		return

	@_pets.group(name="list", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _list(self, ctx):
		"""Check your pet list"""


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to check their friend list")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return
		pet_list = ""
		flist = "" 
		f = 0
		
		for i in userinfo["pet_list"]:
			equipped_name = "easter egg"
			try:
				equipped_info = userinfo["equipped_pet"][0]
				equipped_name = equipped_info["name"]
			except:
				pass
			petinfo = i
			pet_name = petinfo["name"]
			pet_type = petinfo["type"]
			pet_level = petinfo["level"]
			pet_xp = petinfo["xp"]
			maxexp = 100 + ((petinfo["level"] + 1) * 3.5)
			if pet_name == equipped_name:
				flist = ("{}. **{}**, Type: {} - Level: {} <:Magic:560844225839890459>,  Exp: {}/{}:sparkles: **Selected!** \n".format(f + 1, equipped_name, pet_type, pet_level, pet_xp, maxexp))
			else:
				flist = ("{}. **{}**, Type: {} - Level: {} <:Magic:560844225839890459>,  Exp: {}/{} :sparkles:\n".format(f + 1, pet_name, pet_type, pet_level, pet_xp, maxexp))

			f += 1

			pet_list +=  flist
		
			
		em = discord.Embed(description=pet_list, color=discord.Colour(0xffffff))
		em.set_author(name="{}'s Pets".format(userinfo["name"]), icon_url=user.avatar_url)
		await ctx.send(embed=em)

	@_pets.group(name="tame", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _tame(self, ctx):
		"""try and tame a pet"""


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		titlesinfo = db.titles.find_one({"_id": user.id})

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to tame a pet")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["pet_find"] == "None":
			em = discord.Embed(title="No tameable pet",description="There's no tameable pets nearby fight bosses to find some!", color=discord.Colour(0xE0119F))
			await ctx.send(embed=em)

		elif userinfo["pet_find"] == "Golden Goose":
			
			pet_tame = random.randint(1, 100)

			if pet_tame >= 80:
				
				em = discord.Embed(title="Tameable pet",description="You have tamed the Goose!\nCheck it in `{}pet list`\n You can equip it with `{}pet equip [number]`\n You can level your pet by giving it food `{}pet feed [number]`\nAlso you can rename your pet with `-pet name [number]` :P".format(ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xE0119F))
				em.set_image(url="")
				await ctx.send(embed=em)

				userinfo["pet_find"] = "None"
				userinfo["pet_list"].append({ "name": "Un-named", "type": "Goose", "level": 1, "xp": 0})
				userinfo["pet_stage"] = "Fox"
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				if not "Goose catcher" in titlesinfo["titles_list"]:
					newtitle = "Goose catcher"
					if not newtitle in titlesinfo["titles_list"]:
						titlesinfo["titles_list"].append(newtitle)
						titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
						db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
						em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
						try:
							await user.send(embed=em)
						except:
							await ctx.send(embed=em)
			else:
				em = discord.Embed(title="Tameable pet",description="You have failed to tame the Goose!\n", color=discord.Colour(0xFF0000))
				em.set_image(url="")
				await ctx.send(embed=em)
				userinfo["pet_find"] = "None"
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				
 
		elif userinfo["pet_find"] == "Fox":
			
			pet_tame = random.randint(1, 100)

			if pet_tame >= 80:
				
				em = discord.Embed(title="Tameable pet",description="You have tamed a fox!\nCheck it in `{}pet list`\n You can equip it with `{}pet equip [number]`\n You can level your pet by giving it food `{}pet feed [number]`\nAlso you can rename your pet with `-pet name [number]` :P".format(ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xE0119F))
				em.set_image(url="")
				await ctx.send(embed=em)

				userinfo["pet_find"] = "None"
				userinfo["pet_list"].append({ "name": "Un-named", "type": "Fox", "level": 1, "xp": 0})
				userinfo["pet_stage"] = "Polar Bear"

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				if not "Fox tracker" in titlesinfo["titles_list"]:
					newtitle = "Fox tracker"
					if not newtitle in titlesinfo["titles_list"]:
						titlesinfo["titles_list"].append(newtitle)
						titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
						db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
						em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
						try:
							await user.send(embed=em)
						except:
							await ctx.send(embed=em)
			else:	
				em = discord.Embed(title="Tameable pet",description="You have failed to tame the Fox!\n", color=discord.Colour(0xE0119F))
				em.set_image(url="")
				await ctx.send(embed=em)
				userinfo["pet_find"] = "None"
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				
				
		elif userinfo["pet_find"] == "Polar Bear":

			pet_tame = random.randint(1, 100)

			if pet_tame >= 80:
				
				em = discord.Embed(title="Tameable pet",description="You have tamed a polar bear!\nCheck it in `{}pet list`\n You can equip it with `{}pet equip [number]`\n You can level your pet by giving it food `{}pet feed [number]`\nAlso you can rename your pet with `-pet name [number]` :P".format(ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xE0119F))
				em.set_image(url="")
				await ctx.send(embed=em)

				userinfo["pet_find"] = "None"
				userinfo["pet_list"].append({ "name": "Un-named", "type": "Polar Bear", "level": 1, "xp": 0})
				userinfo["pet_stage"] = "Small Cerberus"

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				
				if not "Bear friend" in titlesinfo["titles_list"]:
					newtitle = "Bear friend"
					if not newtitle in titlesinfo["titles_list"]:
						titlesinfo["titles_list"].append(newtitle)
						titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
						db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
						em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
						try:
							await user.send(embed=em)
						except:
							await ctx.send(embed=em)
			
			else:	
				em = discord.Embed(title="Tameable pet",description="You have failed to tame the Polar Bear!\n", color=discord.Colour(0xE0119F))
				em.set_image(url="")
				await ctx.send(embed=em)
				userinfo["pet_find"] = "None"
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	

		elif userinfo["pet_find"] == "Small Cerberus":
			
			pet_tame = random.randint(1, 100)

			if pet_tame >= 80:
				
				em = discord.Embed(title="Tameable pet",description="You have tamed a small cerberus!\nCheck it in `{}pet list`\n You can equip it with `{}pet equip [number]`\n You can level your pet by giving it food `{}pet feed [number]`\nAlso you can rename your pet with `-pet name [number]` :P".format(ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xE0119F))
				em.set_image(url="")
				await ctx.send(embed=em)

				userinfo["pet_find"] = "None"
				userinfo["pet_list"].append({ "name": "Un-named", "type": "Small Cerberus", "level": 1, "xp": 0})
				userinfo["pet_stage"] = "None"

				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				
				if not "Strange dog keeper" in titlesinfo["titles_list"]:
					newtitle = "Strange dog keeper"
					if not newtitle in titlesinfo["titles_list"]:
						titlesinfo["titles_list"].append(newtitle)
						titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
						db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
						em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
						try:
							await user.send(embed=em)
						except:
							await ctx.send(embed=em)
			
			else:	
				em = discord.Embed(title="Tameable pet",description="You have failed to tame the Small Cerberus!\n", color=discord.Colour(0xE0119F))
				em.set_image(url="")
				await ctx.send(embed=em)
				userinfo["pet_find"] = "None"
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	


	@_pets.group(name="name", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _name(self, ctx, number: int, name: str):
		"""Name your pet, unequip your pet to rename that one!!"""
		
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip a pet")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		try:
			petinfo = userinfo["pet_list"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No pet in this slot...**")
			return

		try:
			equipped_petinfo = userinfo["equipped_pet"][0]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No pet in this slot...**")
			return
		if equipped_petinfo["name"] == petinfo["name"]:
			petinfo["name"] = name
			equipped_petinfo["name"] = name

		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		em = discord.Embed(title="Pet named",description="You have named your {}!\nit will now be known as  {}".format(petinfo["type"], petinfo["name"]), color=discord.Colour(0xE0119F))
		em.set_image(url="")
		await ctx.send(embed=em)



	@_pets.group(name="equip", aliases=["select"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _equip(self, ctx, number:int):
		"""equip your pet\n"""


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to equip a pet")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		try:
			petinfo = userinfo["pet_list"][number-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No pet in this slot...**")
			return


		pet_name = petinfo["name"]
		pet_type = petinfo["type"]
		pet_level = petinfo["level"]
		pet_xp = petinfo["xp"]
			
			
		flist = ("Equipped **{}**, Type: {} - Level: {} <:Magic:560844225839890459>,  Exp: {} :sparkles:\n".format(pet_name, pet_type, pet_level, pet_xp))
			
		em = discord.Embed(description=flist, color=discord.Colour(0xffffff))
		em.set_author(name="Pet Equip", icon_url=user.avatar_url)
		await ctx.send(embed=em)

		try:
			userinfo["equipped_pet"].remove(userinfo["equipped_pet"][0])
		except:
			pass
		userinfo["equipped_pet"].append(petinfo)		

		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		
	@_pets.group(name="unequip", aliases=["dequip"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _unequip(self, ctx):
		"""unequip your pet"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to unequip a pet")
		
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		try:
					
			equipped_info = userinfo["equipped_pet"][0]
			equipped_name = equipped_info["name"]
			userinfo["equipped_pet"].remove(userinfo["equipped_pet"][0])
			flist = ("You unequipped: **{}**\n\n".format(equipped_name))
			em = discord.Embed(description=flist, color=discord.Colour(0xffffff))
			em.set_author(name="Pet Unequiped", icon_url=user.avatar_url)
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No pet equipped...**")
		return

	@_pets.group(name="feed", aliases=["eat"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _feed(self, ctx, pet:int):
		"""give them food to level up!\n(obtainable in support server lotteries)"""


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to feed their pet")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		try:
			petinfo = userinfo["pet_list"][pet-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No pet in this slot...**")
			return
			
		pet_name = petinfo["name"]
	
		print(userinfo["pet_food"])

		if userinfo["pet_food"] == 0:
			em = discord.Embed(title="OH NO!", description="You have no pet food.\n", color=discord.Colour(0xffd700))
			await ctx.send(embed=em)

		if userinfo["pet_food"] >= 1:
			
			gain = random.randint(10, 15)
			petinfo["xp"] += gain
			userinfo["pet_food"] -= 1

			em = discord.Embed(title="Pet fed!", description="**{} gained {} exp!** <:Experience:560809103346368522>".format(petinfo["name"], gain), color=discord.Colour(0xffd700))
			await ctx.send(embed=em)

			if petinfo["xp"] >= 100 + ((petinfo["level"] + 1) * 3.5):
				petinfo["xp"] = petinfo["xp"] - (100 + ((petinfo["level"] + 1) * 3.5))
				petinfo["level"] = petinfo["level"] + 1
			
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(pet_name), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		
		
	@_pets.group(name="pat", aliases=["pet"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _pat(self, ctx, pet:int):
		"""pat your pet uwu!"""
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has patted their pet uwu")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		try:
			petinfo = userinfo["pet_list"][pet-1]
		except:
			await ctx.send("<:Solyx:560809141766193152> **| No pet in this slot...**")
			return
			
		pet_name = petinfo["name"]
	
		em = discord.Embed(title="You patted {} look how cuteee, your friendship level has increased!".format(pet_name), color=discord.Colour(0xffd700))
		await ctx.send(embed=em)


		
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
				return answer.content #await self.check_answer(ctx, valid_options)  //  This could keep a check loop going

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
	c = friends(bot)
	bot.add_cog(c)

