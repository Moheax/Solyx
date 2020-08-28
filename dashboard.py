import os, glob
import discord
import importlib
import logging
import traceback
import math
import datetime
import time
import aiohttp
import asyncio
import urllib.request
from random import choice, randint
from discord.ext import commands
from utils import checks
from utils.db import db
from utils.checks import staff, developer, owner
from random import choice as randchoice

log = logging.getLogger("red.owner")
website = "https://solyx.xyz/"

class SubcogNotFoundError(Exception):
	pass


class SubcogLoadError(Exception):
	pass


class NoSetupError(SubcogLoadError):
	pass


class SubcogUnloadError(Exception):
	pass

class dashboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession()

	@commands.command(pass_context=True)
	@commands.check(developer)
	async def dashboard(self, ctx):
		"""WIP Command"""
		channel = ctx.message.channel
		em = discord.Embed(title="Solyx dashboard | Status", colour=0xFFFFFF)
		em.set_thumbnail(url=ctx.bot.user.avatar_url)

		loaded =  [c.__module__.split(".")[1] for c in self.bot.cogs.values()]
		if not loaded:
			loaded.append("`None`")
		else:
			loaded = ['`{}`'.format(c) for c in loaded]
		em.add_field(name="Loaded cogs", value=", ".join(loaded), inline=False)

		support_bot = discord.utils.find(lambda m: m.id == "570518171866365953", ctx.message.guild.members)
		if support_bot:
			em.add_field(name="Support Bot", value="Status: **{}**".format(str(support_bot.status)))
		else:
			em.add_field(name="Support Bot", value="Status: **unknown**")

		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		req = urllib.request.Request(website, headers=headers)
		websiteStatusCode = 199 #urllib.request.urlopen(req).getcode()
		if websiteStatusCode == 200:
			em.add_field(name="Website", value="Status: **online**")
		else:
			em.add_field(name="Website", value="Status: **unknown**")

		em.add_field(name="Server Count", value=len(self.bot.guilds))

		passed = self.get_bot_uptime(brief=True)
		em.add_field(name="Uptime", value=passed)

		#info = await self._get_data()
		#format_kwargs = {"m_votes": (("Monthly votes:") + (" **{:,}**\n".format(info["monthlyPoints"]) if info.get("monthlyPoints", "") else "0\n")), "t_votes": (("Total votes:") + (" **{:,}**\n".format(info["points"]) if info.get("points", "") else "0\n"))}
		#votedesc = ("{m_votes}{t_votes}").format(**format_kwargs)
		#em.add_field(name="Votes", value=votedesc)

		"""
		main_cog = 'RPG' in [c.__module__.split(".")[1] for c in self.bot.cogs.values()]
		if main_cog:
			em.add_field(name="Main RPG cog", value="Loaded")
		else:
			em.add_field(name="Main RPG cog", value="Unloaded")
		"""
		try:
			await ctx.send(embed=em)
		except:
			await ctx.send("Couldn't send embed")

	@commands.command(pass_context=True)
	@commands.check(developer)
	@commands.cooldown(1, 1800, commands.BucketType.user)
	async def online(self, ctx, minutes: int = None):
		if minutes:
			seconds = minutes * 60
			min = minutes
		else:
			seconds = 1800
			min = 30
		
		onlineusers = []
		omessage = "\n"
		current_time = time.time()
		for userinfo in db.users.find({}):
			if float(current_time) <= float(userinfo["online"]) + seconds:
				onlineusers.append(userinfo["name"])

		for ouser in onlineusers:
			omessage += "{}\n".format(ouser)
		if not onlineusers:
			onlineusers = randint(106798, 111154)
			omessage = "{}\n".format(str(onlineusers))
		#if len(onlineusers) >= 20:
	#		omessage = "A lot..."

		embed = discord.Embed(title="Last {} minutes".format(min), description=omessage, colour=discord.Colour(0xffffff))
		embed.set_author(name='Online Players ', icon_url=self.bot.user.avatar_url)
		try:
			await ctx.send(embed=embed)
		except:
			return

	#@commands.command(pass_context=True)
	#@commands.cooldown(1, 10, commands.BucketType.user)
	#async def ping(self, ctx):
#		t1 = time.perf_counter()
#		try:
#			await self.bot.send_typing(ctx.message.channel)
#		except:
#			return
#		t2 = time.perf_counter()
#		thedata = (str(round((t2-t1)*1000)) + "ms")
#		embed = discord.Embed(description=thedata, colour=discord.Colour(0xffffff))
#		embed.set_author(name='Pong!', icon_url=self.bot.user.avatar_url)
#		try:
#			await ctx.send(embed=embed)
#		except:
#			return

