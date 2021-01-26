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
from collections import Counter
import datetime
import os
import asyncio

try:
	import psutil
except:
	psutil = False

from utils.dataIO import dataIO
from utils.checks import staff, developer, owner



class statistics(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.counter = Counter()	


	def redapi_hook(self, data=None):
		if not data:
			x = self.retrieve_statistics()
			x['avatar'] = self.bot.user.avatar_url if self.bot.user.avatar else self.bot.user.default_avatar_url
			x['uptime'] = self.get_bot_uptime(brief=False)
			x['total_cogs'] = len(self.bot.cogs)
			x['total_commands'] = len(self.bot.commands)
			x['discord_version'] = str(discord.__version__)
			x['id'] = self.bot.user.id
			x['discriminator'] = self.bot.user.discriminator
			x['created_at'] = self.bot.user.created_at.strftime('%B %d, %Y at %H:%M:%S')
			x['loaded_cogs'] = [cog for cog in self.bot.cogs]
			x['prefixes'] = self.bot.settings.prefixes
			x['guilds'] = [{'name': guild.name, 'members': len(guild.members), 'icon_url': guild.icon_url} for guild in self.bot.guilds]
			x['cogs'] = len(self.bot.cogs)
			return x
		else:
			pass


	@commands.command(aliases=["info"])
	@commands.cooldown(1, 12, commands.BucketType.user)
	async def information(self, ctx):
		"""Bot information"""

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has opened info")

		embed = discord.Embed(description="Click [here](https://solyxbot.webflow.io/team) for a detailed documentation.", color=discord.Colour(0xffffff))
		avatar = self.bot.user.avatar_url if self.bot.user.avatar else self.bot.user.default_avatar_url
		embed.set_author(name="Solyx Info", icon_url=avatar)
		embed.add_field(name="Developers", value="`TheMaksoo#1212`", inline=False)
		embed.add_field(name="Managing assistant", value="`AceTheBearg223#4562`", inline=False)
		embed.add_field(name="Library", value="Discord.py", inline=False)
		try:
			await ctx.send(embed=embed)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return
		
	
	@commands.command()
	@commands.check(developer)
	async def statistics(self, ctx):

		message2 = await self.embed_statistics()

		await ctx.send(embed=message2)

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+user.discriminator,"stared at statistics")

		
	async def embed_statistics(self):
		stats = self.retrieve_statistics()
		
		em = discord.Embed(color=discord.Colour(0xffffff))
		avatar = self.bot.user.avatar_url if self.bot.user.avatar else self.bot.user.default_avatar_url
		em.set_author(name='Solyx statistics', icon_url=avatar)
		em.add_field(name='**Uptime**', value='{}'.format(self.get_bot_uptime(brief=True)))
		em.add_field(name=u'\u2063', value=u'\u2063')
		em.add_field(name=u'\u2063', value=u'\u2063')

		em.add_field(name='**Servers**', value=stats['total_guilds'])
		em.add_field(name='**Users**', value=stats['users'])
		em.add_field(name='**Messages received**', value=str(stats['read_messages']))
		em.add_field(name='**Commands run**', value=str(stats['commands_run']))

		em.add_field(name='**Channels**', value=str(stats['channels']))
		em.add_field(name='**Text channels**', value=str(stats['text_channels']))
		em.add_field(name='**Voice channels**', value=str(stats['voice_channels']))

		em.add_field(name='**CPU**', value='{0:.1f}%'.format(stats['cpu_usage']))
		em.add_field(name='**Memory**', value='{0:.0f} MB ({1:.2f}%)'.format(stats['mem_v_mb'] / 1024 / 1024, stats['mem_v']))
		em.add_field(name='**Threads**', value='{}'.format(stats['threads']))
		em.set_footer(text='API version {}'.format(discord.__version__))

		
		return em

		

	def retrieve_statistics(self):
		

		
		name = self.bot.user.name
		users = db.users.count()
		guilds = str(len(self.bot.guilds))
		commands_run = self.counter["commands"] 
		read_messages = self.counter["messages"] 
		text_channels = 0
		voice_channels = 0
		command_count = 0
		message_count = 0




		process = psutil.Process()

		cpu_usage = psutil.cpu_percent()

		mem_v = process.memory_percent()
		mem_v_mb = process.memory_full_info().uss
		threads = process.num_threads()

		io_reads = process.io_counters().read_count
		io_writes = process.io_counters().write_count

		for channel in self.bot.get_all_channels():
			if channel.type == discord.ChannelType.text:
				text_channels += 1
			elif channel.type == discord.ChannelType.voice:
				voice_channels += 1
		channels = text_channels + voice_channels

		stats = {
			'name': name, 'users': users, 'total_guilds': guilds, 'commands_run': commands_run,
			'read_messages': read_messages, 'text_channels': text_channels,
			'voice_channels': voice_channels, 'channels': channels,
			'cpu_usage': cpu_usage, 'mem_v': mem_v, 'mem_v_mb': mem_v_mb, 'threads': threads,
			'io_reads': io_reads, 'io_writes': io_writes}
		return stats

	def get_bot_uptime(self, *, brief=False):
		now = datetime.datetime.now()
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


	@commands.Cog.listener()
	async def on_command(self, ctx_command):
		
		self.counter["commands"] += 1
		
	@commands.Cog.listener()		
	async def on_message(self, message):
		
		self.counter["messages"] += 1
		
def check_folder():
	if not os.path.exists('data/statistics'):
		print('Creating data/statistics folder...')
		os.makedirs('data/statistics')

def check_file():
	data = {}
	data['CHANNEL_ID'] = None
	data['REFRESH_RATE'] = 10
	f = 'data/statistics/settings.json'
	if not dataIO.is_valid_json(f):
		print('Creating default settings.json...')
		dataIO.save_json(f, data)

	



def setup(bot):
	if psutil is False:
		raise RuntimeError('psutil is not installed. Run `pip3 install psutil --upgrade` to use this cog.')
	else:
		check_folder()
		check_file()
		n = statistics(bot)
		bot.add_cog(n)