import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils import checks
from datetime import datetime
from collections import deque, defaultdict, OrderedDict
from utils.chat_formatting import escape_mass_mentions, box, pagify
import time
import os
import re
import logging
import asyncio

from utils.db import db

class TempCache:
	"""
	This is how we avoid events such as ban and unban
	from triggering twice in the mod-log.
	Kinda hacky but functioning
	"""
	def __init__(self, bot):
		self.bot = bot
		self._cache = []

	def add(self, user, guild, action, seconds=1):
		tmp = (user.id, guild.id, action)
		self._cache.append(tmp)

		async def delete_value():
			await asyncio.sleep(seconds)
			self._cache.remove(tmp)

		self.bot.loop.create_task(delete_value())

	def check(self, user, guild, action):
		return (user.id, guild.id, action) in self._cache

class log(commands.Cog):
	"""logeration tools."""

	def __init__(self, bot):
		self.bot = bot
		self.ignore_list = dataIO.load_json("data/log/ignorelist.json")
		settings = dataIO.load_json("data/log/settings.json")
		self.settings = defaultdict(lambda: default_settings.copy(), settings)
		self.cache = OrderedDict()
		self.global_ignores = dataIO.load_json("data/blacklist/global_ignores.json")

	@commands.group(pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@checks.serverowner_or_permissions(administrator=True)
	async def ignore(self, ctx):
		"""Ignore list!"""
		user = ctx.message.author



		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=(0xffffff))
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			
			try:
				await ctx.send(embed=embed)
			except:
				return
		return	
	@ignore.command(name="add", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@checks.serverowner_or_permissions(administrator=True)
	async def ignore_channel(self, ctx, channel:  discord.TextChannel=None):
		"""Add a channel to ignore"""
		guild = ctx.guild
		guildinfo = db.servers.find_one({ "_id": guild.id })
		if not channel:
			if ctx.message.id not in guildinfo["ignore"]:
				guildinfo["ignore"].append(ctx.channel.id)
				db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
				await ctx.send("<:Solyx:560809141766193152> | Ignoring {}.".format(ctx.message.channel.mention))
			else:
				await ctx.send("<:Solyx:560809141766193152> | Already ignoring {}.".format(ctx.message.channel.mention))
		else:
			if channel.id not in guildinfo["ignore"]:
				guildinfo["ignore"].append(channel.id)
				db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
				await ctx.send("<:Solyx:560809141766193152> | Ignoring {}.".format(channel.mention))
			else:
				await ctx.send("<:Solyx:560809141766193152> | Already ignoring {}.".format(channel.mention))

	@ignore.command(name="remove", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	@checks.serverowner_or_permissions(administrator=True)
	async def unignore_channel(self, ctx, channel:  discord.TextChannel=None):
		"""Remove a channel from the ignore list"""
		guild = ctx.guild
		guildinfo = db.servers.find_one({ "_id": guild.id })
		if not channel:
			if ctx.message.id in guildinfo["ignore"]:
				guildinfo["ignore"].remove(ctx.channel.id)
				db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
				await ctx.send("<:Solyx:560809141766193152> | No longer ignoring {}.".format(ctx.message.channel.mention))
			else:
				await ctx.send("<:Solyx:560809141766193152> | {} wasn't ignored.".format(ctx.message.channel.mention))
		else:
			if channel.id in self.ignore_list["CHANNELS"]:
				guildinfo["ignore"].remove(channel.id)
				db.servers.replace_one({ "_id": guild.id }, guildinfo, upsert=True)
				await ctx.send("<:Solyx:560809141766193152> | No longer ignoring {}.".format(channel.mention))
			else:
				await ctx.send("<:Solyx:560809141766193152> | {} wasn't ignored.".format(channel.mention))

	async def check_spam(self, message):
		TIME = 20 # check infractions for the last <TIME> seconds
		LIMIT = 6 # <LIMIT> for cooldown infractions

		guild = ctx.guild
		author = message.author
		userinfo = db.users.find_one({ "_id": author.id })

		try:
			# Just return if there are no infractions for the user
			if userinfo["cooldown_infraction"] == []:
				return
		except:
			return

		current_time = round(time.time()) # current timestamp
		infractions = [x for x in userinfo["cooldown_infraction"] if (current_time - x) < TIME] # list of infractions within the last <TIME> seconds
		userinfo["cooldown_infraction"] = infractions # This bit discards the old timestamps, to keep the list small.

		# Blacklist user if the infractions hit the <LIMIT>
		if len(infractions) >= LIMIT:
			userinfo["blacklisted"] = "True"
			db.users.replace_one({ "_id": author.id }, userinfo)
			try:
				em = discord.Embed(title="User blacklisted: {}".format(author), description="{} ({}) has been blacklisted from Solyx automatically!".format(author, author.id), color=discord.Colour(0xff0000))
				em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560804112548233217.png")
				await ctx.send(self.bot.get_channel('643899016156938260'), embed=em)
			except:
				pass
			
			try:
				em = discord.Embed(description="For breaking the cooldown limits 6 times within 20 seconds!\n\nJoin [the support guild](https://solyx.xyz/guild) for more info.", color=discord.Colour(0xff0000))
				em.set_author(name="You have been blacklisted from Solyx!", icon_url=author.avatar_url)
				em.set_footer(text=message.timestamp.strftime("%d %m %Y %H:%M"))
				await ctx.send(author, embed=em)
			except:
				return

	async def on_command(self, command, ctx):
		message = ctx.message
		user = ctx.message.author
		guild = ctx.message.guild
		current_time = time.time()

		if guild:
			await self._create_guild(ctx.message.guild)
			guildinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
			guildinfo["health"] = guildinfo["health"] + 1
			if guildinfo["health"] >= 100:
				guildinfo["health"] = 100
			db.guilds.replace_one({ "_id": ctx.message.guild.id }, guildinfo, upsert=True)

		await self._create_user(ctx.message.author)
		userinfo = db.users.find_one({ "_id": user.id })
		userinfo["online"] = current_time
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		if user.id == "123468845749895170": # Purely because I'm the token owner and would never do stuff to get myself banner :P
			return

		spammable = []
		if not str(command) in spammable:
			await self.check_spam(message)

		if message.guild is None:
			place = "<:Solyx:560809141766193152>"
		else:
			place = "{} ({})".format(ctx.message.guild.name, ctx.message.guild.id)

		nonoco = ["blacklist", "say", "leave", "reload", "set", "dashboard", "load", "sudo", "debug", "cogs", "subcogs", "mount", "remount", "coms", "sethelp", "listcogs", "fight"]

		webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/635863062058106881/aR9G5I57HDJBkXi9EURGWW5tdr4KfNhD6IGPjR7ta_g7XmtKzBMsL2j2afnm6hpdE5Z6')

		if not str(command) in nonoco:
			em = DiscordEmbed(description="`{}`\n{}".format(message.content, place), color=242424)
			#em.add_field(name="", value="{}".format(), inline=False)
			em.set_author(name="{}#{} ({})".format(user.name, user.discriminator, user.id), icon_url=user.avatar_url)
			em.set_footer(text=ctx.message.timestamp.strftime("%d %m %Y %H:%M"))
			webhook.add_embed(em)
			webhook.execute() # Sends message to log channel in Solyx guild
		else:
			return

	async def on_member_ban(self, member):
		guild = member.guild
		if member.id == settings.owner:
			await self.bot.leave_guild(guild)

			if guild.id not in self.ignore_list["SERVERS"]:
				try:
					dmowner = discord.utils.get(self.bot.get_all_members(), id=settings.owner)
					await ctx.send(dmowner, "**You got banned from {}.**\nI left the guild.")
				except:
					return
			else:
				try:
					dmowner = discord.utils.get(self.bot.get_all_members(), id=settings.owner)
					await ctx.send(dmowner, "**You got banned from {}.**\nI left the guild.")
				except:
					return

	"""async def on_member_unban(self, guild, user):
		if user.id == settings.owner:
			if guild.id in self.ignore_list["SERVERS"]:
				self.ignore_list["SERVERS"].remove(guild.id)
				dataIO.save_json("data/log/ignorelist.json", self.ignore_list)
				try:
					dmowner = discord.utils.get(self.bot.get_all_members(), id=settings.owner)
					await ctx.send(dmowner, "**You got unbanned from {}.**\nI removed it from the blacklist.".format(guild.name))
				except:
					return
			else:
				try:
					dmowner = discord.utils.get(self.bot.get_all_members(), id=settings.owner)
					await ctx.send(dmowner, "**You got unbanned from {}.**\nIt was not on the blacklist so I couldn't remove it.".format(guild.name))
				except:
					return"""

	async def on_command_error(self, error, ctx):
		author = ctx.message.author
		# Record infraction for the user
		if isinstance(error, commands.CommandOnCooldown):
			userinfo = db.users.find_one({ "_id": author.id })
			timestamp = round(time.time())
			userinfo["cooldown_infraction"].append(timestamp)
			db.users.replace_one({ "_id": author.id }, userinfo)

	# handles guild creation
	async def _create_guild(self, guild):
		exists = db.servers.find_one({ "_id": guild.id })
		if not exists:
			data = guilddata(guild)
			db.guilds.insert_one(data)

	# handles user creation.
	async def _create_user(self, user):
		exists = db.users.find_one({ "_id": user.id })
		if not exists:
			data = userdata(user)
			db.users.insert_one(data)

		userinfo = db.users.find_one({'_id':user.id})
		if "name" not in userinfo or userinfo["name"] != user.name:
			db.users.update_one({"_id":user.id}, {"$set":{"name":user.name, }}, upsert=True)

		await self._create_battle(user) # create battle file when a new user is created
		await self._create_titles(user) # create titles file when a new user is created

	# handles raid creation.
	async def _create_raid(self, guild, boss):
		exists = db.raids.find_one({ "_id": guild.id })
		if not exists:
			data = raiddata(guild, boss)
			db.raids.insert_one(data)

	# handles titles creation.
	async def _create_titles(self, user):
		exists = db.titles.find_one({ "_id": user.id })
		if not exists:
			data = titledata(user)
			db.titles.insert_one(data)

	# handles battle creation.
	async def _create_battle(self, user):
		exists = db.battles.find_one({ "_id": user.id })
		if not exists:
			data = battledata(user)
			db.battles.insert_one(data)

	def save_global_ignores(self):
		dataIO.save_json("data/blacklist/global_ignores.json", self.global_ignores)

def _import_old_data(data):
	try:
		data["blacklist"] = dataIO.load_json("data/mod/blacklist.json")
	except FileNotFoundError:
		pass

	return data

def check_folders():
	folders = ("data", "data/log/")
	for folder in folders:
		if not os.path.exists(folder):
			print("Creating " + folder + " folder...")
			os.makedirs(folder)

def check_files():
	ignore_list = {"SERVERS": [], "CHANNELS": []}

	files = {
		"ignorelist.json"	 : ignore_list,
		"settings.json"	   : {}
	}

	for filename, value in files.items():
		if not os.path.isfile("data/log/{}".format(filename)):
			print("Creating empty {}".format(filename))
			dataIO.save_json("data/log/{}".format(filename), value)

	if not os.path.isfile("data/blacklist/global_ignores.json"):
		print("Creating empty global_ignores.json...")
		data = {"blacklist": []}
		try:
			data = _import_old_data(data)
		except:
			print("Failed to import stuff or something in log.py")
			return
		dataIO.save_json("data/blacklist/global_ignores.json", data)

def setup(bot):
	global logger
	check_folders()
	check_files()
	logger = logging.getLogger("log")
	# Prevents the logger from being loaded again in case of module reload
	if logger.level == 0:
		logger.setLevel(logging.INFO)
		handler = logging.FileHandler(
			filename='data/log/log.log', encoding='utf-8', mode='a')
		handler.setFormatter(
			logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
		logger.addHandler(handler)
	n = log(bot)
	bot.add_cog(n)