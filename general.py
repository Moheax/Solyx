import discord
from discord.ext import commands
import sys
import asyncio
import logging
import os
import importlib
import traceback
import threading
import datetime
import glob
import aiohttp

from copy import deepcopy

from utils.chat_formatting import pagify
from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import userdata, guilddata
from utils.checks import staff, developer, owner

class general(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot
		self.bot.remove_command("help")
		self.logger = logging.getLogger('solyx.general')
		self.session = aiohttp.ClientSession(loop=self.bot.loop)

	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def help(self, ctx, *, command=None):
		if command is not None:
			try:
				ctx.command = self.bot.get_command(command)
				msg = ""
				msg += ctx.command.usage
				em=discord.Embed(title="Example", description="{}{} {}".format(ctx.prefix, ctx.command, msg), colour=0xfffffc)
				em.set_author(name="{}".format(ctx.command), icon_url=ctx.avatar_url)
				em.set_footer(text="{}".format(ctx.command.help))
				await ctx.message.channel.send(embed=em)
				return
			except:
				pass

		msg = "Fun & Addicting Discord RPG focused on activity!\n"
		msg += "➤ [Support](http://solyx.xyz/contact) -help\n"
		msg += "➤ [Invite Solyx](http://solyx.xyz/invite) -invite\n"
		msg += "➤ [Commands](http://solyx.xyz/commands) -commands\n"
		em = discord.Embed(title="Solyx", description=msg, colour=0xfffffc)
		em.set_thumbnail(url=ctx.bot.user.avatar_url)
		#em.set_footer(text="Enjoy!")
		try:
			await ctx.message.channel.send(embed=em)
		except:
			try:
				await ctx.author.send(embed=em)
			except:
				return

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has asked for help")

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def ping(self, ctx):

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has checked the ping! pong!")


		embed = discord.Embed(description='{}ms'.format(round(self.bot.latency * 1000)), colour=0xfffffc)
		embed.set_author(name="Pong!", icon_url=ctx.bot.user.avatar_url, url="https://solyx.xyz")
		#embed.set_footer(text="Enjoy!")
		try:
			await ctx.message.channel.send(embed=embed)
		except:
			try:
				await ctx.author.send(embed=embed)
			except:
				return



	@commands.command()
	@commands.check(owner)
	async def shutdown(self, ctx):
		await ctx.send(':wave: Cya...')
		sys.exit()

	@commands.command()
	@commands.check(developer)
	async def py(self, ctx, code: str):
		result = None
		try:
			result = eval(code)
		except Exception as e:
			await ctx.send('Error:\n```py\n{}\n```'.format(e))
		else:
			if asyncio.iscoroutine(result):
				result = await result
			await ctx.send('Result:\n```py\n{}\n```'.format(result))

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has checked python")

	@commands.command()
	@commands.check(developer)
	async def sudo(self, ctx, user: discord.Member, *, command):
		"""Run a command as if someone else used it"""
		new_msg = deepcopy(ctx.message)
		new_msg.author = user
		new_msg.content = "-" + command
		await self.bot.process_commands(new_msg)

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has TAKEN OVER A USER AAAH")

	@commands.command()
	@commands.guild_only()
	@commands.check(owner)
	async def leave(self, ctx):
		"""Leaves server"""
		await ctx.send(":wave: Bye!")
		await ctx.guild.leave()

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has made the bot leave ;-;")

	@commands.command(name="prefix")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.has_permissions(administrator=True)
	async def serverprefix(self, ctx, *prefixes):
		"""Set a custom server prefixes"""
		guild = ctx.message.guild
		await self._create_guild(guild)
		serverinfo = db.servers.find_one({ "_id": f"{guild.id}" })

		if prefixes == ():

			serverinfo["prefixes"] = []
			db.servers.replace_one({ "_id": f"{guild.id}" }, serverinfo, upsert=True)
			_prefixes = [i for i in serverinfo["prefixes"]]
			list = "\n".join(_prefixes[len(_prefixes):]) if _prefixes else "-\n<@495928914045304847>"
			em = discord.Embed(color=discord.Colour(0xffffff))
			em.add_field(name="Current prefixes:", value="{}".format(list), inline=True)
			em.set_author(name='Prefixes Reset', icon_url=guild.icon_url)
			await ctx.send(embed=em)
			return

		prefixes = sorted(prefixes, reverse=True)
		serverinfo["prefixes"] = prefixes
		db.servers.replace_one({ "_id": f"{guild.id}" }, serverinfo, upsert=True)

		p = "Prefixes" if len(prefixes) > 1 else "Prefix"
		em = discord.Embed(color=discord.Colour(0xffffff))
		em.set_author(name='{} set!'.format(p), icon_url=guild.icon_url)
		await ctx.send(embed=em)

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(owner)
	async def stream(self, ctx, *, title=None):
		"""Sets the bot's streaming status"""
		user = ctx.author
		if not user.id == 123468845749895170:
			return
		guild = ctx.guild
		current_status = guild.me.status if guild is not None else None

		if title:
			title = title.strip()
			stream = discord.Streaming(url="https://www.twitch.tv/#", name=title)
			await self.bot.change_presence(activity=stream, status=current_status, afk=False)
		else:
			await self.bot.change_presence(activity=None, status=current_status, afk=False)
		await ctx.send(":pencil2: | Yes, I'm a streamer!")



	@commands.group()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(developer)
	async def blacklist(self, ctx):
		"""Blacklist commands"""
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
	@blacklist.command(name="add", pass_context=True)
	@commands.check(developer)
	async def _blacklist_add(self, ctx, user: discord.User):
		"""Adds user to the blacklist"""
		author = ctx.author

		userinfo = db.users.find_one({ "_id": user.id })
		try:
			userinfo["blacklisted"] = "True"

			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			await ctx.send(":pencil2: | User has been blacklisted.")

			em = discord.Embed(title="User blacklisted: {}".format(user), description="{} ({}) has been blacklisted from Solyx by {} ({})!".format(user, user.id, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560804112548233217.png")
			await self.bot.get_channel(643899016156938260).send(embed=em)

		except:
			await ctx.send(":pencil2: | User is already blacklisted.")

	@commands.command(name="ban", pass_context=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(developer)
	async def ban_blacklist_add(self, ctx, user: discord.User):
		"""Adds user to the blacklist"""
		author = ctx.author
		authorinfo = db.users.find_one({ "_id": f"{author.id}" })
	

		
		userinfo = db.users.find_one({ "_id": user.id })
		try:
			userinfo["blacklisted"] = "True"
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			await ctx.send(":pencil2: | User has been blacklisted.")

			em = discord.Embed(title="User blacklisted: {}".format(user), description="{} ({}) has been blacklisted from Solyx by {} ({})!".format(user, user.id, author.mention, author.id), color=discord.Colour(0xff0000))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560804112548233217.png")
			await self.bot.get_channel(643899016156938260).send(embed=em)

		except:
			await ctx.send(":pencil2: | User is already blacklisted.")

	@blacklist.command(name="remove", pass_context=True)
	@commands.check(developer)
	async def _blacklist_remove(self, ctx, user: discord.User):
		"""Removes user from the blacklist"""
		author = ctx.author
		authorinfo = db.users.find_one({ "_id": f"{author.id}" })
	

		
		userinfo = db.users.find_one({ "_id": user.id })
		try:
			userinfo["blacklisted"] = "False"
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			await ctx.send(":pencil2: | User has been removed from the blacklist.")

			em = discord.Embed(title="User removed from blacklisted: {}".format(user), description="{} ({}) has been removed from the blacklist by {} ({})!".format(user, user.id, author.mention, author.id), color=discord.Colour(0x00ff00))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560804135545602078.png")
			await self.bot.get_channel(643899016156938260).send(embed=em)

		except:
			await ctx.send(":pencil2: | User wasn't blacklisted.")

	@commands.command(name="unban", pass_context=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(developer)
	async def unban_blacklist_remove(self, ctx, user: discord.User):
		"""Removes user from the blacklist"""
		author = ctx.author
		authorinfo = db.users.find_one({ "_id": f"{author.id}" })
	

		userinfo = db.users.find_one({ "_id": user.id })
		try:
			userinfo["blacklisted"] = "False"
			db.users.replace_one({ "_id": f"{user.id}" }, userinfo, upsert=True)
			await ctx.send(":pencil2: | User has been removed from the blacklist.")

			em = discord.Embed(title="User removed from blacklisted: {}".format(user), description="{} ({}) has been removed from the blacklist by {} ({})!".format(user, user.id, author.mention, author.id), color=discord.Colour(0x00ff00))
			em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560804135545602078.png")
			await self.bot.get_channel(643899016156938260).send(embed=em)

		except:
			await ctx.send(":pencil2: | User wasn't blacklisted.")

	@blacklist.command(name="list", pass_context=True)
	@commands.cooldown(1, 30, commands.BucketType.user)
	@commands.check(developer)
	async def _blacklist_list(self, ctx):
		"""Lists users on the blacklist"""
		author = ctx.author
		authorinfo = db.users.find_one({ "_id": f"{author.id}" })


		blacklist = "\n"
		for userinfo in db.users.find({}):
			if userinfo["blacklisted"] == "True":
				blacklist += "{} ({})\n".format(userinfo["name"], userinfo["_id"])

		blacklist_list = pagify(blacklist, delims=[" ", "\n"])
		for page in blacklist_list:
			em = discord.Embed(description=page, color=discord.Colour(0xffffff))
			em.set_author(name="Blacklisted Users", icon_url=ctx.bot.user.avatar_url)
			try:
				await ctx.send(embed=em)
			except:
				try:
					await author.send(embed=em)
				except:
					pass

	@commands.command()
	@commands.check(developer)
	async def cogs(self, ctx):
		"""Shows all parts of the bot."""
		modules = [x.replace(".py", "") for x in os.listdir("cogs") if ".py" in x]
		loaded = [c.__module__.split(".")[-1] for c in self.bot.cogs.values()]
		unloaded = [c.split(".")[-1] for c in modules if c.split(".")[-1] not in loaded]
		total_modules = len(modules)
		embed=discord.Embed(title=f"Solyx dashboard | Cogs ({total_modules})", colour=discord.Colour(0xfffffc))
		embed.add_field(name=f"✅ Loaded ({len(loaded)})", value=", ".join(loaded) if loaded != [] else "None", inline=False)
		
		embed.add_field(name=f"⛔ Unloaded ({len(unloaded)})", value="\n".join(unloaded) if unloaded != [] else "None", inline=False)
		try:
			await ctx.send(embed=embed)
		except:
			try:
				await ctx.send(":pencil2: | Please give me permissions to send embeded messages.")
			except:
				return

	@commands.command()
	@commands.check(developer)
	async def load(self, ctx, *, module: str):
		"""Load a part of the bot."""
		modules = [x.replace(".py", "") for x in os.listdir("cogs") if ".py" in x]
		msg = ""
		if module.lower() == "all":
			for m in modules:
				if not m == "general":
					try:
						self.bot.load_extension("cogs."+m)
						msg += "`{}` ".format(m)
					except Exception as e:
						print(f'{e}')
						pass
			embed=discord.Embed(title="Cogs Loaded", description=msg, colour=0xfffffc)
			try:
				await ctx.send(embed=embed)
			except:
				try:
					await ctx.send(":pencil2: | Please give me permissions to send embeded messages.")
				except:
					return
		else:
			try:
				self.bot.load_extension("cogs."+module)
			except Exception as e:
				print(f'{e}')
				try:
					await ctx.send(":pencil2: | I couldn't load the cog.")
					return
				except Exception as e:
					print(f'{e}')
					return
			embed=discord.Embed(title="Cog Loaded", description="`{}`".format(module), colour=0xfffffc)
			try:
				await ctx.send(embed=embed)
			except:
				try:
					await ctx.send(":pencil2: | Please give me permissions to send embeded messages.")
				except:
					return

	@commands.command()
	@commands.check(developer)
	async def unload(self, ctx, *, module: str):
		"""Unload a part of the bot."""
		modules = [x.replace(".py", "") for x in os.listdir("cogs") if ".py" in x]
		msg = ""
		if module.lower() == "all":
			for m in modules:
				if not m == "general":
					try:
						self.bot.unload_extension("cogs."+m)
						msg += "`{}` ".format(m)
					except Exception as e:
						print(f'{e}')
						pass
			embed=discord.Embed(title="Cogs Unloaded", description=msg, colour=0xfffffc)
			try:
				await ctx.send(embed=embed)
			except:
				try:
					await ctx.send(":pencil2: | Please give me permissions to send embeded messages.")
				except:
					return
		else:
			try:
				self.bot.unload_extension("cogs."+module)
			except Exception as e:
				print(f'{e}')
				try:
					await ctx.send(":pencil2: | I couldn't unload the cog.")
					return
				except:
					return
			embed=discord.Embed(title="Cog Unloaded", description="`{}`".format(module), colour=0xfffffc)
			try:
				await ctx.send(embed=embed)
			except:
				try:
					await ctx.send(":pencil2: | Please give me permissions to send embeded messages.")
				except:
					return

	@commands.command(hidden=True)
	@commands.check(developer)
	async def reload(self, ctx, *, module: str):
		"""Reloads a part of the bot."""
		modules = [x.replace(".py", "") for x in os.listdir("cogs") if ".py" in x]
		msg = ""
		if module.lower() == "all":
			for m in modules:
				if not m == "general":
					try:
						self.bot.reload_extension("cogs."+m)
						msg += "`{}` ".format(m)
					except Exception as e:
						print(f'{e}')
						pass
			embed=discord.Embed(title="Cogs Reloaded", description=msg, colour=0xfffffc)
			try:
				await ctx.send(embed=embed)
			except:
				try:
					await ctx.send(":pencil2: | Please give me permissions to send embeded messages.")
				except:
					return
		else:
			try:
				self.bot.reload_extension("cogs."+module)
			except Exception as e:
				print(f'{e}')
				try:
					await ctx.send(":pencil2: | I couldn't reload the cog.")
					return
				except:
					return
			embed=discord.Embed(title="Cog Reloaded", description="`{}`".format(module), colour=0xfffffc)
			try:
				await ctx.send(embed=embed)
			except:
				try:
					await ctx.send(":pencil2: | Please give me permissions to send embeded messages.")
				except:
					return

	@commands.command(hidden=True)
	@commands.check(developer)
	async def rawreload(self, ctx, *, module: str):
		"""Reloads a part of the bot."""
		self.bot.reload_extension("cogs."+module)

	@commands.command(hidden=True)
	@commands.check(developer)
	async def rawload(self, ctx, *, module: str):
		"""Reloads a part of the bot."""
		self.bot.load_extension("cogs."+module)

	# handles guild creation.
	async def _create_guild(self, guild):
		exists = db.servers.find_one({ "_id": f"{guild.id}" })
		if not exists:
			data = guilddata(guild)
			db.servers.insert_one(data)

	# handles user creation.
	async def _create_user(self, user):
		exists = db.users.find_one({ "_id": f"{user.id}" })
		if not exists:
			data = userdata(user)
			db.users.insert_one(data)

		userinfo = db.users.find_one({'_id': f"{user.id}" })
		if "name" not in userinfo or userinfo["name"] != user.name:
			db.users.update_one({ "_id": f"{user.id}" }, {"$set":{ "name": f"{user.name}" }}, upsert=True)

		await self._create_titles(user) # create titles file when a new user is created


def setup(bot):
	c = general(bot)
	bot.add_cog(c)
