import discord
import random

import datetime
from random import choice as randchoice
from discord.ext import commands
from utils.db import db
from utils.defaults import guilddata
from utils import checks
import asyncio
from utils.dataIO import fileIO

class guild(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	async def check_answer_other_user(self, ctx, user, valid_options):
		answer = await self.bot.wait_for_message(author=user, channel=ctx.message.channel)

		if answer.content.lower() in valid_options:
			return answer.content
		elif answer.content in valid_options:
			return answer.content
		elif answer.content.upper() in valid_options:
			return answer.content
		else:
			return #await self.check_answer(ctx, valid_options)  //  This could keep a check loop going

	@commands.group(pass_context=True, no_pm=True)
	@commands.cooldown(2, 8, commands.BucketType.user)
	async def guild(self, ctx):
		"""Guild stuff"""
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

	"""@guild.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def invite(self, ctx, user: discord.Member):
		author = ctx.message.author
		guild = ctx.message.guild
		authorinfo = db.users.find_one({ "_id": author.id })
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": author.id })
		guildname = authorinfo[""]

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("<:Solyx:560809141766193152> | Please start your character using `{}begin`".format(ctx.prefix))
			return

		if not authorinfo["owner"] == "True":
			await ctx.send("<:Solyx:560809141766193152> **| Only guild owners can invite people.**")
			return

		if not guildinfo:
			await ctx.send("<:Solyx:560809141766193152> **| You are not in a guild.**")
			return

		if len(guild.members) >= 10:
			await ctx.send("<:Solyx:560809141766193152> **| Guilds can only have 10 members.**")
			return

		if "<@{}>".format(user.id) in guildinfo["memberlist"]:
			await ctx.send("<:Solyx:560809141766193152> **| That user is already in your guild!")
			return

		if authorinfo[""] == "None" and not authorinfo["inguild"] == "False":
			await ctx.send("<:Solyx:560809141766193152> **| You are not in a guild.**")
			return

		if userinfo["owner"] == "True":
			await ctx.send("<:Solyx:560809141766193152> **| That user owns a guild.**")
			return

		if (not userinfo[""] == "None") or (not userinfo["inguild"] == "False"):
			await ctx.send("<:Solyx:560809141766193152> **| That user is already in a guild!")

		await ctx.send("{}".format(user.mention))
		em = discord.Embed(title="Guild invite", description="{} has invited you to join {}!\nDo you want to join this guild?".format(author.mention, guildname), color=discord.Colour(0xffffff))
		em.set_thumbnail(url=guild.icon_url)
		await ctx.send(embed=em)
		answer1 = await self.check_answer_other_user(ctx, user, ["yes", "no", "n", "y"])
		if answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes":
			userinfo[""] = guildname
			userinfo["inguild"] = "True"
			userinfo["owner"] = "False"
			guild.id = author.id
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

			len(guild.members) = len(guild.members) + 1
			guildinfo["memberlist"].append("<@" + user.id + ">")
			db.servers.replace_one({ "_id": author.id }, guildinfo, upsert=True)

			em = discord.Embed(title="Joined Guild", description="You are now a member of {}!".format(guildname), color=discord.Colour(0xffffff))
			em.set_thumbnail(url=guild.icon_url)
			await ctx.send(embed=em)

		elif answer1 == "n" or answer1 == "N" or answer1 == "no" or answer1 == "No":
			await ctx.send("<:Guild:560844076967002112> **| Invitation ignored.**")
			return"""

	@guild.command(name="represent", pass_context=True, no_pm=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def guild_represent(self, ctx):
		"""Represent this guild!"""

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Is now representing"+guild.name)

		user = ctx.message.author
		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		guildinfo = db.servers.find_one({ "_id": guild.id })

		userinfo["guild"] = guild.id
		userinfo["GuildTag"] = guildinfo["tag"]
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		em = discord.Embed(title="<:Guild:560844076967002112> Representing", description="You are now representing {}!".format(guild.name), color=discord.Colour(0xffffff))
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

	@guild.command(name="info", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def guild_info(self, ctx):
		"""Show your guild's info."""
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]
			
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Checked guild info")

		user = ctx.message.author
		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if guildinfo["title"] == "None" and guildinfo["bonus"] >= 10:
			guildinfo["title"] = "Big Boys"
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)

		if guildinfo["title"] == "None" or guildinfo["title"] == "Big Boys" and guildinfo["bonus"] >= 30:
			guildinfo["title"] = "Achievers"
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)

		if guildinfo["title"] == "None" and guildinfo["lvl"] >= 3:
			guildinfo["title"] = "Real Deal"
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)

		if guildinfo["title"] == "Big Boys" and guildinfo["lvl"] >= 3:
			guildinfo["title"] = "Real Deal"
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
		try:

			em = discord.Embed(title="Guild Information", description="**Name:** {}\n**Tag:** {}\n**Title:** {}\n**Leader:** {}\n**Members:** {}\n**Level:** {}\n**Exp:** {}\n**Bonus:** {}\n**Health:** {}".format(guildinfo["name"],guildinfo["tag"], guildinfo["title"], guild.owner.mention, len(guild.members), guildinfo["lvl"], guildinfo["exp"], int(guildinfo["bonus"]), guildinfo["health"]), color=discord.Colour(0xffffff))
			em.set_thumbnail(url=guild.icon_url)
			await ctx.send(embed=em)
			return
		except:
			pass
		em = discord.Embed(title="Guild Information", description="**Name:** {}\n**Tag:** {}\n**Title:** {}\n**Leader:** ~\n**Members:** {}\n**Level:** {}\n**Exp:** {}\n**Bonus:** {}\n**Health:** {}".format(guildinfo["name"],guildinfo["tag"], guildinfo["title"], len(guild.members), guildinfo["lvl"], guildinfo["exp"], int(guildinfo["bonus"]), guildinfo["health"]), color=discord.Colour(0xffffff))
		em.set_thumbnail(url=guild.icon_url)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

	@guild.command(name="promote", pass_context=True, no_pm=True)
	@checks.serverowner_or_permissions(administrator=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def guild_promote(self, ctx, user: discord.Member):
		"""Promote someone to officer of your guild."""

		author = ctx.message.author
		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if not author == guild.owner:
			await ctx.send("<:Solyx:560809141766193152> | Only the guild owner can promote members in their own guild.")
			return

		if not userinfo["guild"] == guild.id:
			await ctx.send("<:Solyx:560809141766193152> | {} doesn't represent your guild so I won't promote him.".format(user.mention))
			return

		if author == user:
			await ctx.send("<:Solyx:560809141766193152> | You can't promote yourself!")
			return

		guildinfo["officers"].append(user.id)
		db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)

		em = discord.Embed(title="Guild Promotion", description=":tada: {} got promoted to officer of {}! :tada:".format(user.mention, guild.name), color=discord.Colour(0xffffff))
		em.set_thumbnail(url=guild.icon_url)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
			except:
				pass

		em2 = discord.Embed(title="Guild Promotion", description=":tada: You got promoted to officer of {}! :tada:".format(guild.name), color=discord.Colour(0xffffff))
		em2.set_thumbnail(url=guild.icon_url)
		try:
			await self.bot.send_message(user, embed=em2)
		except:
			pass
		guild = ctx.guild

		channel = ctx.message.channel

		author = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+author.name+"#"+author.discriminator,"Promoted"+user.name)
	@guild.command(name="demote", pass_context=True, no_pm=True)
	@checks.serverowner_or_permissions(administrator=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def guild_demote(self, ctx, user: discord.Member):
		"""Demote someone to officer of your guild."""


		author = ctx.message.author
		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if not author == guild.owner:
			await ctx.send("<:Solyx:560809141766193152> | Only the guild owner can demote members in their own guild.")
			return

		if author == user:
			await ctx.send("<:Solyx:560809141766193152> | You can't demote yourself!")
			return

		if len(guildinfo["officers"]) >= 5:
			await ctx.send("<:Solyx:560809141766193152> | A guild can only have 5 officers.")
			return

		guildinfo["officers"].remove(user.id)
		db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)

		em = discord.Embed(title="Guild Demotion", description="{} got demoted to member in {}.".format(user.mention, guild.name), color=discord.Colour(0xffffff))
		em.set_thumbnail(url=guild.icon_url)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
			except:
				pass

		em2 = discord.Embed(title="Guild Demotion", description="You got demoted to member in {}.".format(guild.name), color=discord.Colour(0xffffff))
		em2.set_thumbnail(url=guild.icon_url)
		try:
			await ctx.send(user, embed=em2)
		except:
			pass	
		guild = ctx.guild

		channel = ctx.message.channel

		author = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+author.name+"#"+author.discriminator,"Demoted"+user.name)
	@guild.command(name="tag", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def guild_tag(self, ctx, tag: str):
		"""Set the tag of your guild."""


		author = ctx.message.author
		guild = ctx.guild
		userinfo = db.users.find_one({ "_id": author.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		allowed = False # I am very professional
		if author.id == guild.owner.id:
			allowed = True
		if author.id in guildinfo["officers"]:
			allowed = True

		if not allowed == True:
			await ctx.send("<:Solyx:560809141766193152> | Only guild officers and the guild leader can change the guild tag!")
			return

		if str(tag) == str(guildinfo["tag"]):
			await ctx.send("<:Solyx:560809141766193152> | The guild tag already is [{}]!".format(guildinfo["tag"]))
			return

		if len(tag) > 4:
			await ctx.send("<:Solyx:560809141766193152> | A guild tag can only be 4 characters long.")
			return

		if not tag.isalnum() is True:
			await ctx.send("<:Solyx:560809141766193152> | A guild tag can only be alphabetical and numeric.")
			return

		available = True
		for guild in db.servers.find({}):
			if guild["tag"].lower() == str(tag).lower():
				available = False

		if available == False:
			await ctx.send("<:Solyx:560809141766193152> | The tag [{}] is already taken!".format(str(tag)))
			return

		guild = ctx.guild
		guildinfo["tag"] = tag
		db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)

		userinfo["GuildTag"] = tag
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		
		
		em = discord.Embed(title="Guild Tag Changed", description="{} changed the tag of {} to [{}]!".format(author.mention, guild.name, tag), color=discord.Colour(0xffffff))
		em.set_thumbnail(url=guild.icon_url)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
			except:
				pass

		if not author == guild.owner:
			em2 = discord.Embed(title="Guild Tag Changed", description="{} changed the tag of {} to [{}]!".format(author.mention, guild.name, tag), color=discord.Colour(0xffffff))
			em2.set_thumbnail(url=guild.icon_url)
			try:
				await self.bot.send_message(guild.owner, embed=em2)
			except:
				pass

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Changed guild tag to"+tag)
	@guild.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def leaders(self, ctx):
		"""A list all officers and the leader of this guild guild."""

		guild = ctx.guild

		channel = ctx.message.channel

		author = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+author.name+"#"+author.discriminator,"check leader list")
		user = ctx.message.author
		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		officerlist = ""
		for member in guildinfo["officers"]:
			officerlist += "<@{}>\n".format(member)
		if not guildinfo["officers"]:
			officerlist = "None"

		em = discord.Embed(title="Guild Leaders", description="**Leader:** {}".format(guild.owner.mention), color=discord.Colour(0xffffff))
		em.add_field(name="Officers", value=officerlist, inline=True)
		em.set_thumbnail(url=guild.icon_url)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

	@guild.command(pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def mission(self, ctx):
		"""Complete missions together to get rewards."""

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Checked guild mission")
		user = ctx.message.author
		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		randommission = randchoice(["Collect 200 wood", "Collect 120 metal", "Collect 160 stone", "Check-in 10 times", "Kill 400 Oofers", "Kill 100 Goblins", "Open 250 Lootbags", "Donate 35000 gold to your guild"]) 
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if guildinfo["mission"] == "None":
			guildinfo["mission"] = randommission
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			em = discord.Embed(title="New Guild Mission!", description="{}.".format(randommission), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
				return
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			return

		if guildinfo["mission"] == "Donate 35000 gold to your guild" and guildinfo["missionprogress"] >= 35000:
			reward1 = random.randint(10, 40)
			em = discord.Embed(title="Mission Completed", description="Your guild completed the Donate 35000 gold to your guild mission and got {} :sparkles: as a reward!".format(reward1), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			guildinfo["mission"] = randommission
			guildinfo["missionscompleted"] = guildinfo["missionscompleted"] + 1
			guildinfo["missionprogress"] = 0
			guildinfo["health"] = 100
			guildinfo["exp"] = guildinfo["exp"] + reward1
			if guildinfo["exp"] >= guildinfo["lvl"]:
				em = discord.Embed(title="Guild Level Up", description=":tada: **{} gained a level!** :tada:".format(guildinfo["name"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				guildinfo["lvl"] = guildinfo["lvl"] + 1
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			return

		elif guildinfo["mission"] == "Collect 200 wood" and guildinfo["missionprogress"] >= 200:
			reward1 = random.randint(10, 40)
			em = discord.Embed(title="Mission Completed", description="Your guild completed the Collect 200 wood mission and got {} :sparkles: as a reward!".format(reward1), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			guildinfo["mission"] = randommission
			guildinfo["missionscompleted"] = guildinfo["missionscompleted"] + 1
			guildinfo["missionprogress"] = 0
			guildinfo["health"] = 100
			guildinfo["exp"] = guildinfo["exp"] + reward1
			if guildinfo["exp"] >= guildinfo["lvl"]:
				em = discord.Embed(title="Guild Level Up", description=":tada: **{} gained a level!** :tada:".format(guildinfo["name"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				guildinfo["lvl"] = guildinfo["lvl"] + 1
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			return

		elif guildinfo["mission"] == "Check-in 10 times" and guildinfo["missionprogress"] >= 10:
			reward1 = random.randint(10, 40)
			em = discord.Embed(title="Mission Completed", description="Your guild completed the Check-in 10 times mission and got {} :sparkles: as a reward!".format(reward1), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			guildinfo["mission"] = randommission
			guildinfo["missionscompleted"] = guildinfo["missionscompleted"] + 1
			guildinfo["missionprogress"] = 0
			guildinfo["health"] = 100
			guildinfo["exp"] = guildinfo["exp"] + reward1
			if guildinfo["exp"] >= guildinfo["lvl"]:
				em = discord.Embed(title="Guild Level Up", description=":tada: **{} gained a level!** :tada:".format(guildinfo["name"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				guildinfo["lvl"] = guildinfo["lvl"] + 1
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			return

		elif guildinfo["mission"] == "Collect 120 metal" and guildinfo["missionprogress"] >= 120:
			reward1 = random.randint(10, 40)
			em = discord.Embed(title="Mission Completed", description="Your guild completed the Collect 120 metal mission and got {} :sparkles: as a reward!".format(reward1), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			guildinfo["mission"] = randommission
			guildinfo["missionscompleted"] = guildinfo["missionscompleted"] + 1
			guildinfo["missionprogress"] = 0
			guildinfo["health"] = 100
			guildinfo["exp"] = guildinfo["exp"] + reward1
			if guildinfo["exp"] >= guildinfo["lvl"]:
				em = discord.Embed(title="Guild Level Up", description=":tada: **{} gained a level!** :tada:".format(guildinfo["name"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				guildinfo["lvl"] = guildinfo["lvl"] + 1
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			return

		elif guildinfo["mission"] == "Collect 160 stone" and guildinfo["missionprogress"] >= 160:
			reward1 = random.randint(10, 40)
			em = discord.Embed(title="Mission Completed", description="Your guild completed the Collect 160 Stone mission and got {} :sparkles: as a reward!".format(reward1), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			guildinfo["mission"] = randommission
			guildinfo["missionscompleted"] = guildinfo["missionscompleted"] + 1
			guildinfo["missionprogress"] = 0
			guildinfo["health"] = 100
			guildinfo["exp"] = guildinfo["exp"] + reward1
			if guildinfo["exp"] >= guildinfo["lvl"]:
				em = discord.Embed(title="Guild Level Up", description=":tada: **{} gained a level!** :tada:".format(guildinfo["name"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				guildinfo["lvl"] = guildinfo["lvl"] + 1
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			return

		elif guildinfo["mission"] == "Open 250 Lootbags" and guildinfo["missionprogress"] >= 250:
			reward1 = random.randint(10, 40)
			em = discord.Embed(title="Mission Completed", description="Your guild completed the open 250 lootbags mission and got {} :sparkles: as a reward!".format(reward1), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			guildinfo["mission"] = randommission
			guildinfo["missionscompleted"] = guildinfo["missionscompleted"] + 1
			guildinfo["missionprogress"] = 0
			guildinfo["health"] = 100
			guildinfo["exp"] = guildinfo["exp"] + reward1
			if guildinfo["exp"] >= guildinfo["lvl"]:
				em = discord.Embed(title="Guild Level Up", description=":tada: **{} gained a level!** :tada:".format(guildinfo["name"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				guildinfo["lvl"] = guildinfo["lvl"] + 1
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			return

		elif guildinfo["mission"] == "Kill 400 Oofers" and guildinfo["missionprogress"] >= 400:
			reward1 = random.randint(20, 50)
			em = discord.Embed(title="Mission Completed", description="Your guild completed the Kill 400 Oofers mission and got {} :sparkles: as a reward!".format(reward1), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			guildinfo["mission"] = randommission
			guildinfo["missionscompleted"] = guildinfo["missionscompleted"] + 1
			guildinfo["missionprogress"] = 0
			guildinfo["health"] = 100
			guildinfo["exp"] = guildinfo["exp"] + reward1
			if guildinfo["exp"] >= guildinfo["lvl"]:
				em = discord.Embed(title="Guild Level Up", description=":tada: **{} gained a level!** :tada:".format(guildinfo["name"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				guildinfo["lvl"] = guildinfo["lvl"] + 1
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			return

		elif guildinfo["mission"] == "Kill 100 Goblins" and guildinfo["missionprogress"] >= 100:
			reward1 = random.randint(10, 30)
			em = discord.Embed(title="Mission Completed", description="Your guild completed the Kill 100 Goblins mission and got {} :sparkles: as a reward!".format(reward1), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			guildinfo["mission"] = randommission
			guildinfo["missionscompleted"] = guildinfo["missionscompleted"] + 1
			guildinfo["missionprogress"] = 0
			guildinfo["health"] = 100
			guildinfo["exp"] = guildinfo["exp"] + reward1
			if guildinfo["exp"] >= guildinfo["lvl"]:
				em = discord.Embed(title="Guild Level Up", description=":tada: **{} gained a level!** :tada:".format(guildinfo["name"]), color=discord.Colour(0xffffff))
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
				guildinfo["lvl"] = guildinfo["lvl"] + 1
			db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
			return

		else:
			if guildinfo["mission"] == "Donate 35000 gold to your guild":
				mtitle = "Money Grab!"
				mdescription = guildinfo["mission"]
				mprogress = guildinfo["missionprogress"]

			elif guildinfo["mission"] == "Collect 200 wood":
				mtitle = "Lumberjack"
				mdescription = guildinfo["mission"]
				mprogress = guildinfo["missionprogress"]

			elif guildinfo["mission"] == "Collect 120 metal":
				mtitle = "Metal Masters"
				mdescription = guildinfo["mission"]
				mprogress = guildinfo["missionprogress"]

			elif guildinfo["mission"] == "Collect 160 stone":
				mtitle = "Stone Masons"
				mdescription = guildinfo["mission"]
				mprogress = guildinfo["missionprogress"]

			elif guildinfo["mission"] == "Check-in 10 times":
				mtitle = "Dedicated"
				mdescription = guildinfo["mission"]
				mprogress = guildinfo["missionprogress"]

			elif guildinfo["mission"] == "Kill 400 Oofers":
				mtitle = "Monster Hunter"
				mdescription = guildinfo["mission"]
				mprogress = guildinfo["missionprogress"]

			elif guildinfo["mission"] == "Kill 100 Goblins":
				mtitle = "Goblin Slayers"
				mdescription = guildinfo["mission"]
				mprogress = guildinfo["missionprogress"]

			elif guildinfo["mission"] == "Open 250 Lootbags":
				mtitle = "Loot Collector"
				mdescription = guildinfo["mission"]
				mprogress = guildinfo["missionprogress"]


			em = discord.Embed(title="{}.".format(mtitle), description="{}".format(mdescription), color=discord.Colour(0xffffff))
			em.add_field(name="Progress", value="{}".format(mprogress), inline=False)
			em.set_thumbnail(url=guild.icon_url)
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	@guild.command(name="donate", pass_context=True, no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def guild_donate(self, ctx, amount: int):
		"""Increase your guild boosters by donating gold."""

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Donated gold to the guild")
		user = ctx.message.author
		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if amount <= 0:
			em = discord.Embed(description="You can't donate negative amounts!", color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			return

		if userinfo["gold"] < amount:
			em = discord.Embed(description="You don't have enough gold.", color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			return


		try:
			if guildinfo["mission"] == "Donate 35000 gold to your guild":
				if not guildinfo["mission"] == "Donate 35000 gold to your guild":
					pass
			try:
				guildinfo["missionprogress"] = guildinfo["missionprogress"] + amount
				db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
				pass
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
				pass
		except:
			print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guild.id)
			pass


		userinfo["gold"] = userinfo["gold"] - amount
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
		gmembercount = len(guild.members)
		taxes = amount / 10000
		finalamt = taxes / (1 * 1)
		guildinfo["bonus"] = guildinfo["bonus"] + finalamt
		db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
		em = discord.Embed(title="You donated {} gold to your guild".format(amount), description="+{} guild boost!".format(finalamt), color=discord.Colour(0xffffff))
		em.set_thumbnail(url=guild.icon_url)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

	"""@guild.group(name="settings", pass_context=True)
	async def guild_settings(self, ctx):
		user = ctx.message.author
		guild = ctx.message.guild
		userinfo = db.users.find_one({ "_id": user.id })
		guildinfo = db.servers.find_one({ "_id": guild.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send("<:Solyx:560809141766193152> | Please start your character using `{}begin`".format(ctx.prefix))
			return

		if not user.id == guild.owner.id:
			await ctx.send("<:Solyx:560809141766193152> **| Only guild owners can edit the guild.**")
			return
		em = discord.Embed(title="Guild Settings", description="Hello, {}. How can I help you?".format(user.mention), color=discord.Colour(0xffffff))
		em.set_thumbnail(url=guild.icon_url)
		em.set_footer(text="Example: -guild settings icon clear")
		await ctx.send(embed=em)
		return"""

	async def _guild_mission_check(self, user, mission, add):
		userinfo = db.users.find_one({ "_id": user.id })
		guildid = guild.id
		guildinfo = db.servers.find_one({ "_id": guildid })

		if guildid == "None":
			return

		if mission == "Donate 35000 gold to your guild":
			try:
				guildinfo["missionprogress"] = guildinfo["missionprogress"] + add
				db.servers.replace_one({ "_id": guildid }, guildinfo, upsert=True)
				return
			except:
				print("Error while trying to log guild mission" + mission + "for: " + user.name + " (" + user.id + ") Guild leader id: " + guildid)
				return

		else:
			print(user.name + " (" + user.id + ") from guild with leader id " + guildid + "managed to check a non-existing mission!")
			return

	async def guild_degenerate(self):
		while self is self.bot.get_cog("guild"):
			for guildinfo in db.servers.find({}):
				idowo = guildinfo["_id"]
				try:
					if guildinfo["health"] <= 0:
						guildinfo["bonus"] = 0
						guildinfo["lvl"] = 0
						guildinfo["exp"] = 0
						guildinfo["gold"] = 0
						guildinfo["stone"] = 0
						guildinfo["metal"] = 0
						guildinfo["wood"] = 0
						guildinfo["title"] = "None"
						guildinfo["inventory"] = []
						db.servers.replace_one({ "_id": idowo }, guildinfo, upsert=True)
					else:
						guildinfo["health"] = guildinfo["health"] - random.randint(0, 2)
						db.servers.replace_one({ "_id": idowo }, guildinfo, upsert=True)
				except:
					try:
						guildinfo["health"] = 100
						db.servers.replace_one({ "_id": idowo }, guildinfo, upsert=True)
					except:
						pass
			await asyncio.sleep(2400)

def setup(bot):
	n = guild(bot)
	loop = asyncio.get_event_loop()
	loop.create_task(n.guild_degenerate())
	bot.add_cog(n)