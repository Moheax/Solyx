import discord
from discord.ext import commands

import datetime
import asyncio
import random
from random import choice as randchoice
from time import time

from discord.flags import alias_flag_value

from utils.dataIO import fileIO
from utils.db import db

class toggle(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.group(name="toggle", pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _toggle(self, ctx):
		"""Toggle!"""
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

	@_toggle.group(name="list", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _list(self, ctx):
		"""Check what is or isn't toggled!"""


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has checked toggle list.")

		list = ""

		if userinfo["toggle"][0]["loot"] == False:
			list += "`loot` | Loot reward message: <:ShieldCheck:560804135545602078>\n"
			
		elif userinfo["toggle"][0]["loot"] == True:
			list += "`loot` | Loot reward message: <:ShieldCross:560804112548233217>\n"

		if userinfo["toggle"][0]["level"] == False:
			list += "`level` | levelup message: <:ShieldCheck:560804135545602078>\n"
			
		elif userinfo["toggle"][0]["level"] == True:
			list += "`level` | levelup message: <:ShieldCross:560804112548233217>\n"

		if userinfo["toggle"][0]["tools"] == False:
			list += "`tools` | tools info: <:ShieldCheck:560804135545602078>\n"
			
		elif userinfo["toggle"][0]["tools"] == True:
			list += "`tools` | tools info: <:ShieldCross:560804112548233217>\n"

		if userinfo["toggle"][0]["history"] == False:
			list += "`history` | history info: <:ShieldCheck:560804135545602078>\n"
			
		elif userinfo["toggle"][0]["history"] == True:
			list += "`history` | history info: <:ShieldCross:560804112548233217>\n"

		if userinfo["toggle"][0]["basic"] == False:
			list += "`basic` | basic extra info: <:ShieldCheck:560804135545602078>\n"
			
		elif userinfo["toggle"][0]["basic"] == True:
			list += "`basic` | basic extra info: <:ShieldCross:560804112548233217>\n"

		if userinfo["toggle"][0]["buildings"] == False:
			list += "`buildings` | buildings info: <:ShieldCheck:560804135545602078>\n"
			
		elif userinfo["toggle"][0]["buildings"] == True:
			list += "`buildings` | buildings info: <:ShieldCross:560804112548233217>\n"

		if userinfo["toggle"][0]["items"] == False:
			list += "`items` | items / equipement info: <:ShieldCheck:560804135545602078>\n"
			
		elif userinfo["toggle"][0]["items"] == True:
			list += "`items` | items / equipement info: <:ShieldCross:560804112548233217>\n"

		if userinfo["toggle"][0]["traps"] == False:
			list += "`traps` | traps info: <:ShieldCheck:560804135545602078>\n"
			
		elif userinfo["toggle"][0]["traps"] == True:
			list += "`traps` | traps info: <:ShieldCross:560804112548233217>\n"

		embed=discord.Embed(color=discord.Colour(0xffffff))
		embed.add_field(name="**Toggle list**", value=list.format(ctx.prefix, ctx.prefix), inline=False)
		embed.set_footer(text="Check is on.\nCross is off.\nDefault is checked.")
		await ctx.send(embed=embed)

	@_toggle.group(name="loot", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _loot(self, ctx):
		"""Toggle kill loot reward"""


		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has toggled loot reward")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

	
		if userinfo["toggle"][0]["loot"] == False:
			userinfo["toggle"][0]["loot"] = True
			em = discord.Embed(title="Toggle", description="Loot reward message has been turned off.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

		elif userinfo["toggle"][0]["loot"] == True:
			userinfo["toggle"][0]["loot"] = False
			em = discord.Embed(title="Toggle", description="Loot reward message has been turned on.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

	@_toggle.group(name="level", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _level(self, ctx):
		"""Toggle level up message"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has toggled level message")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["toggle"][0]["level"] == False:
			userinfo["toggle"][0]["level"] = True
			em = discord.Embed(title="Toggle", description="level up message has been turned off.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

		elif userinfo["toggle"][0]["level"] == True:
			userinfo["toggle"][0]["level"] = False
			em = discord.Embed(title="Toggle", description="level up message has been turned on.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return



	@_toggle.group(name="tools", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _tools(self, ctx):
		"""Toggle tool info in stats message"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has toggled tools info")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["toggle"][0]["tools"] == False:
			userinfo["toggle"][0]["tools"] = True
			em = discord.Embed(title="Toggle", description="tools info in stats has been turned off.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

		elif userinfo["toggle"][0]["tools"] == True:
			userinfo["toggle"][0]["tools"] = False
			em = discord.Embed(title="Toggle", description="tools info in stats has been turned on.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

	@_toggle.group(name="history", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _history(self, ctx):
		"""Toggle history info in stats message"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has toggled history info")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["toggle"][0]["history"] == False:
			userinfo["toggle"][0]["history"] = True
			em = discord.Embed(title="Toggle", description="history info in stats has been turned off.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

		elif userinfo["toggle"][0]["history"] == True:
			userinfo["toggle"][0]["history"] = False
			em = discord.Embed(title="Toggle", description="history info in stats has been turned on.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

	@_toggle.group(name="basic", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _basic(self, ctx):
		"""Toggle basic info in stats message"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has toggled basic info")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["toggle"][0]["basic"] == False:
			userinfo["toggle"][0]["basic"] = True
			em = discord.Embed(title="Toggle", description="basic info in stats has been turned off.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

		elif userinfo["toggle"][0]["basic"] == True:
			userinfo["toggle"][0]["basic"] = False
			em = discord.Embed(title="Toggle", description="basic info in stats has been turned on.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

	@_toggle.group(name="buildings", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _buildings(self, ctx):
		"""Toggle buildings info in inventory message"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has toggled buildings info")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["toggle"][0]["buildings"] == False:
			userinfo["toggle"][0]["buildings"] = True
			em = discord.Embed(title="Toggle", description="buildings info in inventory has been turned off.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

		elif userinfo["toggle"][0]["buildings"] == True:
			userinfo["toggle"][0]["buildings"] = False
			em = discord.Embed(title="Toggle", description="buildings info in inventory  has been turned on.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

	@_toggle.group(name="items", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _items(self, ctx):
		"""Toggle items info (equipment / weapons) in inventory message"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has toggled items info")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["toggle"][0]["items"] == False:
			userinfo["toggle"][0]["items"] = True
			em = discord.Embed(title="Toggle", description="items info in inventory has been turned off.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

		elif userinfo["toggle"][0]["items"] == True:
			userinfo["toggle"][0]["items"] = False
			em = discord.Embed(title="Toggle", description="items info in inventory  has been turned on.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

	@_toggle.group(name="traps", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _traps(self, ctx):
		"""Toggle trap info in traps message"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has toggled trap info")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		if userinfo["toggle"][0]["traps"] == False:
			userinfo["toggle"][0]["traps"] = True
			em = discord.Embed(title="Toggle", description="traps info has been turned off.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

		elif userinfo["toggle"][0]["traps"] == True:
			userinfo["toggle"][0]["traps"] = False
			em = discord.Embed(title="Toggle", description="traps info has been turned on.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
			return

	@_toggle.group(name="on", aliases=["all"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _on(self, ctx):
		"""toggle everything on (default)"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has toggled everything on.")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		userinfo["toggle"][0]["loot"] = False
		userinfo["toggle"][0]["level"] = False
		userinfo["toggle"][0]["tools"] = False
		userinfo["toggle"][0]["history"] = False
		userinfo["toggle"][0]["basic"] = False
		userinfo["toggle"][0]["buildings"] = False
		userinfo["toggle"][0]["items"] = False
		userinfo["toggle"][0]["traps"] = False

		em = discord.Embed(title="Toggle", description="Everyhing has been set to on (default).", color=discord.Colour(0xffffff))
		await ctx.send(embed=em)
		db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

	@_toggle.group(name="off", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _off(self, ctx):
		"""toggle everything off"""

		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		
		guild = ctx.guild

		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has toggled everything off.")

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		userinfo["toggle"][0]["loot"] = True
		userinfo["toggle"][0]["level"] = True
		userinfo["toggle"][0]["tools"] = True
		userinfo["toggle"][0]["history"] = True
		userinfo["toggle"][0]["basic"] = True
		userinfo["toggle"][0]["buildings"] = True
		userinfo["toggle"][0]["items"] = True
		userinfo["toggle"][0]["traps"] = True
		em = discord.Embed(title="Toggle", description="Everyhing has been set to off.", color=discord.Colour(0xffffff))
		await ctx.send(embed=em)
		db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

def setup(bot):
	c = toggle(bot)
	bot.add_cog(c)