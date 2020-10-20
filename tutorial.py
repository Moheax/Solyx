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




class tutorial(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

#No response
	@commands.command (pass_context=True, no_pm=True)
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def tutorial(self, ctx):
		languageinfo = db.servers.find_one({ "_id": ctx.message.guild.id })
		language = languageinfo["language"]

		user = ctx.message.author
		channel = ctx.message.channel

		userinfo = db.users.find_one({ "_id": user.id })

		guild = ctx.guild

		channel = ctx.message.channel

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"has checked the tutorial")

		em = discord.Embed(title="Let's get started!", description="You can find the online tutorial [Here](https://solyxbot.webflow.io/tutorial)!".format(ctx.prefix), color=discord.Colour(0xffffff))
		#em.add_field(name="", value="", inline=False)
		em.set_author(name="Solyx Tutorial", icon_url=user.avatar_url)
		#em.set_footer(text="")
		try:
			await ctx.send(embed=em)
		except:
			try:
				await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
				return
			except:
				return








		""" 
		completiontime = datetime.datetime.now() + datetime.timedelta(minutes=15)
		valid_options = ["Archer", "Knight", "Mage", "Thief", "archer", "knight", "mage", "thief"]
		answer = await self.check_tutorial_answer(user, channel, valid_options, completiontime)
		if answer:
			await asyncio.sleep(2)
			em = discord.Embed(title="Good choice!", description="The {} class is a lot of fun to play!\nLet's start your first fight!\nType **{}fight** to start a fight!".format(answer, ctx.prefix), color=discord.Colour(0xffffff))
			#em.add_field(name="", value="", inline=False)
			em.set_author(name="Solyx Tutorial", icon_url=user.avatar_url)
			#em.set_footer(text="")
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return

			completiontime = datetime.datetime.now() + datetime.timedelta(minutes=15)
			valid_options = ["Shoot", "Swing", "Cast", "Stab", "shoot", "swing", "cast", "stab"]
			answer = await self.check_tutorial_answer(user, channel, valid_options, completiontime)
			if answer:
				await asyncio.sleep(2)
				em = discord.Embed(title="Nice!", description="You seem to have talent!\nYou took a bit of damage, let's fix that.\nType **{}heal** to regain some HP!".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Reward:", value="5 <:HealingPotion:573577125064605706>", inline=False)
				em.set_author(name="Solyx Tutorial", icon_url=user.avatar_url)
				#em.set_footer(text="")
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

				userinfo = db.users.find_one({ "_id": user.id })

				userinfo["hp_potions"] = userinfo["hp_potions"] + 5
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

				completiontime = datetime.datetime.now() + datetime.timedelta(minutes=15)
				valid_options = ["{}heal".format(ctx.prefix)]
				answer = await self.check_tutorial_answer(user, channel, valid_options, completiontime)
				if answer:
					await asyncio.sleep(2)
					em = discord.Embed(title="Good job!", description="You can check your stats using the **{0}stats** or **{0}profile** command.\nThere are quite a few statistics commands like {0}health and {0}rank.".format(ctx.prefix), color=discord.Colour(0xffffff))
					#em.add_field(name="", value="", inline=False)
					em.set_author(name="Solyx Tutorial", icon_url=user.avatar_url)
					#em.set_footer(text="")
					try:
						await ctx.send(embed=em)
					except:
						try:
							await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
							return
						except:
							return

					completiontime = datetime.datetime.now() + datetime.timedelta(minutes=15)
					valid_options = ["{}stats".format(ctx.prefix), "{}profile".format(ctx.prefix)]
					answer = await self.check_tutorial_answer(user, channel, valid_options, completiontime)
					if answer:
						await asyncio.sleep(2)
						em = discord.Embed(title="Well done!", description="You can find crates and keys by fighting monsters.\nThese will get stored in your inventory.\nYou can open a crate using the {0}crate or {0}open command. You can get a ton of different rewards from crates. These items will get stored in your inventory too.\nCheck out the **{0}inventory** command.".format(ctx.prefix), color=discord.Colour(0xffffff))
						em.add_field(name="Reward:", value="2 <:Crate:639425690072252426>\n2 <:Key:573780034355986432>", inline=False)
						em.set_author(name="Solyx Tutorial", icon_url=user.avatar_url)
						#em.set_footer(text="")
						try:
							await ctx.send(embed=em)
						except:
							try:
								await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
								return
							except:
								return

						userinfo["keys"] = userinfo["keys"] + 2
						userinfo["lootbag"] = userinfo["lootbag"] + 2
						db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)

						completiontime = datetime.datetime.now() + datetime.timedelta(minutes=15)
						valid_options = ["{}inv".format(ctx.prefix), "{}inventory".format(ctx.prefix)]
						answer = await self.check_tutorial_answer(user, channel, valid_options, completiontime)
						if answer:
							await asyncio.sleep(2)
							em = discord.Embed(title="It's not that interesting yet...", description="Once you have an item, you can equip it using the {0}equip command.\nYou can also buy items from the market using the **{0}market** command.".format(ctx.prefix), color=discord.Colour(0xffffff))
							#em.add_field(name="", value="", inline=False)
							em.set_author(name="Solyx Tutorial", icon_url=user.avatar_url)
							#em.set_footer(text="")
							try:
								await ctx.send(embed=em)
							except:
								try:
									await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
									return
								except:
									return

							completiontime = datetime.datetime.now() + datetime.timedelta(minutes=15)
							valid_options = ["{}market".format(ctx.prefix)]
							answer = await self.check_tutorial_answer(user, channel, valid_options, completiontime)
							if answer:
								await asyncio.sleep(2)
								em = discord.Embed(title="Sweet!", description="Every server also is a guild.\nThe guild leader is the owner of the server of course.\nYou get a lot of advantages from being in a high level guild like bonus gold and experience.\nHowever, guilds have health that decreases over time.\nYou can only restore your guild's health by completing guild missions.\nCheck out **{0}guild**.".format(ctx.prefix), color=discord.Colour(0xffffff))
								#em.add_field(name="", value="", inline=False)
								em.set_author(name="Solyx Tutorial", icon_url=user.avatar_url)
								#em.set_footer(text="")
								try:
									await ctx.send(embed=em)
								except:
									try:
										await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
										return
									except:
										return

								completiontime = datetime.datetime.now() + datetime.timedelta(minutes=15)
								valid_options = ["{}guild".format(ctx.prefix)]
								answer = await self.check_tutorial_answer(user, channel, valid_options, completiontime)
								if answer:
									await asyncio.sleep(2)
									em = discord.Embed(title="You are ready to start playing!", description="There are more commands and things available that aren't explained in this tutorial.\nYou can check them out using {0}commands.".format(ctx.prefix), color=discord.Colour(0xffffff))
									#em.add_field(name="", value="", inline=False)
									em.set_author(name="Solyx Tutorial", icon_url=user.avatar_url)
									em.set_footer(text="Enjoy!")
									try:
										await ctx.send(embed=em)
									except:
										try:
											await ctx.send(fileIO(f"data/languages/{language}.json", "load")["general"]["embedpermissions"]["translation"])
											return
										except:
											return
									return
									"""

	async def check_tutorial_answer(self, user, channel, valid_options, time):
		if datetime.datetime.now() >= time:
			return
			def pred(m):
				return m.author == message.author and m.channel == message.channel


			answer = await self.bot.wait_for('awnser', check=pred, timeout=300)

			# First check to make sure answer and answer.content exists
			# to prevent any errors when accessing them.
			if not answer or not answer.content:

				return await self.check_tutorial_answer(user, channel, valid_options, time)  #  This keeps a check_tutorial_answer loop going
		
			elif answer.content.lower() in valid_options:
				return answer.content

			elif answer.content in valid_options:
				return answer.content

			elif answer.content.upper() in valid_options:
				return answer.content

			else:
				return await self.check_tutorial_answer(user, channel, valid_options, time)  #  This keeps a check_tutorial_answer loop going





def setup(bot):
	n = tutorial(bot)
	bot.add_cog(n)