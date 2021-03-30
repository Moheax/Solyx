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


	@commands.group(name="friends", aliases=["f", "friend"], pass_context=True, no_pm=True, hidden=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _friends(self, ctx):
		"""Friends!"""
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

	@_friends.group(name="list", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _list(self, ctx):
		"""Check your friend list"""

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

		for i in range(userinfo["friend_amount"]):

			friend_id = userinfo["friend_list"][i]
			friend_info = db.users.find_one({ "_id": friend_id })


			friend_name = friend_info["name"]
			friend_level = friend_info["lvl"]
			friend_class = friend_info["class"]
		
			flist = ("{}. **{}**: {}<:Magic:560844225839890459> Class: **{}**\n".format(i + 1, friend_name, friend_level, friend_class))

			friend_list_1 +=  flist
			print(friend_id)
			print(friend_name)
			print(friend_level)
			
		em = discord.Embed(description=friend_list_1, color=discord.Colour(0xffffff))
		em.set_author(name="{}'s Friend List\n{}/{} Friends".format(userinfo["name"], userinfo["friend_amount"], userinfo["friend_max_amount"]), icon_url=user.avatar_url)
		em.set_footer(text="You can get more friend Slots by leveling up!")
		try:
			await ctx.send(embed=em)
		except Exception as e:
			print(e)
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return


	
	@_friends.group(name="add", aliases=["invite"], pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _add(self, ctx, user: discord.Member):
		"""Add a friend!"""

		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]

		author = ctx.author

		# INVITER
		authorinfo = db.users.find_one({ "_id": author.id })

		# USER
		userinfo = db.users.find_one({ "_id": user.id })

		# CHECK IF USERS INVITES ITSELF
		if authorinfo["_id"] == userinfo["_id"]:
			await ctx.send("<:Solyx:560809141766193152> **| You can't add yourself as friend.**")
			return

		# CHECK IF USERS EXIST
		if authorinfo["race"] == "None" or authorinfo["class"] == "None":
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		# CHECK IF INVITER HAS FREE FRIEND SLOT

		if authorinfo["friend_amount"] + 1 == authorinfo["friend_max_amount"]:
			
			em = discord.Embed(title="Friend invite", description="You can't add more friends, Level up to get more friends or remove a friend.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
		
		if userinfo["friend_amount"] + 1 == userinfo["friend_max_amount"]:
			
			em = discord.Embed(title="Friend invite", description="User can't add more friends, They have to level up to get more friends or remove a friend.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)


	    # CHECK IF USERS AND AUTHOR ARE ALREADY FRIENDS

		if user.id in authorinfo["friend_list"]:
			em = discord.Embed(title="Friend invite", description="You are already friends with this user.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)

		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to add a friend")

		await ctx.send("{}".format(user.mention))
		em = discord.Embed(title="Friend invite", description="{} (Level: {}) has send a friend invite!\nDo you accept?".format(author.mention, authorinfo["lvl"]), color=discord.Colour(0xffffff))
		em.set_footer(text="Say yes/no")

		await ctx.send(embed=em)
		answer1 = await self.check_answer_other_user(ctx, user, ["yes", "no", "n", "y", "Y", "Yes", "N", "No"])
		if answer1 in ["y", "yes", "Y", "Yes"]:
			userinfo["friend_amount"] += 1
			newfrienduser = authorinfo["_id"]
			userinfo["friend_list"].append(newfrienduser)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

			authorinfo["friend_amount"] += 1
			newfriendauthor = userinfo["_id"]
			authorinfo["friend_list"].append(newfriendauthor)
			db.users.replace_one({ "_id": author.id }, authorinfo, upsert=True)

			em = discord.Embed(title="Friend Invite Accepted", description="{} and {} are now Friends!!".format(user.mention, author.mention), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)

			

		elif answer1 in ["n", "no", "N", "No"]:
			await ctx.send("<:CrossShield:560804112548233217> **| Friend Request Denieid.**")
			return


	@_friends.group(name="remove", pass_context=True, no_pm=True)
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _remove(self, ctx, user: discord.Member):
		"""Remove a friend"""

		languageinfo = db.servers.find_one({ "_id": ctx.guild.id })
		language = languageinfo["language"]

		author = ctx.author

		# INVITER
		authorinfo = db.users.find_one({ "_id": author.id })

		# USER
		userinfo = db.users.find_one({ "_id": user.id })

		# CHECK IF USERS REMOVES ITSELF AS FRIEND
		if authorinfo["_id"] == userinfo["_id"]:
			await ctx.send("<:Solyx:560809141766193152> **| You can't remove yourself as friend.**")
			return

		# CHECK IF USERS EXIST
		if authorinfo["race"] == "None" or authorinfo["class"] == "None":
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

	    # CHECK IF USERS AND AUTHOR ARE ALREADY FRIENDS

		if not user.id in authorinfo["friend_list"]:
			em = discord.Embed(title="Friend invite", description="You are not friends with this user.", color=discord.Colour(0xffffff))
			await ctx.send(embed=em)

		guild = ctx.guild
		channel = ctx.channel
		guildcolor = ctx.author.color

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to remove a friend")


		userinfo["friend_amount"] -= 1
		removedfrienduser = authorinfo["_id"]
		userinfo["friend_list"].remove(removedfrienduser)
		db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

		authorinfo["friend_amount"] -= 1
		removefriendauthor = userinfo["_id"]
		authorinfo["friend_list"].remove(removefriendauthor)
		db.users.replace_one({ "_id": author.id }, authorinfo, upsert=True)

		em = discord.Embed(title="Friend Removed", description="{} and {} are no longer Friends. ;-;".format(user.mention, author.mention), color=discord.Colour(0xffffff))
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