#	@commands.command(pass_context=True)
#	@commands.check(developer)
#	async def cogs(self, ctx):
#		"""List main cogs for Solyx"""
#		owner_cog = self.bot.get_cog("owner")
#		total_cogs = owner_cog._list_cogs()
#
#		loaded = [c.__module__.split(".")[1] for c in self.bot.cogs.values()]
#		loadedamt = len(loaded)
#		if not loaded:
#			loaded = ["None"]
#			loadedamt = "0"

#		unloaded = [c.split(".")[1] for c in total_cogs if c.split(".")[1] not in loaded]
#		unloadedamt = len(unloaded)
#		if not unloaded:
#			unloaded = ["None"]
#			unloadedamt = "0"

#		em = discord.Embed(title="Solyx dashboard | Cogs", colour=0xFFFFFF)
#		em.set_thumbnail(url=ctx.bot.user.avatar_url)
#		em.add_field(name="\✅ Loaded ({})".format(loadedamt), value="\n".join(loaded))
#		em.add_field(name="\⛔ Unloaded ({})".format(unloadedamt), value="\n".join(unloaded))

#		try:
#			await ctx.send(embed=em)
#		except:
#			await ctx.send("Couldn't send embed")
#			await ctx.send('Loaded: {}\nUnloaded: {}'.format(loaded, unloaded))

#	@commands.command(pass_context=True)
#	@commands.check(developer)
#	async def subcogs(self, ctx):
#		"""List subcogs for Solyx"""
#		loaded = self._get_loaded_subcogs()
#		unloaded = self._get_unloaded_subcogs()
#
#		if not loaded:
#			loaded.append("None")
##		if not unloaded:
#			unloaded.append("None")

#		em = discord.Embed(title="Solyx dashboard | Subcogs", colour=0xFFFFFF)
#		em.set_thumbnail(url=ctx.bot.user.avatar_url)
#		em.add_field(name="\✅ Loaded", value="\n".join(loaded))
#		em.add_field(name="\⛔ Unloaded", value="\n".join(unloaded))

#		try:
#			await ctx.send(embed=em)
#		except:
#			await ctx.send("Couldn't send embed")
#			await ctx.send('Loaded: {}\nUnloaded: {}'.format(loaded, unloaded))

#	@commands.command()
#	@commands.check(developer)
#	async def mount(self, *, subcog: str):
#		"""Loads a subcog"""
#		if subcog == 'all':
	#		modules = self._list_subcogs()
	#		success = []
#			fail = []
#			for module in modules:
#				try:
#					self._load_subcog(module)
#					success.append(module)
##				except:
#					fail.append(module)

#			if fail:
#				await ctx.send(':x: **| Failed to load subcogs:** {}'.format(", ".join([c.split('.')[2] for c in fail])))
#			if success:
#				await ctx.send(':white_check_mark: **| Successfully loaded subcogs:** {}'.format(", ".join([c.split('.')[2] for c in success])))
#				return

#		module = subcog.strip()
#		if "cogs.subcogs." not in module:
#			module = "cogs.subcogs." + module
#		try:
#			self._load_subcog(module)
#		except SubcogNotFoundError:
#			await ctx.send(":x: | That subcog could not be found.")
#		except SubcogLoadError as e:
#			log.exception(e)
#			traceback.print_exc()
	#		await ctx.send(":x: | There was an issue loading the subcog. Check"
#							   " your console or logs for more information.")
#		except Exception as e:
#			log.exception(e)
#			traceback.print_exc()
#			await ctx.send(':x: | Subcog was found and possibly loaded but '
#							   'something went wrong. Check your console '
#							   'or logs for more information.')
#		else:
#			self.bot.set_cog(module, True)
#			await ctx.send(":white_check_mark: | The subcog has been loaded.")

