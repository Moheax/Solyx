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


	@commands.group(name="pet", aliases=["pets", "companion"], pass_context=True, no_pm=True, hidden=True)
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

	@_party.group(name="list", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _list(self, ctx):
		"""Check your party list"""


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
	c = friends(bot)
	bot.add_cog(c)




