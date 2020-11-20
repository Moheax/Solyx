import discord
import random

import datetime
from random import choice as randchoice
from discord.ext import commands
from utils.db import db
from utils.defaults import userdata, titledata
from utils import checks
import asyncio
from utils.dataIO import fileIO

class quests(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	async def check_answer_other_user(self, ctx, user, valid_options):
		answer = await self.bot.wait_for_message(author=user, channel=ctx.message.channel)

		if answer.content.lower() in valid_options:
			return answer.content
		elif answer.content in valid_options:
			return answer.content
		elif answer.content.upper() in valid_options:
			return answer.content
		else:
			return #await self.check_answer(ctx, valid_options)  //  This could keep a check loop going



	@commands.command(pass_context=True,aliases=["quest"], no_pm=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def quests(self, ctx):
		"""Shows Current quests progress"""

		guild = ctx.guild

		channel = ctx.message.channel

		user = ctx.message.author

		now = datetime.datetime.now()

		current_time = now.strftime("%H:%M:%S")

		print(current_time+" | "+guild.name+" | "+channel.name+" | "+user.name+"#"+user.discriminator,"Checked quests")





		user = ctx.message.author
		userinfo = db.users.find_one({ "_id": user.id })
		titlesinfo = db.titles.find_one({ "_id": user.id })

		if (not userinfo) or (userinfo["race"] == "None") or (userinfo["class"] == "None"):
			await ctx.send(fileIO(f"data/languages/En.json", "load")["general"]["begin"]["translation"].format(ctx.prefix))
			return

		if userinfo and userinfo["blacklisted"] == "True":
			return

		# QUEST TITLE CHECKS

		# Rookie Contractor 10
	
		if "Health acquisition" in userinfo["questscompleted"] and not "Rookie Contractor" in titlesinfo["titles_list"]:
			newtitle = "Rookie Contractor"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)	
		# Novice Contractor 25
		if "Debin I" in userinfo["questscompleted"] and not "Novice Contractor" in titlesinfo["titles_list"]:
			newtitle = "Novice Contractor"
			if not newtitle in titlesinfo["titles_list"]:
				titlesinfo["titles_list"].append(newtitle)
				titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
				db.titles.replace_one({ "_id": user.id }, titlesinfo, upsert=True)
				em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
				try:
					await user.send(embed=em)
				except:
					await ctx.send(embed=em)
		
					
		# Aspiring Contractor 50			
		# Trusted Contractor 75
		# Famed Contractor 100
		# Noble Contractor 150

		if userinfo["questname"] == "Basic A" and userinfo["questprogress"] >= 1:
			oldquest = "Basic A"

			expgain = 20

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience".format(oldquest, expgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			newquest = "Basic B"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Open your Inventory!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Basic B" and userinfo["questprogress"] >= 1:
			oldquest = "Basic B"

			expgain = 20
			goldgain = 20

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Basic C"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Start your first fight!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Basic C" and userinfo["questprogress"] >= 1:
			oldquest = "Basic C"

			expgain = 25
			goldgain = 25

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Gathering Wood I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Gather 5 Wood!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Gathering Wood I" and userinfo["questprogress"] >= 5:
			oldquest = "Gathering Wood I"

			expgain = 30
			goldgain = 30

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Gathering Stone I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Gather 5 Stone!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Gathering Stone I" and userinfo["questprogress"] >= 5:
			oldquest = "Gathering Stone I"

			expgain = 30
			goldgain = 30

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Gathering Metal I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Gather 2 Metal!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Gathering Metal I" and userinfo["questprogress"] >= 2:
			oldquest = "Gathering Metal I"

			expgain = 30
			goldgain = 30

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Gathering Fish I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Fish 5 times!".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Gathering Fish I" and userinfo["questprogress"] >= 5:
			oldquest = "Gathering Fish I"

			expgain = 30
			goldgain = 30

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold".format(oldquest, expgain, goldgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Wood Trader I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Sell 10 Wood!".format(newquest), color=discord.Colour(0xffffff)) # MAKE WOOD TRADER I 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Wood Trader I" and userinfo["questprogress"] >= 10:
			oldquest = "Wood Trader I"

			expgain = 35
			goldgain = 35
			crategain = 1

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crate".format(oldquest, expgain, goldgain, crategain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Stone Trader I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Sell 10 Stone!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Stone Trader I" and userinfo["questprogress"] >= 10:
			oldquest = "Stone Trader I"

			expgain = 35
			goldgain = 35
			crategain = 1

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crate".format(oldquest, expgain, goldgain, crategain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Metal Trader I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Sell 5 Metal!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Metal Trader I" and userinfo["questprogress"] >= 5:
			oldquest = "Metal Trader I"

			expgain = 35
			goldgain = 35
			crategain = 1

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crate".format(oldquest, expgain, goldgain, crategain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Health acquisition"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\nBuy 5 Hp potions!\nUse 1 Hp potions".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Health acquisition" and userinfo["questpart"] == 2 and userinfo["questprogress"] >= 1:
			oldquest = "Health acquisition"

			expgain = 40
			goldgain = 40
			crategain = 2

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates".format(oldquest, expgain, goldgain, crategain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Unboxing I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Open 10 crates".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Unboxing I"  and userinfo["questprogress"] >= 10:
			oldquest = "Unboxing I"

			expgain = 45
			goldgain = 45
			crategain = 5

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates".format(oldquest, expgain, goldgain, crategain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Daily I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\nTry and collect your daily reward!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Daily I"  and userinfo["questprogress"] >= 1:
			oldquest = "Daily I"

			expgain = 45
			goldgain = 45
			crategain = 2
			keygain = 2

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys".format(oldquest, expgain, goldgain, crategain, keygain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Equip"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Equip a weapon.".format(newquest), color=discord.Colour(0xffffff))
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return
		elif userinfo["questname"] == "Equip" and userinfo["questpart"] == 2 and userinfo["questprogress"] >= 1:
			oldquest = "Equip"

			expgain = 50
			goldgain = 50
			crategain = 3
			keygain = 3

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys".format(oldquest, expgain, goldgain, crategain, keygain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Vote I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Vote for solyx to get extra rewards!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Vote I"  and userinfo["questprogress"] >= 1:
			oldquest = "Vote I"

			expgain = 55
			goldgain = 55
			crategain = 3
			keygain = 3

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys".format(oldquest, expgain, goldgain, crategain, keygain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Fight I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Fight 25 times.".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Fight I"  and userinfo["questprogress"] >= 25:
			oldquest = "Fight I"

			expgain = 60
			goldgain = 60
			crategain = 3
			keygain = 3

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys".format(oldquest, expgain, goldgain, crategain, keygain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Wiki Check"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Discover the usefulness of wiki!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Wiki Check"  and userinfo["questprogress"] >= 1:
			oldquest = "Wiki Check"

			expgain = 60
			goldgain = 60
			crategain = 4
			keygain = 4

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys".format(oldquest, expgain, goldgain, crategain, keygain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Shop I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Visit the shop and buy weapon and armor!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Shop I"  and userinfo["questpart"] == 4 and userinfo["questprogress"] >= 1:
			oldquest = "Shop I"

			expgain = 65
			goldgain = 65
			crategain = 4
			keygain = 4
			hpgain = 1

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Check Profile"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Take a look at your visual profile!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Check Profile"  and userinfo["questprogress"] >= 1:
			oldquest = "Check Profile"

			expgain = 70
			goldgain = 70
			crategain = 4
			keygain = 4
			hpgain = 2

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Leaderboard"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Check out the leaderboard!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Leaderboard"  and userinfo["questprogress"] >= 1:
			oldquest = "Leaderboard"

			expgain = 75
			goldgain = 75
			crategain = 4
			keygain = 4
			hpgain = 2

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Guild I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Represent a guild\nCheck guild info\nCheck guild mission\nCheck guild donate function.".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		
		elif userinfo["questname"] == "Guild I"  and userinfo["questpart"] == 4 and userinfo["questprogress"] >= 1:
			oldquest = "Guild I"

			expgain = 80
			goldgain = 80
			crategain = 5
			keygain = 5
			hpgain = 3

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Shop II"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Try and sell a item in the Shop".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Shop II" and userinfo["questprogress"] >= 1:
			oldquest = "Shop II"

			expgain = 85
			goldgain = 85
			crategain = 5
			keygain = 5
			hpgain = 3
			exppgain = 1

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Market I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Take a look at the market!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Market I" and userinfo["questprogress"] >= 1:
			oldquest = "Market I"

			expgain = 90
			goldgain = 90
			crategain = 5
			keygain = 5
			hpgain = 4
			exppgain = 2

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Guild II"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Donate 1000g to your guild!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Guild II" and userinfo["questprogress"] >= 1000:
			oldquest = "Guild II"

			expgain = 95
			goldgain = 95
			crategain = 6
			keygain = 6
			hpgain = 5
			exppgain = 3

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Rachi I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Slay 10 Rachi's!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)	
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Rachi I" and userinfo["questprogress"] >= 10:
			oldquest = "Rachi I"

			expgain = 100
			goldgain = 100
			crategain = 6
			keygain = 6
			hpgain = 5
			exppgain = 4

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Debin I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Slay 10 Debin's!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)		
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Debin I" and userinfo["questprogress"] >= 10:
			oldquest = "Debin I"

			expgain = 100
			goldgain = 100
			crategain = 6
			keygain = 6
			hpgain = 5
			exppgain = 4

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Oofer I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Slay 10 Oofer's!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Oofer I" and userinfo["questprogress"] >= 10:
			oldquest = "Oofer I"

			expgain = 100
			goldgain = 100
			crategain = 6
			keygain = 6
			hpgain = 5
			exppgain = 4

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Wyvern I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Slay 10 Wyvern's!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Wyvern I" and userinfo["questprogress"] >= 10:
			oldquest = "Wyvern I"

			expgain = 100
			goldgain = 100
			crategain = 6
			keygain = 6
			hpgain = 5
			exppgain = 4

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Fire Golem I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\n Slay 5 Fire Golem's!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Fire Golem I" and userinfo["questprogress"] >= 5:
			oldquest = "Fire Golem I"

			expgain = 110
			goldgain = 110
			crategain = 7
			keygain = 7
			hpgain = 6
			exppgain = 5

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Travel I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\nTravel to Saker Keep!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Travel I" and userinfo["questprogress"] >= 1:
			oldquest = "Travel I"

			expgain = 120
			goldgain = 120
			crategain = 7
			keygain = 7
			hpgain = 6
			exppgain = 6

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Draugr I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n**Objective**\nSlay 10 Draugr's!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Draugr I" and userinfo["questprogress"] >= 10:
			oldquest = "Draugr I"

			expgain = 130
			goldgain = 130
			crategain = 8
			keygain = 8
			hpgain = 7
			exppgain = 7

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Stalker I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n**Objective**\nSlay 10 Stalker's!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		
		elif userinfo["questname"] == "Stalker I" and userinfo["questprogress"] >= 10:
			oldquest = "Stalker I"

			expgain = 130
			goldgain = 130
			crategain = 8
			keygain = 8
			hpgain = 7
			exppgain = 7

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Souleater I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n**Objective**\nSlay 10 Souleater's!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		
		elif userinfo["questname"] == "Souleater I" and userinfo["questprogress"] >= 10:
			oldquest = "Souleater I"

			expgain = 130
			goldgain = 130
			crategain = 8
			keygain = 8
			hpgain = 7
			exppgain = 7

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "The Corrupted I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n**Objective**\nSlay 10 Corrupted's!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		
		elif userinfo["questname"] == "The Corrupted I" and userinfo["questprogress"] >= 5:
			oldquest = "The Corrupted I"

			expgain = 130
			goldgain = 130
			crategain = 8
			keygain = 8
			hpgain = 7
			exppgain = 7

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Reforge I"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\nReforge a item!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Reforge I" and userinfo["questprogress"] >= 1:
			oldquest = "Reforge I"

			expgain = 135
			goldgain = 135
			crategain = 9
			keygain = 9
			hpgain = 8
			exppgain = 8

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Support Server"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\nJoin the support server to stay  up-to-date with updates\n and if necessary some support!!\nJoin [here](https://discord.gg/9b3KkJvJea)".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "Support Server" and userinfo["questprogress"] >= 1:
			oldquest = "Support Server"

			expgain = 140
			goldgain = 140
			crategain = 10
			keygain = 10
			hpgain = 9
			exppgain = 9

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "On the hunt!"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\nHunt down a Rare Wyvern\n They have been spotted in the golden temple!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return

		elif userinfo["questname"] == "On the hunt!" and userinfo["questprogress"] >= 1:
			oldquest = "On the hunt!"

			expgain = 145
			goldgain = 145
			crategain = 10
			keygain = 10
			hpgain = 10
			exppgain = 10

			em = discord.Embed(title="Quest Completed", description="You completed  **{}**\n\n **Rewards**\n:sparkles: {} Experience\n<:Gold:639484869809930251> {} Gold\n <:Crate:639425690072252426> {} Crates\n<:Key:573780034355986432> {} Keys\n<:HealingPotion:573577125064605706> {} Health potion\n <:ExpBottle:770044187348566046> {} Experience potion".format(oldquest, expgain, goldgain, crategain, keygain, hpgain, exppgain), color=discord.Colour(0xffffff))
			try:
				await ctx.send(embed=em)
			except:
				try:
					await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
					return
				except:
					return
			
			newquest = "Claim your loot!"
			userinfo["questname"] = newquest
			userinfo["questscompleted"].append(oldquest)
			userinfo["questprogress"] = 0
			userinfo["questpart"] = 0
			userinfo["exp"] = userinfo["exp"] + expgain
			userinfo["gold"] = userinfo["gold"] + goldgain
			userinfo["lootbag"] = userinfo["lootbag"] + crategain
			userinfo["keys"] = userinfo["keys"] + keygain
			userinfo["hp_potions"] = userinfo["hp_potions"] + hpgain
			userinfo["exp_potions"] = userinfo["exp_potions"] + exppgain
			em = discord.Embed(title="New Quest!", description=":notebook_with_decorative_cover: Your new quest is **{}**\n\n**Objective**\nOpen 10 lootbags\n you earned it!".format(newquest), color=discord.Colour(0xffffff)) 
			await ctx.send(embed=em)
			db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
			if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
				userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
				userinfo["lvl"] = userinfo["lvl"] + 1
				userinfo["health"] = 100
				em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
				await ctx.send(embed=em)
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				await asyncio.sleep(0.3)
				if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
					userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
					userinfo["lvl"] = userinfo["lvl"] + 1
					userinfo["health"] = 100
					em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
					await ctx.send(embed=em)
					db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
					await asyncio.sleep(0.3)
			return


		# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000


		else:
			if userinfo["questname"] == "Basic A":
				em = discord.Embed(title="Basic A", description="**Objective**\nTake look at your stats.\nType {}stats".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Unopend stats", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Basic B":
				em = discord.Embed(title="Basic B", description="**Objective**\nOpen your inventory.\nType {}inv".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Unopend Inventory", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Basic C":
				em = discord.Embed(title="Basic C", description="**Objective**\nStart your first Fight.\nType {}fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Fight not started.", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Gathering Wood I":
				em = discord.Embed(title="Gathering Wood I", description="**Objective**\nGather 5 wood.\nType {}chop".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/5 Wood collected".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Gathering Stone I":
				em = discord.Embed(title="Gathering Stone I", description="**Objective**\nGather 5 Stone.\nType {}mine".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/5 Stone collected".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Gathering Metal I":
				em = discord.Embed(title="Gathering Metal I", description="**Objective**\nGather 2 Metal.\nType {}mine".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/2 Metal collected".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Gathering Fish I":
				em = discord.Embed(title="Gathering Fish I", description="**Objective**\nFish 5 times.\nType {}fish".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/5 times Fished".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Wood Trader I":
				em = discord.Embed(title="Wood Trader I", description="**Objective**\nSell 10 Wood.\nType {}sell wood <amount> / all".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Wood Sold".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Stone Trader I":
				em = discord.Embed(title="Stone Trader I", description="**Objective**\nSell 10 Stone.\nType {}sell stone <amount> / all".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Stone Sold".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Metal Trader I":
				em = discord.Embed(title="Metal Trader I", description="**Objective**\nSell 10 Metal.\nType {}sell metal <amount> / all".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/5 Metal Sold".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Health acquisition" and  userinfo["questpart"] == 0:
				em = discord.Embed(title="Health acquisition", description="**Objective**\nBuy 5 health potions.\nType {}buy hp <amount>\n\nUse 1 hp potion\nType {}heal".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Part 1/2\n{}/5 health potions bought".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Health acquisition" and  userinfo["questpart"] == 1:
				userinfo["questprogress"] = 0
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True)
				em = discord.Embed(title="Health acquisition", description="**Objective**\nUse 1 hp potion\nType {}heal".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Part 2/2\n{}/1 health potions used".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Unboxing I":
				em = discord.Embed(title="Unboxing I ", description="**Objective**\nOpen 10 Crate.\nType {}lb / {}crate".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Crates opened".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Daily I":
				em = discord.Embed(title="Daily I ", description="**Objective**\nCollect your first daily reward.\nType {}daily / {}checkin".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Daily not collected", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Equip" and userinfo["questpart"] == 0:
				em = discord.Embed(title="Equip", description="**Objective**\nEquip a weapon\nType {}equip weapon <number>\n Equip a armor piece.\nType {}equip armor <number>.".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Part 1/2\nEquip a weapon", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Equip" and userinfo["questpart"] == 1:
				userinfo["questprogress"] = 0
				em = discord.Embed(title="Equip", description="**Objective**\n Equip a armor piece.\nType {}equip armor <number>".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Part 2/2\nEquip a armor piece", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Vote I":
				em = discord.Embed(title="Vote I ", description="**Objective**\nVote for solyx to get extra rewards!.\nType {}vote ".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Not voted yet", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Fight I":
				em = discord.Embed(title="Fight I", description="**Objective**\nFight 25 times\nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/25 times fought".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Wiki Check":
				em = discord.Embed(title="Wiki Check", description="**Objective**\nCheck the wiki\nType {}wiki".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Wiki Unopenend", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Shop I" and userinfo["questpart"] == 0:
				em = discord.Embed(title="Shop I", description="**Objective**\nCheck the weapon shop\nType {}shop or {}shop weapons\nCheck the armor shop\nType {}shop armor\nBuy a weapon\nType {}shop buy <weapon name>\nBuy a piece of armor\nType {}shop buy <armor name>".format(ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="part 1/4\nWeapon shop not checked.", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Shop I" and userinfo["questpart"] == 1:
				userinfo["questprogress"] = 0
				em = discord.Embed(title="Shop I", description="**Objective**\nCheck the armor shop\nType {}shop armor\nBuy a weapon\nType {}shop buy <weapon name>\nBuy a piece of armor\nType {}shop buy <armor name>".format(ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="part 2/4\nArmor shop not checked.", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Shop I" and userinfo["questpart"] == 2:
				userinfo["questprogress"] = 0
				em = discord.Embed(title="Shop I", description="**Objective**\nBuy a weapon\nType {}shop buy <weapon name>\nBuy a piece of armor\nType {}shop buy <armor name>".format(ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="part 3/4\nNo weapon bought.", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Shop I" and userinfo["questpart"] == 3:
				userinfo["questprogress"] = 0
				em = discord.Embed(title="Shop I", description="**Objective**\nBuy a piece of armor\nType {}shop buy <armor name>".format(ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="part 4/4\nNo armor bought", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Check Profile":
				em = discord.Embed(title="Check Profile", description="**Objective**\nCheck Your own profile\nType {}profile".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="profile Unopenend", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Leaderboard":
				em = discord.Embed(title="Leaderboard", description="**Objective**\nCheck the leaderboard\nType {}leaderboard / {}top users".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="leaderboard unopened", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Guild I" and userinfo["questpart"] == 0:
				userinfo["questprogress"] = 0
				em = discord.Embed(title="Guild", description="**Objective**\nRepresent a guild.\nType {}guild or {}guild represent\nCheck the Guild info.\nType {}guild info\nCheck the guild mission.\nType {}guild mission\nCheck the guild donate function\nType {}Guild donate".format(ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="part 1/4\nNo Guild represented.", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Guild I" and userinfo["questpart"] == 1:
				userinfo["questprogress"] = 0
				em = discord.Embed(title="Guild", description="**Objective**\nCheck the Guild info.\nType {}guild info\nCheck the guild mission.\nType {}guild mission\nCheck the guild donate function\nType {}Guild donate".format(ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="part 2/4\nGuild info not checked.", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Guild I" and userinfo["questpart"] == 2:
				userinfo["questprogress"] = 0
				em = discord.Embed(title="Guild", description="**Objective**\nCheck the guild mission.\nType {}guild mission\nCheck the guild donate function\nType {}Guild donate".format(ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="part 3/4\nGuild mission not checked.", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Guild I" and userinfo["questpart"] == 3:
				userinfo["questprogress"] = 0
				em = discord.Embed(title="Guild", description="**Objective**\nCheck the guild donate function\nType {}Guild donate 1\nside note: you have to donate 1 gold for it to register.".format(ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="part 4/4\nGuild donate function unopened.", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Shop II":
				em = discord.Embed(title="Shop II", description="**Objective**\nSell a item in the shop!\nType {}Shop sell <number>".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="No item bought", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Market I":
				em = discord.Embed(title="Market I", description="**Objective**\nTry and list a item on the market!\nType {}market sell <number> <price>".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="No item listed", inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:	
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Guild II":
				em = discord.Embed(title="Guild II", description="**Objective**\nDonate 1000g to your guild!\nType {}guild donate 1000 / {}guild donate <amount>".format(ctx.prefix, ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/1000 <:Gold:639484869809930251> Donated".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Rachi I":
				em = discord.Embed(title="Rachi I", description="**Objective**\nSlay 10 Rachi's \nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Slain".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Debin I":
				em = discord.Embed(title="Debin I", description="**Objective**\nSlay 10 Debin's \nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Slain".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Oofer I":
				em = discord.Embed(title="Oofer I", description="**Objective**\nSlay 10 Oofer's \nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Slain".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Wyvern I":
				em = discord.Embed(title="Wyvern I", description="**Objective**\nSlay 10 Wyvern's \nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Slain".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Fire Golem I":
				em = discord.Embed(title="Fire Golem I", description="**Objective**\nSlay 10 Fire Golem's \nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/5 Slain".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Travel I":
				em = discord.Embed(title="Travel I", description="**Objective**\nTravel to location 2 Saker keep\nMin level requirement is 10\nType {}Travel".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Not traveled yet".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Draugr I":
				em = discord.Embed(title="Draugr I", description="**Objective**\nSlay 10 Draugr's \nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Slain".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Stalker I":
				em = discord.Embed(title="Stalker I", description="**Objective**\nSlay 10 Stalker's \nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Slain".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Souleater I":
				em = discord.Embed(title="Souleater I", description="**Objective**\nSlay 10 Souleater's \nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/10 Slain".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "The Corrupted I":
				em = discord.Embed(title="The Corrupted I", description="**Objective**\nSlay 10 Corrupted's \nType {}Fight".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="{}/5 Slain".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "Reforge I":
				em = discord.Embed(title="Reforge I", description="**Objective**\nReforge 1 item.\nType {}Reforge <Number>".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="No item reforged.".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
					
			elif userinfo["questname"] == "Support Server":
				em = discord.Embed(title="Support Server", description="**Objective**\nJoin the support server [here](https://discord.gg/9b3KkJvJea).".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="If you want to join its free! :P\n You can leave after!\nQuest done!".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				userinfo["questprogress"] = userinfo["questprogress"] + 1
				db.users.replace_one({ "_id": user.id }, userinfo, upsert=True) 
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return

			elif userinfo["questname"] == "On the hunt!":
				em = discord.Embed(title="On the hunt!", description="**Objective**\nHunt down a Rare Wyvern\n They have been spotted in the golden temple!\ntype {}travel 1 to go to the golden temple.".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Progress", value="Rare Wyvern not killed.".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
			else:
				em = discord.Embed(title="Quest not made", description="You have finished the last quest for now!".format(ctx.prefix), color=discord.Colour(0xffffff))
				em.add_field(name="Info", value="New quests will be added in the future!".format(userinfo["questprogress"]), inline=False)
				em.set_thumbnail(url=user.avatar_url)
				try:
					await ctx.send(embed=em)
				except:
					try:
						await ctx.send(fileIO(f"data/languages/EN.json", "load")["general"]["embedpermissions"]["translation"])
						return
					except:
						return
def setup(bot):
	n = quests(bot)
	bot.add_cog(n)