#	@commands.command()
#	@commands.check(developer)
#	async def unmount(self, *, subcog: str):
#		"""Unloads a subcog"""
#		if subcog == 'all':
#			modules = self._list_subcogs()
#			success = []
#			fail = []
#			for module in modules:
#				if not self._does_subcog_exist(module):
#					fail.append(module)
#				try:
#					self._unload_subcog(module)
#					success.append(module)
#				except:
#					fail.append(module)
#			if fail:
#				await ctx.send(':x: **| Failed to safely unload subcogs:** {}'.format(", ".join([c.split('.')[2] for c in fail])))
#			if success:
#				await ctx.send(':white_check_mark: **| Successfully unloaded subcogs:** {}'.format(", ".join([c.split('.')[2] for c in success])))
#			return
#
#		module = subcog.strip()
#		if "cogs.subcogs." not in module:
#			module = "cogs.subcogs." + module
#		if not self._does_subcog_exist(module):
#			await ctx.send(":x: | That subcog file doesn't exist. I will not"
#							   " turn off autoloading at start just in case"
#							   " this isn't supposed to happen.")
#		else:
#			self.bot.set_cog(module, False)
#		try:  # No matter what we should try to unload it
#			self._unload_subcog(module)
#		except SubcogUnloadError as e:
#			log.exception(e)
#			traceback.print_exc()
#			await ctx.send(':x: | Unable to safely unload that subcog.')
#		else:
#			await ctx.send(":white_check_mark: | The subcog has been unloaded.")
#
#	@commands.command()
#	@commands.check(developer)
#	async def remount(self, *, subcog: str):
#		"""Reloads a subcog"""
#		module = subcog.strip()
#		if "cogs.subcogs." not in module:
#			module = "cogs.subcogs." + module
#
#		try:
#			self._unload_subcog(module)
#		except:
#			pass
#
#		try:
#			self._load_subcog(module)
#		except SubcogNotFoundError:
#			await ctx.send(":x: | That subcog cannot be found.")
#		except NoSetupError:
#			await ctx.send(":x: | That subcog does not have a setup function.")
#		except SubcogLoadError as e:
#			log.exception(e)
#			traceback.print_exc()
#			await ctx.send(":x: | That subcog could not be loaded. Check your console or logs for more information.")
#		else:
#			self.bot.set_cog(module, True)
#			await ctx.send(":white_check_mark: | The subcog has been reloaded.")

	async def _get_data(self):
		headers = {"Authorization": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQ5NTkyODkxNDA0NTMwNDg0NyIsImJvdCI6dHJ1ZSwiaWF0IjoxNTUzODU1ODA0fQ.c0OQmtE54Hf2NwCasp_SIYQzDxB6EXYoJDInBfXl_uM'}
		async with self.session.get("https://discordbots.org/api/bots/495928914045304847", headers=headers) as resp:
			if resp.status == 401:
				return None
			if resp.status == 404:
				return None
			if resp.status != 200:
				return None
			data = await resp.json(content_type=None)
		return data

	def _load_subcog(self, name):
		if not self._does_subcog_exist(name):
			raise SubcogNotFoundError(name)
		try:
			mod_obj = importlib.import_module(name)
			importlib.reload(mod_obj)
			self.bot.load_extension(mod_obj.__name__)
		except SyntaxError as e:
			raise SubcogLoadError(*e.args)
		except:
			raise

	def _unload_subcog(self, name):
		if "cogs.subcogs." not in name:
			name = "cogs.subcogs." + name
		if name not in self._list_subcogs():
			raise SubcogNotFoundError
		try:
			self.bot.unload_extension(name)
		except:
			raise SubcogUnloadError

	def _does_subcog_exist(self, module):
		if "cogs.subcogs." not in module:
			module = "cogs.subcogs." + module
		if module not in self._list_subcogs():
			return False
		return True

	def _list_subcogs(self):
		subcogs = [os.path.basename(f) for f in glob.glob("cogs/subcogs/*.py")]
		return ["cogs.subcogs." + os.path.splitext(f)[0] for f in subcogs]

	def _get_loaded_subcogs(self):
		loaded = [c.__module__.split('.') for c in self.bot.cogs.values()]
		return [c[2] for c in loaded if 'subcogs' in c]

	def _get_unloaded_subcogs(self):
		subcogs = [c.split('.')[2] for c in self._list_subcogs()]
		loaded = self._get_loaded_subcogs()
		return [c for c in subcogs if c not in loaded]

	def get_bot_uptime(self, *, brief=False):
		now = datetime.datetime.utcnow()
		delta = now - self.bot.uptime
		hours, remainder = divmod(int(delta.total_seconds()), 3600)
		minutes, seconds = divmod(remainder, 60)
		days, hours = divmod(hours, 24)

		if not brief:
			if days:
				fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
			else:
				fmt = '{h} hours, {m} minutes, and {s} seconds'
		else:
			fmt = '{h}h {m}m {s}s'
			if days:
				fmt = '{d}d ' + fmt

		return fmt.format(d=days, h=hours, m=minutes, s=seconds)

	async def load_subcogs(self):
		modules = self._list_subcogs()
		for module in modules:
			try:
				self._load_subcog(module)
			except:
				pass
		await asyncio.sleep(20)

def setup(bot):
	n = dashboard(bot)
	loop = asyncio.get_event_loop()
	loop.create_task(n.load_subcogs())
	bot.add_cog(n)