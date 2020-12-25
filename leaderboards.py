import discord
from discord.ext import commands

import datetime
import asyncio
import random
import math
import operator
import pymongo

from time import time

from utils.dataIO import fileIO
from utils.db import db

class leaderboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	def _truncate_text(self, text, max_length):
		if len(text) > max_length:
			if text.strip('$').isdigit():
				text = int(text.strip('$'))
				return "${:.2E}".format(text)
			return text[:max_length-3] + "..."
		return text

	@commands.group(name="leaderboard", aliases=["top"])
	@commands.cooldown(2, 12, commands.BucketType.user)
	async def leaderboard(self, ctx):
		server = ctx.guild
		channel = ctx.channel
		servercolor = ctx.author.color
		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })

		if userinfo["questname"] == "Leaderboard" :
			userinfo["questprogress"] = userinfo["questprogress"] + 1		
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
			if userinfo["questprogress"] >= 1:
				await ctx.send("Quest Updated!")
			pass

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

	@leaderboard.command(name="players", aliases=["player", "users", "user"])
	@commands.cooldown(2, 12, commands.BucketType.user)
	async def playerslb(self, ctx, *options):
		"""See the Solyx players leaderboard"""

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		userinfo = db.users.find_one({ "_id": user.id })

		guildinfo = db.servers.find_one({ "_id": guild.id })

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has check user leaderboard")

		em1 = discord.Embed(description="Gathering leaderboard info <:Solyx:560809141766193152>", color=discord.Colour(0xffffff))
		
					
		try:
			await ctx.send(embed=em1)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["editmsgfail"]["translation"])
				return
			except:
				return
		users = []
		user_stat = None
		title = "Players Leaderboard\n"
		for userinfo in db.users.find({"lvl" : {"$exists": True}}).sort([("lvl", pymongo.DESCENDING)]).limit(10):
			try:
				users.append((userinfo["name"], userinfo["lvl"]))
			except:
				pass

		icon_url = self.bot.user.avatar_url
		

		msg = ""
		rank = 1

		default_label = "⠀"
		special_labels = ["🟃", "🟇", "🟍"]

		for single_user in users:
			
			if rank-1 < len(special_labels):
				label = special_labels[rank-1]
			else:
				label = default_label

			if not single_user[1]:
				msg += u'{:<2}{:<2}|   **{:<22}** `Level: {}`\n'.format(rank, label, self._truncate_text(single_user[0],0), str(single_user[0]))
				rank += 1
			else:
				
				guildtag = guildinfo["tag"]
				if not 'None' in guildinfo["tag"]:
					msg += u'{:<2}{:<2}| **{:<22}** `Level: {}`\n'.format(rank, label, self._truncate_text(single_user[0],10), str(single_user[1]))
					rank += 1
				else:
					msg += u'{:<2}{:<2}|   **{:<22}** `Level: {}`\n'.format(rank, label, self._truncate_text(single_user[0],10), str(single_user[1]))
					rank += 1

		em = discord.Embed(colour=discord.Colour(0xeb3f21))
		em.set_author(name=title, icon_url = icon_url)
		em.add_field(name="Rank		   Name\n", value=msg)
		em.set_footer(text="Your rank: {}".format(await self._find_user_rank(ctx.message.author)))
		try:
			await ctx.send(embed=em)
		except Exception as e:
			print(e)
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except Exception as e:
				print(e)
				return


	async def _find_user_rank(self, user):
		users = []

		for userinfo in db.users.find({}):
			try:
				userid = userinfo["_id"]
				users.append((userid, userinfo["lvl"]))
			except KeyError:
				pass
		sorted_list = sorted(users, key=operator.itemgetter(1), reverse=True)

		rank = 1
		for stats in sorted_list:
			if stats[0] == user.id:
				return rank
			rank+=1

	@leaderboard.command(name="guilds", aliases=["guild"])
	@commands.cooldown(2, 12, commands.BucketType.user)
	async def guildslb(self, ctx, *options):
		"""See the Solyx guilds/guilds leaderboard"""
		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has check user leaderboard")


	

		
		guilds = []
		guild_exps = []
		user_stat = None
		title = "guilds Leaderboard\n"
		for guildinfo in db.servers.find({}):
			try:
				guilds.append((guildinfo["name"], guildinfo["lvl"], guildinfo["tag"]))
				guild_exps.append(guildinfo["exp"])
			except:
				pass

		icon_url = self.bot.user.avatar_url
		sorted_list = sorted(guilds, key=operator.itemgetter(1), reverse=True)
		# multiple page support
		page = 1
		per_page = 10
		pages = math.ceil(len(sorted_list)/per_page)
		for option in options:
			if str(option).isdigit():
				if page >= 1 and int(option) <= pages:
					page = int(str(option))
				else:
					await ctx.send("<:Solyx:560809141766193152> **| Not a valid page number.**")
					return
				break

		msg = ""
		rank = 1 + per_page*(page-1)
		start_index = per_page*page - per_page
		end_index = per_page*page

		default_label = "⠀"
		special_labels = ["🟃", "🟇", "🟍"]

		for single_user in sorted_list[start_index:end_index]:
			if rank-1 < len(special_labels):
				label = special_labels[rank-1]
			else:
				label = default_label

			if 'None' in single_user[2]:
				msg += u'{:<2}{:<2}|   **{:<22}** `Level: {}`\n'.format(rank, label, self._truncate_text(single_user[0],20), str(single_user[1]))
				rank += 1
			else:
				msg += u'{:<2}{:<2}|   [{}] **{:<22}** `Level: {}`\n'.format(rank, label, single_user[2], self._truncate_text(single_user[0],20), str(single_user[1]))
				rank += 1

		em = discord.Embed(colour=discord.Colour(0xeb3f21))
		em.set_author(name=title, icon_url = icon_url)
		em.add_field(name="Rank		   Name\n", value=msg)
		em.set_footer(text="Page {}/{} | guild rank: {}".format(page, pages, await self._find_guild_rank(ctx.message.guild)))
		try:
			guild_exps.sort(reverse=True)
			highest_exp = guild_exps[0]
			top_guild = db.servers.find_one({ "exp": highest_exp })
		except:
			pass
		else:
			topid = top_guild["_id"]
			topguild = self.bot.get_guild(topid)
			em.set_thumbnail(url=topguild.icon_url)
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return
			
		user = ctx.message.author

		print(user.name+"#"+user.discriminator,"Has checked the leaderboard")


	async def _find_guild_rank(self, guild):
		guilds = []

		for guildinfo in db.servers.find({}):
			try:
				guild = guildinfo["_id"]
				
				guilds.append((guildinfo["_id"], guildinfo["exp"]))
			except KeyError:
				pass
		sorted_list = sorted(guilds, key=operator.itemgetter(1), reverse=True)

		rank = 1
		for guilddoc in sorted_list:
			if guilddoc[0] == guild:
				return rank
			rank+=1

def setup(bot):
	n = leaderboard(bot)
	bot.add_cog(n)