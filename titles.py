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



class titles(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

# - - - Titles - - - # 

	@commands.group(name="title", pass_context=True, no_pm=True, aliases=["titles"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def title(self, ctx):

		server = ctx.guild
		channel = ctx.channel
		servercolor = ctx.author.color

		user = ctx.message.author

		print(user.name+"#"+user.discriminator,"Has tried to select a Title")

		msg = ""
		if ctx.invoked_subcommand is None:
			for x in ctx.command.all_commands:
				if x not in ctx.command.all_commands[x].aliases:
					if not ctx.command.all_commands[x].hidden:
						msg += f"`{ctx.prefix}{ctx.command.name} {x}` - {ctx.command.all_commands[x].help} \n"
			embed=discord.Embed(colour=servercolor)
			embed.set_author(name=ctx.command.name, icon_url=ctx.author.avatar_url)
			embed.add_field(name="Subcommands", value=msg, inline=False)
			
			try:
				await ctx.send(embed=embed)
			except:
				return
		return


	@title.command(name="select", pass_context=True, no_pm=True, aliases=["title select"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def title_select(self, ctx):
		"""Select your title"""


		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		titlesinfo = db.titles.find_one({ "_id": user.id })
		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return
		choices = []
		inv_list = [i for i in titlesinfo["titles_list"]]
		if len(inv_list) == 0:
			em = discord.Embed(description=fileIO(f"data/languages/EN.json", "load")["rpg"]["title"]["notitles"]["translation"], color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
		else:
			choices.append(inv_list)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["title"]["select"]["title"]["translation"], color=discord.Colour(0xffffff))
			em.add_field(name="Titles:", value="\n{}".format("\n".join(inv_list)))
			em.set_footer(text=fileIO(f"data/languages/EN.json", "load")["rpg"]["title"]["select"]["footer"]["translation"])
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			answer1 = await self.check_answer(ctx, inv_list)
			em = discord.Embed(title=fileIO(f"data/languages/EN.json", "load")["rpg"]["title"]["selected"]["translation"], description="{}".format(answer1), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			userinfo["title"] = answer1
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
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

	@title.command(name="list", pass_context=True, no_pm=True, aliases=["title list"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def title_list(self, ctx):
		"""List your titles"""


		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		
		titlesinfo = db.titles.find_one({ "_id": user.id })
		# Over here, list_a is the first half of the _members list
		# and list_b is the second half. If _members is an empty
		# array, it just returns "None", otherwise it will join the
		# _members list with "\n"
		_titles = [i for i in titlesinfo["titles_list"]]
		list = "\n".join(_titles) if _titles else "None"

		em = discord.Embed(title="{}'s Titles".format(user.name), color=discord.Colour(0xffffff))
		em.add_field(name="Titles", value=list, inline=True)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

def setup(bot):
	c = titles(bot)
	bot.add_cog(c)