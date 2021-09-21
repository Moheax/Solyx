import discord
from discord.ext import commands, tasks

import dbl
import asyncio
import datetime
import random
import logging
import os, re, aiohttp
import time
import subprocess
from random import choice as randchoice
from dataIO import js
from utils.dataIO import fileIO
from utils.db import db
from utils.defaults import guilddata, userdata


from quart import Quart, g, request, abort, render_template, session, redirect, url_for, flash, jsonify, send_file
from requests_oauthlib import OAuth2Session
from pymongo import MongoClient
import requests
from cogs.quests import _quest_check

class vote(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot
		self.check_reminders.start()
		self.reminders = fileIO("data/reminders/reminders.json", "load")

# - - - Vote - - - its doing a big dumb and idk why pls help ;-;	

	@commands.group(no_pm=True, invoke_without_command=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.guild_only()
	async def vote(self, ctx):
	
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]


		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Has tried to vote")

		server = ctx.guild
		channel = ctx.channel
		user = ctx.author
		userinfo = db.users.find_one({ "_id": user.id })
		# Account check
		if userinfo["class"] == "None" and userinfo["race"] == "None":
			await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return



		# Time left till user can vote again
		curr_time = time.time()
		delta = float(curr_time) - float(userinfo["vote_block"])
		seconds = 43200 - delta
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)	
		# The actual vote stuff
		if seconds <= 0:
			if userinfo["voted"] == "False":
				try:
					userinfo["vote_block"] = curr_time
					db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
				except:
					pass
				

				color = 0xffffff
				embed = discord.Embed(title=fileIO(f"data/languages/{language}.json", "load")["rpg"]["vote"]["canvote"]["title"]["translation"], description=fileIO(f"data/languages/{language}.json", "load")["rpg"]["vote"]["canvote"]["description"]["translation"], colour=color)
				embed.set_footer(text=fileIO(f"data/languages/{language}.json", "load")["rpg"]["vote"]["canvote"]["footer"]["translation"].format(ctx.prefix))
				embed.set_thumbnail(url=ctx.bot.user.avatar_url)
				try:
					await ctx.send(embed=embed)
				except:
					try:
						await ctx.author.send(embed=embed)
					except discord.HTTPException:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])


			


			# Weekend multiplier is in effect
			if userinfo["voted"] == "weekend":
				votemtp = "×2 Weekend multiplier"
				if userinfo["role"] == "patreon2":
					votegold = random.randint(700, 1000)
					votehp = random.randint(3, 8)
					votelb = random.randint(10, 15)
				elif userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4":
					votegold = random.randint(750, 1200)
					votehp = random.randint(4, 8)
					votelb = random.randint(13, 22)
				else:
					votegold = random.randint(500, 900)
					votehp = random.randint(4, 7)
					votelb = random.randint(9, 12)
			else:
				votemtp = "patreon site launched! 1.1X multiplier! " # New merch! 1.1X multiplier
				#if userinfo["role"] == "patreon2":
				#	votegold = random.randint(700, 1000)
				#	votehp = random.randint(3, 8)
				#	votelb = random.randint(10, 15)
				#elif  userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4":
				#	votegold = random.randint(750, 1200)
				#	votehp = random.randint(4, 8)
				#	votelb = random.randint(13, 22)
				#else:
				#	votegold = random.randint(500, 900)
				#	votehp = random.randint(4, 7)
				#	votelb = random.randint(9, 12)
					
				if userinfo["role"] == "patreon2":
					votegold = random.randint(360, 600)
					votehp = random.randint(3, 5)
					votelb = random.randint(7, 13)
				elif userinfo["role"] == "patreon3" or userinfo["role"] == "patreon4":
					votegold = random.randint(450, 750)
					votehp = random.randint(4, 7)
					votelb = random.randint(9, 18)
				else:
					votegold = random.randint(300, 500)
					votehp = random.randint(2, 5)
					votelb = random.randint(6, 10)

			userinfo["lootbag"] = userinfo["lootbag"] + votelb
			userinfo["keys"] = userinfo["keys"] + votelb
			userinfo["gold"] = userinfo["gold"] + votegold
			userinfo["hp_potions"] = userinfo["hp_potions"] + votehp
			userinfo["vote_block"] = curr_time
			userinfo["voted"] = "False"
			db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

			await asyncio.sleep(random.randint(37, 64))

			# Reward embed
			em = discord.Embed(title="Vote Reward", description="{}\n<:Gold:639484869809930251> **{}**\n<:HealingPotion:573577125064605706> **{}**\n<:Crate:639425690072252426> **{}**\n<:Key:573780034355986432> **{}**\n\n[**New Merch!**](https://teespring.com/stores/solyx-2)\n[**Website**](https://solyxbot.webflow.io/)".format(votemtp, votegold, votehp, votelb, votelb), color=discord.Colour(0xffffff))
			em.set_footer(text="React ⏰ to set a vote reminder!")
			try:
				msg = await channel.send(embed=em)
				# Vote reminder
				await self.vote_reminder(ctx, msg, user)
			except:
				try:
					msg = await user.send(embed=em)
					# Vote reminder
					await self.vote_reminder(ctx, msg, user)
				except:
					pass
			voteinfo = db.users.find_one({ "_id": 387317544228487168 })
			voteinfo["solyxvotes"] = voteinfo["solyxvotes"] + 1
			total_votes = voteinfo["solyxvotes"]
			db.users.replace_one({"_id": 387317544228487168}, voteinfo, upsert=True)
			# Solyx server message
			em = discord.Embed(title="🎉 {} has voted 🎉".format(user.name), description="{} has voted for Solyx!\n**Server:** {}\n **Total Votes: **{}".format(user.mention, server.name, int(total_votes)), color=discord.Colour(0xffffff))
			em.set_thumbnail(url=user.avatar_url)
			em.set_footer(text="{}".format(user.id))
			logchannel = self.bot.get_channel(561200838790479873)
			await logchannel.send(embed=em)

		else:
			em = discord.Embed(title=fileIO(f"data/languages/{language}.json", "load")["rpg"]["vote"]["cooldown"]["title"]["translation"], description=fileIO(f"data/languages/{language}.json", "load")["rpg"]["vote"]["cooldown"]["description"]["translation"].format(int(h), int(m), int(s)), color=discord.Colour(0xffffff))
			em.set_thumbnail(url=ctx.bot.user.avatar_url)
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

	@vote.command(no_pm=True, aliases=["hook", "listener"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def webhook(self, ctx):
		author = ctx.author
		authorinfo = db.users.find_one({ "_id": f"{author.id}" })
		if not authorinfo["role"] in ["Developer", "Staff"]:
			return
		subprocess.Popen([r'C:\Users\Gebruiker\Documents\Nova\Solyx\rewrite\webhooklistener.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
		await ctx.send("<:Solyx:560809141766193152> | Started the webhook listener!")

	async def vote_reminder(self, ctx, message, user):
		try:
			await message.add_reaction('⏰')
		except:
			pass

		await asyncio.sleep(0.3)

		def check(reaction, user):
			return user == message.author and str(reaction.emoji) == '⏰'

		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=20, check=check)
		except:
			try:
				await message.clear_reactions()
			except:
				pass
		else:
			try:
				seconds = 43200
				future = int(time.time()+seconds)
				self.reminders.append({"ID": user.id, "FUTURE": future})
				fileIO("data/reminders/reminders.json", "save", self.reminders)
				logger.info("{} ({}) set a vote reminder.".format(user.name, user.id))
			except:
				try:
					await ctx.send(":x: | I couldn't set the reminder...")
				except:
					return
				return
			try:
				await ctx.send(":alarm_clock: | Reminder set!")
			except:
				pass

# - - - Vote Reminder - - -

	@tasks.loop(seconds=5)
	async def check_reminders(self):
		to_remove = []
		daynumber = datetime.datetime.today().weekday()
		for reminder in self.reminders:
			if reminder["FUTURE"] <= int(time.time()):
				try:
					embed = discord.Embed(description="You can vote again!", colour=0xffffff)
					embed.set_author(name="Vote Reminder", url="https://top.gg/bot/495928914045304847/vote", icon_url="https://i.imgur.com/p1Clibi.png")
					if daynumber >= 4:
						embed.set_footer(text="×2 Weekend multiplier active")
					else:
						pass
					usertosendto = self.bot.get_user(int(reminder["ID"]))
					await usertosendto.send(embed=embed)
					print(f"Vote reminder sent to {reminder['ID']}")
				except:
					pass
				to_remove.append(reminder)
		for reminder in to_remove:
			self.reminders.remove(reminder)
		if to_remove:
			fileIO("data/reminders/reminders.json", "save", self.reminders)





app = Quart(__name__)


@app.route('/', methods=["POST", "GET"])
async def votes_webhook():
	if request.method == 'GET':
		return abort(400)
	if request.method == 'POST':
		if not request.headers.get('authorization') == "387317544228487168":
			return
		data = (await request.json)
		print("VOTE: {}".format(data["user"]))

		userinfo = db.users.find_one({"_id": int(data['user'])})
		if not userinfo:
			return 

		userinfo["vote_info"] = True
		db.users.replace_one({"_id": int(data['user'])}, userinfo, upsert=True)

		return 

	else:
		return abort(400)


if __name__ == "__main__":
	app.run(host="83.82.139.228", port=int(8080), debug=False)

def setup(bot):
	global logger
	logger = logging.getLogger("vote")
	if logger.level == 0: # Prevents the logger from being loaded again in case of module reload
		logger.setLevel(logging.INFO)
		handler = logging.FileHandler(filename='data/reminders/reminders.log', encoding='utf-8', mode='a') # data/reminders/reminders.log
		handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
		logger.addHandler(handler)
	n = vote(bot)
	bot.add_cog(n)