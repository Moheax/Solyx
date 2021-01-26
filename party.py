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


	@commands.group(name="party", aliases=["p"], pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _party(self, ctx):
		"""Party!"""
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

		friend_list_1 = "" 

		for i in range(userinfo["party_amount"]):

			friend_id = userinfo["party_list"][i]
			friend_info = db.users.find_one({ "_id": friend_id })


			friend_name = friend_info["name"]
			friend_level = friend_info["lvl"]
		
			flist = ("{}. **{}**: {}<:Magic:560844225839890459>\n".format(i + 1, friend_name, friend_level))

			friend_list_1 +=  flist
		
			
		em = discord.Embed(description=friend_list_1, color=discord.Colour(0xffffff))
		em.set_author(name="Party\n{}/4 Members".format(userinfo["party_amount"]), icon_url=user.avatar_url)
		
		try:
			await ctx.send(embed=em)
		except Exception as e:
			print(e)
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return

		
	@_party.group(name="add", aliases=["invite"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _add(self, ctx, user: discord.Member):
		"""invite a user to your party!"""

		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]

		author = ctx.author

		# INVITER
		authorinfo = db.users.find_one({ "_id": author.id })

		# USER
		userinfo = db.users.find_one({ "_id": user.id })

		# CHECK IF USERS INVITES ITSELF
		if authorinfo["_id"] == userinfo["_id"]:
			await ctx.send("<:Solyx:560809141766193152> **| You can't add yourself to your party.**")
			return

		# CHECK IF USERS EXIST
		if authorinfo["race"] == "None" or authorinfo["class"] == "None":
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return


		# CHECK IF USER IS FRIENDS WITH AUTHOR

		if not user.id in authorinfo["friend_list"]:
			em = discord.Embed(title="Party invite", description="You are not friends with this user.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return
		# CHECK IF INVITER HAS FREE PARTY SLOT

		if authorinfo["party_amount"] + 1 == 4:
			
			em = discord.Embed(title="Party invite", description="You can't add more users to the party.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return
		
		if userinfo["in_party"] == "True":
			
			em = discord.Embed(title="Party invite", description="User can't is already in a party.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return

	    # CHECK IF USERS AND AUTHOR ARE ALREADY IN THE PARTY

		if user.id in authorinfo["party_list"]:
			em = discord.Embed(title="Party invite", description="User is already in this Party.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			return
		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to add a user to their party.")

		await ctx.send("{}".format(user.mention))
		em = discord.Embed(title="Party invite", description="{} (Level: {}) has send a Party invite!\nDo you accept?".format(author.mention, authorinfo["lvl"]), color=discord.Colour(0xffffff))
		em.set_footer(text="Say yes/no")

		await ctx.send(embed=em)
		answer1 = await self.check_answer_other_user(ctx, user, ["yes", "no", "n", "y", "Y", "Yes", "N", "No"])
		if answer1 in ["y", "yes", "Y", "Yes"]:
			userinfo["party_amount"] += 1
			newpartyuser = authorinfo["_id"]
			userinfo["party_list"].append(newpartyuser)
			userinfo["in_party"] = "True"
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

			authorinfo["party_amount"] += 1
			newpartyauthor = userinfo["_id"]
			authorinfo["party_list"].append(newpartyauthor)
			authorinfo["in_party"] = "True"
			db.users.replace_one({ "_id": author.id }, authorinfo, upsert=True)

			em = discord.Embed(title="Party Invite Accepted", description="{} has joined the party!".format(user.mention), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)

			

		elif answer1 in ["n", "no", "N", "No"]:
			await ctx.send("<:CrossShield:560804112548233217> **| Party Request Denied.**")
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
